"""Webhook signature verification.

Python port of the TypeScript SDK's ``webhooks/signature.ts``. The signing
math is identical across all Transcodely SDKs: HMAC-SHA-256 over
``"<unix-timestamp>.<raw-body-bytes>"``, hex-encoded, carried in the
``Transcodely-Signature`` header as ``t=<ts>,v1=<hex>``.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Callable, Optional, Union

from ..errors import WebhookSignatureError, WebhookTimestampError

#: Default signature tolerance window in seconds (Stripe parity).
DEFAULT_TOLERANCE_SECONDS = 300

#: HTTP header name carrying the signature (lower-cased for case-insensitive lookup).
SIGNATURE_HEADER = "transcodely-signature"

#: HTTP header name carrying the event ID (``evt_*``). Useful as an idempotency
#: key for handlers that dedupe redeliveries — the same event ID rides every
#: retry of a given event.
EVENT_ID_HEADER = "webhook-id"


def _parse_header(header: str) -> tuple[int, list[str]]:
    """Parse the ``Transcodely-Signature`` header.

    The header is a comma-separated list of ``key=value`` pairs. ``t`` is the
    unix timestamp (seconds); each ``v1`` entry is a hex-encoded
    HMAC-SHA-256. Unknown keys are ignored so future scheme versions don't
    break older receivers.
    """
    timestamp: Optional[int] = None
    signatures: list[str] = []
    for part in header.split(","):
        eq = part.find("=")
        if eq < 0:
            continue
        key = part[:eq].strip()
        value = part[eq + 1 :].strip()
        if key == "t":
            try:
                timestamp = int(value)
            except ValueError:
                # Divergence from the JS SDK (which parses with Number() and an
                # isInteger check, so it would accept "123.0"/"1e3"): int() is
                # stricter and rejects those. Harmless — the API always emits a
                # plain integer timestamp.
                continue
        elif key == "v1":
            signatures.append(value)
    if timestamp is None:
        raise WebhookSignatureError("Signature header is missing the timestamp (t=) component")
    if not signatures:
        raise WebhookSignatureError("Signature header has no v1 entries")
    return timestamp, signatures


def verify_signature(
    raw_body: Union[str, bytes],
    sig_header: str,
    secret: Union[str, list[str]],
    *,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
    now: Optional[Callable[[], int]] = None,
) -> None:
    """Verify a webhook signature. Raises on failure; returns ``None`` on success.

    Multiple secrets are accepted so a customer rotating their signing secret
    can pass ``[previous, current]`` during the overlap window without dropping
    legitimate deliveries signed under either key.

    :raises WebhookSignatureError: the header is malformed or no signature matched.
    :raises WebhookTimestampError: the timestamp is outside ``tolerance`` seconds.
    """
    timestamp, signatures = _parse_header(sig_header)

    now_fn: Callable[[], int] = now or (lambda: int(time.time()))
    if abs(now_fn() - timestamp) > tolerance:
        raise WebhookTimestampError(
            f"Signature timestamp is outside the tolerance window ({tolerance}s)"
        )

    secrets = [secret] if isinstance(secret, str) else secret
    body_bytes = raw_body.encode("utf-8") if isinstance(raw_body, str) else raw_body
    payload = f"{timestamp}.".encode("utf-8") + body_bytes

    for s in secrets:
        expected = hmac.new(s.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        for candidate in signatures:
            # `expected` is lowercase hex (hexdigest); normalize the candidate so
            # an upper/mixed-case hex digest still matches — the JS SDK compares
            # decoded bytes, which is inherently case-insensitive.
            if hmac.compare_digest(expected, candidate.lower()):
                return

    raise WebhookSignatureError("No signatures matched the expected value")


__all__ = [
    "DEFAULT_TOLERANCE_SECONDS",
    "EVENT_ID_HEADER",
    "SIGNATURE_HEADER",
    "verify_signature",
]
