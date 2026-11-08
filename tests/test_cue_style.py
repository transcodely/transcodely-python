"""Tests for the 5.42.1 resync: caption cue styles and RestyleCaptions.

Pins ``CueStyle`` with a lowercase ``CueStylePreset`` in both directions,
``cue_style`` on apps, tracks and the inline-captions create requests, the
``RestyleCaptions`` request/response and the facade call, and
``Video.cost_breakdown``. Mirror of the TS / Go tests.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

import transcodely
from transcodely._codec.json_codec import deserialize, serialize
from transcodely.resources._helpers import fill_from_dict
from transcodely.resources.videos import Videos
from transcodely.v1 import app_pb2, subtitles_pb2, video_pb2


class _FakeTransport:
    def __init__(self, resp: Any) -> None:
        self.resp = resp
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self, service: str, method: str, request: Any, response: Any, opts: Any = None
    ) -> Any:
        self.calls.append((method, request))
        return self.resp


def test_cue_style_serializes_preset_lowercase_and_omits_unset_limits() -> None:
    style = subtitles_pb2.CueStyle(preset=transcodely.CueStylePreset.Value("CUE_STYLE_PRESET_LONG"))
    style.max_lines = 3
    assert json.loads(serialize(style).decode()) == {"preset": "long", "max_lines": 3}


def test_cue_style_deserializes_resolved_style() -> None:
    style = deserialize(
        json.dumps(
            {
                "preset": "compact",
                "max_chars_per_line": 42,
                "max_lines": 1,
                "max_cue_duration_ms": 4000,
            }
        ).encode(),
        transcodely.CueStyle(),
    )
    assert style.preset == subtitles_pb2.CUE_STYLE_PRESET_COMPACT
    assert (style.max_chars_per_line, style.max_lines, style.max_cue_duration_ms) == (42, 1, 4000)


def test_cue_style_on_app_update_and_track() -> None:
    req = fill_from_dict(
        app_pb2.UpdateAppRequest(), {"id": "app_abc", "cue_style": {"preset": "compact"}}
    )
    assert json.loads(serialize(req).decode())["cue_style"] == {"preset": "compact"}

    app = deserialize(
        json.dumps({"id": "app_abc", "cue_style": {"max_lines": 1}}).encode(), app_pb2.App()
    )
    assert app.HasField("cue_style") and app.cue_style.max_lines == 1
    assert not app.cue_style.HasField("preset")

    track = fill_from_dict(
        subtitles_pb2.SubtitleTrack(), {"operation": "generate", "cue_style": {"preset": "long"}}
    )
    assert json.loads(serialize(track).decode())["cue_style"] == {"preset": "long"}

    vtt = deserialize(
        json.dumps(
            {
                "id": "trk_abc",
                "updated_at": "2026-11-08T10:00:00Z",
                "cue_style": {
                    "preset": "standard",
                    "max_chars_per_line": 42,
                    "max_lines": 2,
                    "max_cue_duration_ms": 7000,
                },
            }
        ).encode(),
        video_pb2.VideoTextTrack(),
    )
    assert vtt.cue_style.preset == subtitles_pb2.CUE_STYLE_PRESET_STANDARD
    assert vtt.cue_style.max_cue_duration_ms == 7000
    assert vtt.updated_at.seconds > 0


_REQUESTS: list[tuple[Any, dict[str, Any]]] = [
    (video_pb2.CreateUploadRequest, {"filename": "clip.mp4"}),
    (video_pb2.CreateFromUrlRequest, {"url": "https://example.com/a.mp4"}),
    (video_pb2.CreateMultipartUploadRequest, {"filename": "big.mp4"}),
]


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_create_cue_style_serializes(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(cls(), {**base, "auto_captions": True, "cue_style": {"max_lines": 1}})
    assert json.loads(serialize(req).decode())["cue_style"] == {"max_lines": 1}
    # Unset, the optional message stays off the wire.
    assert "cue_style" not in json.loads(serialize(fill_from_dict(cls(), base)).decode())


def test_restyle_captions_request_wire_shape() -> None:
    req = fill_from_dict(
        video_pb2.RestyleCaptionsRequest(),
        {"id": "vid_a1b2c3d4e5f6g7", "language": "eng", "cue_style": {"preset": "compact"}},
    )
    assert json.loads(serialize(req).decode()) == {
        "id": "vid_a1b2c3d4e5f6g7",
        "language": "eng",
        "cue_style": {"preset": "compact"},
    }


def test_restyle_captions_facade_sends_request_and_returns_response() -> None:
    resp = video_pb2.RestyleCaptionsResponse(
        job_id="job_a1b2c3d4e5f6",
        video_id="vid_a1b2c3d4e5f6g7",
        language="eng",
        cue_style=subtitles_pb2.CueStyle(
            preset=subtitles_pb2.CUE_STYLE_PRESET_COMPACT,
            max_chars_per_line=42,
            max_lines=1,
            max_cue_duration_ms=4000,
        ),
    )
    t = _FakeTransport(resp)
    out = Videos(t).restyle_captions(  # type: ignore[arg-type]
        id="vid_a1b2c3d4e5f6g7", cue_style={"max_lines": 1}
    )
    method, req = t.calls[0]
    assert method == "RestyleCaptions"
    assert isinstance(req, transcodely.types.RestyleCaptionsRequest)
    assert req.id == "vid_a1b2c3d4e5f6g7"
    assert req.cue_style.max_lines == 1
    assert not req.cue_style.HasField("preset")
    assert not req.HasField("language")
    assert not req.HasField("app_id")
    assert out is resp
    assert out.cue_style.max_cue_duration_ms == 4000


def test_video_cost_breakdown_deserializes() -> None:
    video = deserialize(
        json.dumps(
            {
                "id": "vid_abc",
                "total_cost": 1.5,
                "cost_breakdown": [
                    {"kind": "encoding", "amount": 1.2},
                    {"kind": "captions", "amount": 0.3},
                ],
            }
        ).encode(),
        video_pb2.Video(),
    )
    assert [(line.kind, line.amount) for line in video.cost_breakdown] == [
        ("encoding", 1.2),
        ("captions", 0.3),
    ]
    assert isinstance(video.cost_breakdown[0], transcodely.VideoCostLine)
