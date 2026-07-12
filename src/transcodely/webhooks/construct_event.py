"""Verify a signed webhook delivery and decode it into a typed :class:`Event`.

Python port of the TypeScript SDK's ``webhooks/construct-event.ts``.
"""

from __future__ import annotations

import json
import math
from typing import Any, Callable, Mapping, Optional, Union

from ..errors import WebhookPayloadError
from .signature import DEFAULT_TOLERANCE_SECONDS, verify_signature
from .types import Event, EventRequest, decoder_for_type


def construct_event(
    raw_body: Union[str, bytes],
    sig_header: str,
    secret: Union[str, list[str]],
    *,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
    now: Optional[Callable[[], int]] = None,
) -> Event:
    """Verify a signed webhook delivery and return the typed :class:`Event`.

    ``secret`` may be a single signing secret or a list of secrets — pass
    ``[previous, current]`` during a secret rotation's overlap window.

    :raises WebhookSignatureError: the signature is missing/malformed or doesn't match.
    :raises WebhookTimestampError: the timestamp is outside the tolerance window.
    :raises WebhookPayloadError: the body isn't valid JSON or the envelope shape is wrong.
    """
    body_bytes = raw_body.encode("utf-8") if isinstance(raw_body, str) else raw_body

    verify_signature(body_bytes, sig_header, secret, tolerance=tolerance, now=now)

    try:
        parsed = json.loads(body_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as cause:
        raise WebhookPayloadError("Webhook body is not valid JSON") from cause

    return _build_event(parsed)


def _require_string(obj: Mapping[str, Any], key: str) -> str:
    v = obj.get(key)
    if not isinstance(v, str) or len(v) == 0:
        raise WebhookPayloadError(f"Webhook envelope is missing required string field `{key}`")
    return v


def _require_number(obj: Mapping[str, Any], key: str) -> int:
    v = obj.get(key)
    # bool is a subclass of int in Python — reject it explicitly so a JSON
    # `true` doesn't sail through as the number 1 (matches the TS typeof check).
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise WebhookPayloadError(f"Webhook envelope field `{key}` must be a number")
    return int(v)


def _build_event(parsed: Any) -> Event:
    if not isinstance(parsed, dict):
        raise WebhookPayloadError("Webhook body must be a JSON object")

    id_ = _require_string(parsed, "id")
    if parsed.get("object") != "event":
        raise WebhookPayloadError('Webhook envelope `object` must be "event"')
    api_version = _require_string(parsed, "api_version")
    created = _require_string(parsed, "created")
    type_ = _require_string(parsed, "type")
    pending_webhooks = _require_number(parsed, "pending_webhooks")

    data_raw = parsed.get("data")
    if not isinstance(data_raw, dict):
        raise WebhookPayloadError("Webhook envelope field `data` must be a JSON object")

    request_raw = parsed.get("request")
    if not isinstance(request_raw, dict):
        raise WebhookPayloadError("Webhook envelope field `request` must be a JSON object")
    # `request.id` is null for events emitted outside a request scope — every
    # worker-callback event (job.succeeded/failed/canceled/progress, output.*,
    # video.uploaded) and every SendTestWebhook delivery. Accept null or a
    # non-empty string; reject "" and non-strings (mirrors the JS SDK).
    request_id = request_raw.get("id")
    if request_id is not None and (not isinstance(request_id, str) or request_id == ""):
        raise WebhookPayloadError(
            "Webhook envelope field `request.id` must be a non-empty string or null"
        )
    idempotency_key = request_raw.get("idempotency_key")
    if idempotency_key is not None and not isinstance(idempotency_key, str):
        raise WebhookPayloadError(
            "Webhook envelope field `request.idempotency_key` must be a string or null"
        )

    decode = decoder_for_type(type_)
    data: Any = decode(data_raw) if decode else data_raw

    return Event(
        id=id_,
        object="event",
        api_version=api_version,
        created=created,
        type=type_,
        data=data,
        pending_webhooks=pending_webhooks,
        request=EventRequest(id=request_id, idempotency_key=idempotency_key),
    )


__all__ = ["construct_event"]
