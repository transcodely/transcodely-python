"""Tests for the F2 animated hover-preview surface.

Pins the wire format for the animated ThumbnailMode: snake_case field names,
the ``mode`` enum simplified to the lowercase string ``"animated"``, and the
Video hover-preview URL fields parsing back off the wire. Mirror of the TS / Go
animated-preview codec tests.
"""

from __future__ import annotations

import json

from transcodely._codec.json_codec import deserialize, serialize
from transcodely.resources._helpers import fill_from_dict
from transcodely.v1 import thumbnails_pb2, video_pb2


class TestAnimatedThumbnailSpec:
    def test_serializes_snake_case_fields_and_lowercase_enum(self) -> None:
        spec = thumbnails_pb2.ThumbnailSpec(
            mode=thumbnails_pb2.THUMBNAIL_MODE_ANIMATED,
            duration_seconds=6,
            fps=10,
            start_offsets=[1.5, 4, 9.25],
        )
        obj = json.loads(serialize(spec).decode())
        # Mode simplifies to the lowercase wire string.
        assert obj["mode"] == "animated"
        # Snake_case keys, not protojson camelCase.
        assert obj["duration_seconds"] == 6
        assert obj["fps"] == 10
        assert obj["start_offsets"] == [1.5, 4, 9.25]
        assert "durationSeconds" not in obj
        assert "startOffsets" not in obj

    def test_round_trips_expanding_the_enum(self) -> None:
        original = thumbnails_pb2.ThumbnailSpec(
            mode=thumbnails_pb2.THUMBNAIL_MODE_ANIMATED,
            duration_seconds=4,
            fps=12,
            start_offsets=[0, 2.5],
        )
        decoded = deserialize(serialize(original), thumbnails_pb2.ThumbnailSpec())
        assert decoded.mode == thumbnails_pb2.THUMBNAIL_MODE_ANIMATED
        assert decoded.duration_seconds == 4
        assert decoded.fps == 12
        assert list(decoded.start_offsets) == [0, 2.5]

    def test_fill_from_dict_accepts_simplified_animated_kwargs(self) -> None:
        # The ergonomic kwarg path: simplified "animated" string expands to the
        # canonical enum and the snake_case scalars land on the message.
        spec = fill_from_dict(
            thumbnails_pb2.ThumbnailSpec(),
            {"mode": "animated", "duration_seconds": 6, "fps": 10, "start_offsets": [1.0, 3.0]},
        )
        assert spec.mode == thumbnails_pb2.THUMBNAIL_MODE_ANIMATED
        assert spec.duration_seconds == 6
        assert spec.fps == 10
        assert list(spec.start_offsets) == [1.0, 3.0]


class TestVideoHoverPreviewURLs:
    def test_hover_preview_urls_parse_from_snake_case_wire(self) -> None:
        payload = json.dumps(
            {
                "video": {
                    "id": "vid_abc",
                    "hover_preview_url": "https://cdn.example.com/p.webp",
                    "hover_preview_mp4_url": "https://cdn.example.com/p.mp4",
                }
            }
        ).encode()
        resp = deserialize(payload, video_pb2.GetVideoResponse())
        assert resp.video.hover_preview_url == "https://cdn.example.com/p.webp"
        assert resp.video.hover_preview_mp4_url == "https://cdn.example.com/p.mp4"


class TestCreateUploadHoverPreviews:
    def test_hover_previews_toggle_serializes_snake_case(self) -> None:
        req = fill_from_dict(
            video_pb2.CreateUploadRequest(),
            {"filename": "clip.mp4", "hover_previews": True},
        )
        assert req.hover_previews is True
        obj = json.loads(serialize(req).decode())
        assert obj["hover_previews"] is True
        assert "hoverPreviews" not in obj
