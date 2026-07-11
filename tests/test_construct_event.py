"""Unit tests for construct_event (mirror of the TS construct-event suite)."""

from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

import pytest

from transcodely import Event, construct_event
from transcodely.errors import (
    WebhookPayloadError,
    WebhookSignatureError,
    WebhookTimestampError,
)
from transcodely.v1 import app_pb2, job_pb2, video_pb2

SECRET = "whsec_test_12345678901234567890abcdef"
TS = 1716480293


def envelope(type_: str, data: Any, **overrides: Any) -> dict[str, Any]:
    env: dict[str, Any] = {
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
    env.update(overrides)
    return env


def sign(body: bytes, *, secret: str = SECRET, ts: int = TS) -> str:
    digest = hmac.new(secret.encode(), f"{ts}.".encode() + body, hashlib.sha256).hexdigest()
    return f"t={ts},v1={digest}"


def construct(body: Any, *, secret: str = SECRET, ts: int = TS, now: int = TS) -> Event:
    raw = json.dumps(body) if not isinstance(body, (str, bytes)) else body
    raw_bytes = raw.encode() if isinstance(raw, str) else raw
    return construct_event(
        raw_bytes, sign(raw_bytes, secret=secret, ts=ts), secret, now=lambda: now
    )


# ---- Happy paths -------------------------------------------------------------


def test_job_succeeded_decodes_job() -> None:
    ev = construct(
        envelope("job.succeeded", {"id": "job_1", "object": "job", "status": "completed"})
    )
    assert isinstance(ev, Event)
    assert ev.type == "job.succeeded"
    assert isinstance(ev.data, job_pb2.Job)
    assert ev.data.id == "job_1"
    assert ev.data.status == job_pb2.JOB_STATUS_COMPLETED
    assert ev.object == "event"
    assert ev.livemode is True


def test_output_ready_decodes_job_output() -> None:
    ev = construct(envelope("output.ready", {"id": "jot_1", "output_url": "https://cdn/out.m3u8"}))
    assert isinstance(ev.data, job_pb2.JobOutput)
    assert ev.data.id == "jot_1"


def test_video_uploaded_decodes_video() -> None:
    ev = construct(envelope("video.uploaded", {"id": "vid_1"}))
    assert isinstance(ev.data, video_pb2.Video)
    assert ev.data.id == "vid_1"


def test_app_created_decodes_app() -> None:
    ev = construct(envelope("app.created", {"id": "app_1", "name": "My App"}))
    assert isinstance(ev.data, app_pb2.App)
    assert ev.data.id == "app_1"


def test_preserves_idempotency_key() -> None:
    env = envelope(
        "job.created", {"id": "job_1"}, request={"id": "req_1", "idempotency_key": "key_abc"}
    )
    ev = construct(env)
    assert ev.request.id == "req_1"
    assert ev.request.idempotency_key == "key_abc"


def test_accepts_null_request_id() -> None:
    # The API sends request.id == null for worker-emitted events (job.succeeded,
    # output.ready, ...) and for every SendTestWebhook delivery — must not reject.
    env = envelope("job.succeeded", {"id": "job_1"}, request={"id": None, "idempotency_key": None})
    ev = construct(env)
    assert ev.request.id is None


def test_rejects_empty_request_id() -> None:
    # "" is not a valid request id — the API sends null (not "") when there is no
    # originating request scope. Empty string must raise, not slip through.
    env = envelope("job.succeeded", {"id": "job_1"}, request={"id": "", "idempotency_key": None})
    with pytest.raises(WebhookPayloadError):
        construct(env)


def test_request_id_non_string_raises_payload_error() -> None:
    env = envelope("job.succeeded", {"id": "job_1"}, request={"id": 123, "idempotency_key": None})
    with pytest.raises(WebhookPayloadError):
        construct(env)


def test_accepts_bytes_and_str_body() -> None:
    body = json.dumps(envelope("job.created", {"id": "job_1"}))
    assert construct(body.encode()).id == "evt_1"
    assert construct(body).id == "evt_1"


def test_unknown_type_leaves_data_as_dict() -> None:
    ev = construct(envelope("future.thing", {"foo": "bar"}))
    assert ev.type == "future.thing"
    assert ev.data == {"foo": "bar"}


# ---- Error paths -------------------------------------------------------------


def test_tampered_body_raises_signature_error() -> None:
    body = json.dumps(envelope("job.succeeded", {"id": "job_1"})).encode()
    header = sign(body)
    with pytest.raises(WebhookSignatureError):
        construct_event(b'{"id":"evt_TAMPERED"}', header, SECRET, now=lambda: TS)


def test_wrong_secret_raises_signature_error() -> None:
    body = json.dumps(envelope("job.succeeded", {"id": "job_1"})).encode()
    with pytest.raises(WebhookSignatureError):
        construct_event(body, sign(body), "whsec_wrong", now=lambda: TS)


def test_expired_timestamp_raises_timestamp_error() -> None:
    with pytest.raises(WebhookTimestampError):
        construct(envelope("job.created", {"id": "job_1"}), now=TS + 301)


def test_invalid_json_raises_payload_error() -> None:
    with pytest.raises(WebhookPayloadError):
        construct("{not valid json")


def test_object_not_event_raises_payload_error() -> None:
    with pytest.raises(WebhookPayloadError):
        construct(envelope("job.created", {"id": "job_1"}, object="charge"))


def test_data_is_string_raises_payload_error() -> None:
    with pytest.raises(WebhookPayloadError):
        construct(envelope("job.succeeded", "not an object"))


def test_missing_id_raises_payload_error() -> None:
    env = envelope("job.succeeded", {"id": "job_1"})
    del env["id"]
    with pytest.raises(WebhookPayloadError):
        construct(env)


def test_bad_idempotency_key_type_raises_payload_error() -> None:
    env = envelope("job.created", {"id": "job_1"}, request={"id": "req_1", "idempotency_key": 123})
    with pytest.raises(WebhookPayloadError):
        construct(env)


def test_pending_webhooks_bool_raises_payload_error() -> None:
    # bool is a subclass of int in Python — it must not slip through as a number.
    with pytest.raises(WebhookPayloadError):
        construct(envelope("job.created", {"id": "job_1"}, pending_webhooks=True))


def test_json_array_body_raises_payload_error() -> None:
    body = b"[1,2,3]"
    with pytest.raises(WebhookPayloadError):
        construct_event(body, sign(body), SECRET, now=lambda: TS)
