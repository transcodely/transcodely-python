"""Tests for highlight clips: GenerateHighlights, Video.highlights, the create option.

Pins the request as snake_case with unset config fields off the wire, the
``VideoHighlight`` fields with the lowercase status enum in both directions, the
facade call, and ``highlights`` on all three video-creating requests. Mirror of
the TS / Go tests.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from transcodely._codec.json_codec import deserialize, serialize
from transcodely.resources._helpers import fill_from_dict
from transcodely.resources.videos import Videos
from transcodely.v1 import video_pb2


class _FakeTransport:
    def __init__(self, resp: Any) -> None:
        self.resp = resp
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self, service: str, method: str, request: Any, response: Any, opts: Any = None
    ) -> Any:
        self.calls.append((method, request))
        return self.resp


def test_request_serializes_snake_case() -> None:
    req = fill_from_dict(
        video_pb2.GenerateHighlightsRequest(),
        {"id": "vid_abc", "language": "eng", "config": {"max_count": 3, "padding_seconds": 2.0}},
    )
    obj = json.loads(serialize(req).decode())
    assert obj["id"] == "vid_abc"
    assert obj["language"] == "eng"
    assert obj["config"]["max_count"] == 3
    assert obj["config"]["padding_seconds"] == 2
    assert "min_seconds" not in obj["config"]
    assert "max_seconds" not in obj["config"]


def test_video_highlights_decode_with_lowercase_status() -> None:
    body = json.dumps(
        {
            "id": "vid_abc",
            "highlights": [
                {
                    "id": "hl_a1b2c3d4e5f6g7",
                    "start_seconds": 18.5,
                    "end_seconds": 31.5,
                    "title": "Patience.",
                    "status": "ready",
                    "playback_url": "https://cdn.example/x.mp4",
                    "duration_seconds": 13,
                    "job_id": "job_abc",
                    "language": "eng",
                },
                {
                    "id": "hl_b1b2c3d4e5f6g7",
                    "status": "failed",
                    "error_code": "queue_limit_exceeded",
                },
            ],
        }
    ).encode()
    video = deserialize(body, video_pb2.Video())
    ready, failed = video.highlights
    assert ready.status == video_pb2.VIDEO_HIGHLIGHT_STATUS_READY
    assert ready.start_seconds == 18.5
    assert ready.end_seconds == 31.5
    assert ready.playback_url == "https://cdn.example/x.mp4"
    assert ready.duration_seconds == 13
    assert failed.status == video_pb2.VIDEO_HIGHLIGHT_STATUS_FAILED
    assert failed.error_code == "queue_limit_exceeded"
    assert not failed.HasField("playback_url")

    obj = json.loads(
        serialize(
            video_pb2.VideoHighlight(status=video_pb2.VIDEO_HIGHLIGHT_STATUS_PENDING)
        ).decode()
    )
    assert obj["status"] == "pending"


def test_generate_highlights_sends_request_and_returns_list() -> None:
    resp = video_pb2.GenerateHighlightsResponse(
        highlights=[
            video_pb2.VideoHighlight(
                id="hl_a1b2c3d4e5f6g7",
                start_seconds=18.5,
                end_seconds=31.5,
                status=video_pb2.VIDEO_HIGHLIGHT_STATUS_PENDING,
            )
        ]
    )
    t = _FakeTransport(resp)
    out = Videos(t).generate_highlights(id="vid_a1b2c3d4e5f6g7", config={"max_count": 3})  # type: ignore[arg-type]
    method, req = t.calls[0]
    assert method == "GenerateHighlights"
    assert isinstance(req, video_pb2.GenerateHighlightsRequest)
    assert req.id == "vid_a1b2c3d4e5f6g7"
    assert req.config.max_count == 3
    assert not req.HasField("app_id")
    assert isinstance(out, list)
    assert len(out) == 1
    assert out[0].id == "hl_a1b2c3d4e5f6g7"
    assert out[0].status == video_pb2.VIDEO_HIGHLIGHT_STATUS_PENDING


_REQUESTS: list[tuple[Any, dict[str, Any]]] = [
    (video_pb2.CreateUploadRequest, {"filename": "clip.mp4"}),
    (video_pb2.CreateFromUrlRequest, {"url": "https://example.com/a.mp4"}),
    (video_pb2.CreateMultipartUploadRequest, {"filename": "big.mp4"}),
]


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_create_highlights_option_serializes(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(
        cls(),
        {
            **base,
            "auto_captions": True,
            "auto_insights": True,
            "highlights": {"enabled": True, "max_count": 3},
        },
    )
    obj = json.loads(serialize(req).decode())
    assert obj["highlights"] == {"enabled": True, "max_count": 3}


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_create_highlights_absent_when_unset(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(cls(), base)
    assert not req.HasField("highlights")
    assert "highlights" not in json.loads(serialize(req).decode())
