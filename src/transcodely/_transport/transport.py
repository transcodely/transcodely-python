"""Hand-rolled Connect-RPC HTTP transport over httpx.

Why not a Connect-Python client library? The ecosystem is sparse and none
expose hooks for swapping the JSON codec, but Transcodely's wire format
requires snake_case + simplified-enum JSON. Owning the transport gives us
end-to-end control with ~250 LoC.

Wire format reference:
  - Unary: POST {base_url}/{service.full_name}/{method.name}
           Content-Type: application/json
           body: JSON-encoded request
  - Server-streaming: same URL, Content-Type: application/connect+json
           body: 5-byte envelope header + JSON payload, repeated
           stream ends with an end-stream frame (flag bit 0x02)
"""

from __future__ import annotations

import random
import struct
import time
from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass, field
from typing import Any, TypeVar

import httpx
from google.protobuf.message import Message
from typing_extensions import Self

from .._codec import json_codec
from ..errors import RateLimitError, TranscodelyError
from ..version import API_VERSION, DEFAULT_BASE_URL
from .error_mapping import connection_error, map_http_error
from .headers import client_user_agent_json, new_idempotency_key, user_agent

TReq = TypeVar("TReq", bound=Message)
TRes = TypeVar("TRes", bound=Message)


@dataclass
class CallOptions:
    """Per-call overrides for timeout, retries, idempotency, headers."""

    timeout: float | None = None
    max_retries: int | None = None
    idempotency_key: str | None = None
    api_version: str | None = None
    headers: dict[str, str] = field(default_factory=dict)


@dataclass
class LogEvent:
    service: str
    method: str
    duration_ms: int
    attempt: int
    status: int | None = None
    request_id: str | None = None
    error: TranscodelyError | None = None


_WRITE_PREFIXES = ("Create", "Update", "Delete", "Cancel", "Confirm", "Revoke", "Archive", "Enable")


def _is_write(method_name: str) -> bool:
    return any(method_name.startswith(p) for p in _WRITE_PREFIXES)


class Transport:
    """Synchronous transport. ``client.jobs.*`` calls go through this."""

    def __init__(
        self,
        api_key: str,
        *,
        organization_id: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        api_version: str | None = None,
        default_headers: dict[str, str] | None = None,
        http_client: httpx.Client | None = None,
        logger: Callable[[LogEvent], None] | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("Transcodely: api_key is required")
        self.api_key = api_key
        self.organization_id = organization_id
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.api_version = api_version or API_VERSION
        self.default_headers = default_headers or {}
        self._client = http_client or httpx.Client(timeout=timeout)
        self._owns_client = http_client is None
        self._logger = logger
        #: ID of the most recent successful or failed request, Stripe-style.
        self.last_request_id: str | None = None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    # ---------- unary ----------

    def unary(
        self,
        service_name: str,
        method_name: str,
        request: Message,
        response: TRes,
        opts: CallOptions | None = None,
    ) -> TRes:
        opts = opts or CallOptions()
        url = f"{self.base_url}/{service_name}/{method_name}"
        body = json_codec.serialize(request)
        idempotency_key = (
            opts.idempotency_key or new_idempotency_key() if _is_write(method_name) else None
        )

        def attempt_call(attempt: int) -> TRes:
            headers = self._build_headers(opts, "application/json", idempotency_key)
            started = time.monotonic()
            try:
                resp = self._client.post(
                    url,
                    content=body,
                    headers=headers,
                    timeout=opts.timeout if opts.timeout is not None else self.timeout,
                )
            except httpx.HTTPError as exc:
                raise connection_error(exc) from exc
            self.last_request_id = resp.headers.get("x-request-id") or self.last_request_id
            self._emit(
                LogEvent(
                    service=service_name,
                    method=method_name,
                    attempt=attempt,
                    duration_ms=int((time.monotonic() - started) * 1000),
                    status=resp.status_code,
                    request_id=self.last_request_id,
                )
            )
            if not (200 <= resp.status_code < 300):
                raise map_http_error(
                    status=resp.status_code,
                    body=_try_json(resp.content),
                    headers=resp.headers,
                )
            return json_codec.deserialize(resp.content, response)

        return self._with_retry(service_name, method_name, opts, attempt_call)

    # ---------- server-streaming ----------

    def stream(
        self,
        service_name: str,
        method_name: str,
        request: Message,
        response_factory: Callable[[], TRes],
        opts: CallOptions | None = None,
    ) -> Generator[TRes, None, None]:
        opts = opts or CallOptions()
        url = f"{self.base_url}/{service_name}/{method_name}"
        headers = self._build_headers(opts, "application/connect+json")
        body = _encode_envelope(0, json_codec.serialize(request))
        try:
            with self._client.stream(
                "POST",
                url,
                content=body,
                headers=headers,
                timeout=opts.timeout if opts.timeout is not None else None,
            ) as resp:
                self.last_request_id = resp.headers.get("x-request-id") or self.last_request_id
                if not (200 <= resp.status_code < 300):
                    text = resp.read()
                    raise map_http_error(
                        status=resp.status_code,
                        body=_try_json(text),
                        headers=resp.headers,
                    )
                for frame in _read_envelopes(resp.iter_bytes()):
                    flags, payload = frame
                    if flags & 0x02:
                        # End-stream frame: payload may carry a JSON `error` block.
                        if not payload:
                            return
                        end = _try_json(payload)
                        if isinstance(end, dict) and end.get("error"):
                            raise map_http_error(
                                status=400,
                                body=end["error"],
                                headers=resp.headers,
                            )
                        return
                    yield json_codec.deserialize(payload, response_factory())
        except httpx.HTTPError as exc:
            raise connection_error(exc) from exc

    # ---------- helpers ----------

    def _build_headers(
        self,
        opts: CallOptions,
        content_type: str,
        idempotency_key: str | None = None,
    ) -> dict[str, str]:
        headers = {
            "content-type": content_type,
            "connect-protocol-version": "1",
            "authorization": f"Bearer {self.api_key}",
            "user-agent": user_agent(),
            "x-transcodely-client-user-agent": client_user_agent_json(),
            "transcodely-version": opts.api_version or self.api_version,
            "accept": content_type,
        }
        if self.organization_id:
            headers["x-organization-id"] = self.organization_id
        if idempotency_key:
            headers["idempotency-key"] = idempotency_key
        headers.update(self.default_headers)
        headers.update(opts.headers)
        return headers

    def _emit(self, event: LogEvent) -> None:
        if self._logger is not None:
            try:
                self._logger(event)
            except Exception:  # noqa: BLE001, S110 — a caller's logger must never break requests
                pass

    def _with_retry(
        self,
        service: str,
        method: str,
        opts: CallOptions,
        fn: Callable[[int], TRes],
    ) -> TRes:
        max_retries = opts.max_retries if opts.max_retries is not None else self.max_retries
        last_error: BaseException | None = None
        for attempt in range(1, max_retries + 2):
            try:
                return fn(attempt)
            except Exception as exc:
                last_error = exc
                if attempt > max_retries or not _is_retryable(exc):
                    raise
                _sleep_backoff(attempt, exc)
        if last_error is not None:
            raise last_error
        raise RuntimeError("unreachable")


def _is_retryable(exc: BaseException) -> bool:
    if not isinstance(exc, TranscodelyError):
        return False
    if isinstance(exc, RateLimitError):
        return True
    if exc.__class__.__name__ == "APIConnectionError":
        return True
    return exc.http_status is not None and exc.http_status >= 500


def _sleep_backoff(attempt: int, exc: BaseException) -> None:
    if isinstance(exc, RateLimitError) and exc.retry_after_ms is not None:
        time.sleep(max(0.0, exc.retry_after_ms / 1000.0))
        return
    base = 0.25
    cap = 2.0
    expo = min(cap, base * 2 ** (attempt - 1))
    jitter = expo * (0.5 + random.random() * 0.5)
    time.sleep(jitter)


# ---------- Connect envelope helpers ----------


def _encode_envelope(flags: int, payload: bytes) -> bytes:
    return struct.pack(">BI", flags & 0xFF, len(payload)) + payload


def _read_envelopes(stream: Iterable[bytes]) -> Generator[tuple[int, bytes], None, None]:
    buf = bytearray()
    for chunk in stream:
        if chunk:
            buf.extend(chunk)
        while len(buf) >= 5:
            flags = buf[0]
            length = struct.unpack(">I", bytes(buf[1:5]))[0]
            if len(buf) < 5 + length:
                break
            payload = bytes(buf[5 : 5 + length])
            del buf[: 5 + length]
            yield flags, payload
    if buf:
        # Trailing bytes that didn't make a complete frame
        raise connection_error(RuntimeError("stream ended with partial frame"))


def _try_json(data: bytes) -> Any:
    if not data:
        return None
    try:
        import json

        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return data.decode("utf-8", errors="replace")
