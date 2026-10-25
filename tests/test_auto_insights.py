"""Tests for the ``auto_insights`` upload opt-in.

Pins the wire format on all three video-creating requests: snake_case
``auto_insights`` beside ``auto_captions``, and absent when unset. Mirror of the
TS / Go auto-insights tests.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from transcodely._codec.json_codec import serialize
from transcodely.resources._helpers import fill_from_dict
from transcodely.v1 import video_pb2

_REQUESTS: list[tuple[Any, dict[str, Any]]] = [
    (video_pb2.CreateUploadRequest, {"filename": "clip.mp4"}),
    (video_pb2.CreateFromUrlRequest, {"url": "https://example.com/a.mp4"}),
    (video_pb2.CreateMultipartUploadRequest, {"filename": "big.mp4"}),
]


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_auto_insights_serializes_snake_case(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(cls(), {**base, "auto_captions": True, "auto_insights": True})
    assert req.auto_insights is True
    obj = json.loads(serialize(req).decode())
    assert obj["auto_insights"] is True
    assert obj["auto_captions"] is True
    assert "autoInsights" not in obj


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_auto_insights_absent_when_unset(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(cls(), {**base, "auto_captions": True})
    assert not req.HasField("auto_insights")
    obj = json.loads(serialize(req).decode())
    assert "auto_insights" not in obj
