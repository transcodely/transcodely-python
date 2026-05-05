"""Map a Connect-RPC error response (HTTP status + JSON body) to a typed exception."""

from __future__ import annotations

import json
from typing import Any, Mapping, Optional

from ..errors import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    ConflictError,
    FieldViolation,
    InvalidRequestError,
    NotFoundError,
    PermissionError,
    PreconditionError,
    RateLimitError,
    TranscodelyError,
)


def map_http_error(*, status: int, body: Any, headers: Mapping[str, str]) -> TranscodelyError:
    request_id = _header(headers, "x-request-id")
    parsed = _parse_body(body)
    message = parsed.get("message") or f"HTTP {status}"
    detail = (parsed.get("details") or [{}])[0].get("debug") or {}
    code = detail.get("code")
    raw_violations = detail.get("field_violations") or detail.get("fieldViolations") or []
    violations = [
        FieldViolation(field=v.get("field", ""), description=v.get("description", ""))
        for v in raw_violations
        if isinstance(v, dict)
    ]
    kwargs = {
        "code": code,
        "type": parsed.get("code"),
        "errors": violations,
        "http_status": status,
        "request_id": request_id,
        "raw": body,
    }

    if status == 401:
        return AuthenticationError(message, **kwargs)
    if status == 403:
        return PermissionError(message, **kwargs)
    if status == 404:
        return NotFoundError(message, **kwargs)
    if status == 409:
        return ConflictError(message, **kwargs)
    if status == 412:
        return PreconditionError(message, **kwargs)
    if status == 422:
        return InvalidRequestError(message, **kwargs)
    if status == 429:
        retry_after = _header(headers, "retry-after")
        retry_after_ms: Optional[int] = None
        if retry_after:
            try:
                retry_after_ms = max(0, int(retry_after) * 1000)
            except ValueError:
                retry_after_ms = None
        return RateLimitError(message, retry_after_ms=retry_after_ms, **kwargs)
    if status >= 500:
        return APIError(message, **kwargs)
    if status >= 400:
        return InvalidRequestError(message, **kwargs)
    return APIError(message, **kwargs)


def connection_error(cause: BaseException, message: Optional[str] = None) -> APIConnectionError:
    msg = message or str(cause) or "network request failed"
    err = APIConnectionError(msg)
    err.__cause__ = cause
    return err


def _parse_body(body: Any) -> dict[str, Any]:
    if isinstance(body, dict):
        return body
    if isinstance(body, (bytes, bytearray)):
        try:
            return json.loads(body.decode("utf-8"))
        except Exception:
            return {"message": body.decode("utf-8", errors="replace")}
    if isinstance(body, str):
        try:
            return json.loads(body)
        except Exception:
            return {"message": body}
    return {}


def _header(headers: Mapping[str, str], key: str) -> Optional[str]:
    # httpx headers are case-insensitive but expose .get with the lowercase form.
    if hasattr(headers, "get"):
        try:
            return headers.get(key) or headers.get(key.title())
        except Exception:
            return None
    return None
