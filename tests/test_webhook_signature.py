"""Unit tests for webhook signature verification (mirror of the TS signature suite)."""

from __future__ import annotations

import hashlib
import hmac

import pytest

from transcodely.errors import WebhookSignatureError, WebhookTimestampError
from transcodely.webhooks.signature import (
    DEFAULT_TOLERANCE_SECONDS,
    EVENT_ID_HEADER,
    SIGNATURE_HEADER,
    verify_signature,
)

SECRET = "whsec_test_12345678901234567890abcdef"
BODY = b'{"id":"evt_1","type":"job.succeeded"}'
TS = 1716480293


def sign(secret: str, ts: int, body: bytes) -> str:
    return hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()


def header(ts: int = TS, *, secret: str = SECRET, body: bytes = BODY) -> str:
    return f"t={ts},v1={sign(secret, ts, body)}"


def at(ts: int):  # type: ignore[no-untyped-def]
    return lambda: ts


def test_constants() -> None:
    assert DEFAULT_TOLERANCE_SECONDS == 300
    assert SIGNATURE_HEADER == "transcodely-signature"
    assert EVENT_ID_HEADER == "webhook-id"


def test_accepts_uppercase_hex_signature() -> None:
    # Signatures are lowercase hex in practice, but an upper/mixed-case hex
    # digest must still verify — the JS SDK compares decoded bytes (parity).
    h = f"t={TS},v1={sign(SECRET, TS, BODY).upper()}"
    verify_signature(BODY, h, SECRET, now=at(TS))  # no raise


def test_accepts_well_formed_single_v1() -> None:
    verify_signature(BODY, header(), SECRET, now=at(TS))  # no raise


def test_accepts_str_or_bytes_body() -> None:
    verify_signature(BODY.decode(), header(), SECRET, now=at(TS))


def test_accepts_multiple_v1_entries_one_matching() -> None:
    h = f"t={TS},v1=deadbeef,v1={sign(SECRET, TS, BODY)}"
    verify_signature(BODY, h, SECRET, now=at(TS))


def test_accepts_secret_list_rotation() -> None:
    # Body signed with the new secret; old secret listed first.
    h = header(secret="whsec_new_secret_value")
    verify_signature(BODY, h, ["whsec_old_secret_value", "whsec_new_secret_value"], now=at(TS))


def test_rejects_tampered_body() -> None:
    with pytest.raises(WebhookSignatureError):
        verify_signature(b'{"id":"evt_TAMPERED"}', header(), SECRET, now=at(TS))


def test_rejects_wrong_secret() -> None:
    with pytest.raises(WebhookSignatureError):
        verify_signature(BODY, header(), "whsec_wrong_secret", now=at(TS))


def test_accepts_timestamp_at_tolerance_edge() -> None:
    verify_signature(BODY, header(ts=TS), SECRET, tolerance=300, now=at(TS + 300))


def test_rejects_timestamp_beyond_tolerance() -> None:
    with pytest.raises(WebhookTimestampError):
        verify_signature(BODY, header(ts=TS), SECRET, tolerance=300, now=at(TS + 301))


def test_honors_custom_tolerance() -> None:
    # 100s skew passes at tolerance=120 but fails at tolerance=60.
    verify_signature(BODY, header(ts=TS), SECRET, tolerance=120, now=at(TS + 100))
    with pytest.raises(WebhookTimestampError):
        verify_signature(BODY, header(ts=TS), SECRET, tolerance=60, now=at(TS + 100))


def test_rejects_missing_timestamp() -> None:
    h = f"v1={sign(SECRET, TS, BODY)}"
    with pytest.raises(WebhookSignatureError):
        verify_signature(BODY, h, SECRET, now=at(TS))


def test_rejects_no_v1_entries() -> None:
    with pytest.raises(WebhookSignatureError):
        verify_signature(BODY, f"t={TS}", SECRET, now=at(TS))


def test_ignores_unknown_scheme_keys() -> None:
    h = f"t={TS},v0=legacy,v1={sign(SECRET, TS, BODY)},v2=future"
    verify_signature(BODY, h, SECRET, now=at(TS))


def test_rejects_length_mismatched_signature() -> None:
    # A truncated hex digest must not match (and must not raise on length).
    short = sign(SECRET, TS, BODY)[:10]
    with pytest.raises(WebhookSignatureError):
        verify_signature(BODY, f"t={TS},v1={short}", SECRET, now=at(TS))
