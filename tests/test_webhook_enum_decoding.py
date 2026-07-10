"""Regression tests for the webhook enum-decoding bug found & fixed in the TS SDK.

The API serializes a webhook event's inner ``data`` resource with SIMPLIFIED
LOWERCASE enum values (e.g. ``JOB_STATUS_COMPLETED`` → ``"completed"``), identical
to Get-RPC responses. A correct SDK must route the webhook decode through the same
enum-EXPANDING codec the RPC path uses *before* unmarshaling — otherwise the enum
silently becomes UNSPECIFIED (0) under ``ParseDict(ignore_unknown_fields=True)``,
exactly the TS failure mode.

These tests fail (enum == 0) if that expansion is ever bypassed. They cover both
decode paths (the verify/construct_event path and the events-resource bridge),
plus an externally-computed known-answer signature check.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

import pytest

from transcodely import construct_event, verify_signature
from transcodely.errors import WebhookSignatureError
from transcodely.resources.events import proto_event_to_sdk
from transcodely.v1 import app_pb2, job_pb2, webhook_pb2

SECRET = "whsec_test_12345678901234567890abcdef"
TS = 1716480293


def _envelope(type_: str, data: dict[str, Any]) -> str:
    return json.dumps(
        {
            "id": "evt_1",
            "object": "event",
            "api_version": "2026-05-23",
            "created": "2026-05-24T10:55:08Z",
            "type": type_,
            "data": data,
            "livemode": True,
            "pending_webhooks": 0,
            "request": {"id": "req_1", "idempotency_key": None},
        }
    )


def _construct(body: str) -> Any:
    sig = hmac.new(SECRET.encode(), f"{TS}.{body}".encode(), hashlib.sha256).hexdigest()
    return construct_event(body, f"t={TS},v1={sig}", SECRET, now=lambda: TS)


def _bridge(type_: str, data: dict[str, Any]) -> Any:
    """Decode via the events-resource path (proto Event -> SDK Event)."""
    return proto_event_to_sdk(webhook_pb2.Event(type=type_, data=json.dumps(data)))


# --- construct_event (HTTP verify) path --------------------------------------


def test_construct_event_expands_job_enums() -> None:
    ev = _construct(
        _envelope(
            "job.succeeded",
            {"id": "job_1", "object": "job", "status": "completed", "priority": "premium"},
        )
    )
    assert ev.data.status == job_pb2.JOB_STATUS_COMPLETED  # NOT UNSPECIFIED/0
    assert ev.data.status != job_pb2.JOB_STATUS_UNSPECIFIED
    assert ev.data.priority == job_pb2.JOB_PRIORITY_PREMIUM


def test_construct_event_expands_output_status() -> None:
    ev = _construct(_envelope("output.ready", {"id": "jot_1", "status": "completed"}))
    assert ev.data.status == job_pb2.OUTPUT_STATUS_COMPLETED
    assert ev.data.status != job_pb2.OUTPUT_STATUS_UNSPECIFIED


def test_construct_event_expands_app_status() -> None:
    ev = _construct(_envelope("app.created", {"id": "app_1", "object": "app", "status": "active"}))
    assert ev.data.status == app_pb2.APP_STATUS_ACTIVE
    assert ev.data.status != app_pb2.APP_STATUS_UNSPECIFIED


# --- events-resource (proto bridge) path -------------------------------------


def test_bridge_expands_job_enums() -> None:
    ev = _bridge("job.succeeded", {"id": "job_1", "status": "processing", "priority": "economy"})
    assert ev.data.status == job_pb2.JOB_STATUS_PROCESSING
    assert ev.data.priority == job_pb2.JOB_PRIORITY_ECONOMY


def test_bridge_expands_app_status() -> None:
    ev = _bridge("app.created", {"id": "app_1", "status": "archived"})
    assert ev.data.status == app_pb2.APP_STATUS_ARCHIVED


# --- Independent known-answer signature cross-check --------------------------

# Golden = HMAC-SHA256(secret, "<ts>.<body>"), computed externally via OpenSSL —
# independent of both the Go server and this SDK.
_GA_SECRET = "whsec_known_answer_test_key_here"
_GA_TS = 1700000000
_GA_BODY = '{"id":"job_abc123","status":"succeeded"}'
_GA_GOLDEN = "738628e4926e9ad49a18b13f0e83519f30e3a79650f68528a4b69dfe27abdd93"


def test_signature_matches_external_golden() -> None:
    computed = hmac.new(
        _GA_SECRET.encode(), f"{_GA_TS}.{_GA_BODY}".encode(), hashlib.sha256
    ).hexdigest()
    assert computed == _GA_GOLDEN  # SDK's HMAC primitive agrees with OpenSSL


def test_verify_accepts_golden_signature() -> None:
    verify_signature(
        _GA_BODY, f"t={_GA_TS},v1={_GA_GOLDEN}", _GA_SECRET, now=lambda: _GA_TS
    )  # no raise


def test_verify_rejects_tampered_golden_signature() -> None:
    # Flip the last hex char.
    flipped = _GA_GOLDEN[:-1] + ("4" if _GA_GOLDEN[-1] != "4" else "5")
    with pytest.raises(WebhookSignatureError):
        verify_signature(_GA_BODY, f"t={_GA_TS},v1={flipped}", _GA_SECRET, now=lambda: _GA_TS)
