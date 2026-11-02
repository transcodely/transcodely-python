"""Tests for source retention on the wire.

Pins retain-at-create (snake_case ``source_pinned`` on all three
video-creating requests, absent when unset), ``Video.source_expires_at`` and
the ``UsageSummary`` retained-source pair. Mirror of the Go codec test.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import pytest

from transcodely._codec.json_codec import deserialize, serialize
from transcodely.resources._helpers import fill_from_dict
from transcodely.v1 import video_pb2

_REQUESTS: list[tuple[Any, dict[str, Any]]] = [
    (video_pb2.CreateUploadRequest, {"filename": "clip.mp4"}),
    (video_pb2.CreateFromUrlRequest, {"url": "https://example.com/a.mp4"}),
    (video_pb2.CreateMultipartUploadRequest, {"filename": "big.mp4"}),
]


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_source_pinned_serializes_snake_case(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(cls(), {**base, "source_pinned": True})
    assert req.source_pinned is True
    obj = json.loads(serialize(req).decode())
    assert obj["source_pinned"] is True
    assert "sourcePinned" not in obj


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_source_pinned_absent_when_unset(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(cls(), dict(base))
    assert not req.HasField("source_pinned")
    obj = json.loads(serialize(req).decode())
    assert "source_pinned" not in obj


def test_video_source_expires_at_decodes() -> None:
    payload = b'{"video":{"id":"vid_abc","source_pinned":false,"source_expires_at":"2026-11-08T21:23:00Z"}}'
    resp = deserialize(payload, video_pb2.GetVideoResponse())
    assert resp.video.HasField("source_expires_at")
    got = resp.video.source_expires_at.ToDatetime(tzinfo=timezone.utc)
    assert got == datetime(2026, 11, 8, 21, 23, tzinfo=timezone.utc)


def test_usage_summary_retained_source_pair_decodes() -> None:
    payload = (
        b'{"storage_gb_avg":1.5,"storage_cost":0.03,'
        b'"retained_source_gb_avg":500,"retained_source_cost":10,"total_cost":10.03}'
    )
    usage = deserialize(payload, video_pb2.UsageSummary())
    assert usage.retained_source_gb_avg == 500
    assert usage.retained_source_cost == 10
    assert usage.storage_gb_avg == 1.5
