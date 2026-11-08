"""Tests for the 5.43.0 resync: caption style variants.

Pins ``VideoTextTrack.is_default`` / ``style_variant`` / ``stale`` from the
wire, ``RestyleCaptions`` ``make_default`` / ``adds_variant``, and the
``SetDefaultCaptionStyle`` / ``DeleteCaptionStyle`` facade calls. Mirror of the
TS / Go tests.
"""

from __future__ import annotations

import json
from typing import Any

import transcodely
from transcodely._codec.json_codec import deserialize, serialize
from transcodely.resources._helpers import fill_from_dict
from transcodely.resources.videos import Videos
from transcodely.v1 import subtitles_pb2, video_pb2


class _FakeTransport:
    def __init__(self, resp: Any) -> None:
        self.resp = resp
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self, service: str, method: str, request: Any, response: Any, opts: Any = None
    ) -> Any:
        self.calls.append((method, request))
        return self.resp


# Two English styles (long the default) plus a translation made stale by the
# default changing, as the API sends it.
_VARIANT_VIDEO = {
    "id": "vid_a1b2c3d4e5f6g7",
    "text_tracks": [
        {
            "id": "trk_long",
            "language": "eng",
            "label": "English",
            "auto_generated": True,
            "is_default": True,
            "style_variant": "long",
        },
        {
            "id": "trk_std",
            "language": "eng",
            "label": "English (standard)",
            "auto_generated": True,
            "style_variant": "standard",
        },
        {
            "id": "trk_bul",
            "language": "bul",
            "label": "Bulgarian",
            "auto_generated": True,
            "is_default": True,
            "style_variant": "long",
            "translated_from": "eng",
            "stale": True,
        },
    ],
}


def test_text_track_variant_fields_deserialize() -> None:
    video = deserialize(json.dumps(_VARIANT_VIDEO).encode(), transcodely.Video())
    default, other, translation = video.text_tracks
    assert default.is_default
    assert default.style_variant == subtitles_pb2.CUE_STYLE_PRESET_LONG
    assert default.label == "English"
    assert not other.is_default
    assert other.style_variant == subtitles_pb2.CUE_STYLE_PRESET_STANDARD
    assert other.label == "English (standard)"
    assert not other.stale
    assert translation.stale
    assert translation.translated_from == "eng"


def test_text_track_style_variant_absent_for_supplied_track() -> None:
    video = deserialize(
        json.dumps({"id": "vid_x", "text_tracks": [{"id": "trk_up", "language": "eng"}]}).encode(),
        transcodely.Video(),
    )
    track = video.text_tracks[0]
    assert not track.HasField("style_variant")
    assert not track.is_default
    assert not track.stale


def test_restyle_captions_make_default_and_adds_variant() -> None:
    req = fill_from_dict(
        video_pb2.RestyleCaptionsRequest(),
        {"id": "vid_a1b2c3d4e5f6g7", "cue_style": {"preset": "compact"}, "make_default": True},
    )
    assert json.loads(serialize(req).decode()) == {
        "id": "vid_a1b2c3d4e5f6g7",
        "cue_style": {"preset": "compact"},
        "make_default": True,
    }
    resp = deserialize(
        json.dumps(
            {"job_id": "job_a1b2c3d4e5f6", "style_variant": "compact", "adds_variant": True}
        ).encode(),
        video_pb2.RestyleCaptionsResponse(),
    )
    assert resp.style_variant == subtitles_pb2.CUE_STYLE_PRESET_COMPACT
    assert resp.adds_variant


def test_set_default_caption_style_facade_returns_video() -> None:
    resp = deserialize(
        json.dumps({"video": _VARIANT_VIDEO}).encode(),
        video_pb2.SetDefaultCaptionStyleResponse(),
    )
    t = _FakeTransport(resp)
    video = Videos(t).set_default_caption_style(  # type: ignore[arg-type]
        id="vid_a1b2c3d4e5f6g7", language="eng", style_variant="long"
    )
    method, req = t.calls[0]
    assert method == "SetDefaultCaptionStyle"
    assert isinstance(req, transcodely.types.SetDefaultCaptionStyleRequest)
    assert json.loads(serialize(req).decode()) == {
        "id": "vid_a1b2c3d4e5f6g7",
        "language": "eng",
        "style_variant": "long",
    }
    assert isinstance(video, transcodely.Video)
    assert video is resp.video
    assert video.text_tracks[0].is_default


def test_delete_caption_style_facade_returns_video() -> None:
    resp = video_pb2.DeleteCaptionStyleResponse(video=video_pb2.Video(id="vid_a1b2c3d4e5f6g7"))
    t = _FakeTransport(resp)
    video = Videos(t).delete_caption_style(  # type: ignore[arg-type]
        id="vid_a1b2c3d4e5f6g7", language="eng", style_variant="standard", app_id="app_xyz"
    )
    method, req = t.calls[0]
    assert method == "DeleteCaptionStyle"
    assert isinstance(req, transcodely.types.DeleteCaptionStyleRequest)
    assert json.loads(serialize(req).decode()) == {
        "id": "vid_a1b2c3d4e5f6g7",
        "language": "eng",
        "style_variant": "standard",
        "app_id": "app_xyz",
    }
    assert video is resp.video
    assert video.id == "vid_a1b2c3d4e5f6g7"
