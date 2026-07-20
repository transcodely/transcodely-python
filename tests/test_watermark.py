"""Tests for the watermark / logo overlay wire format.

These pin the Transcodely wire format for the watermark config that rides inside
an ``OutputSpec``: snake_case field names + a simplified lowercase anchor enum
(``"bottom_right"``). They mirror the Go / TS watermark codec tests.
"""

from __future__ import annotations

import json

from transcodely._codec.json_codec import deserialize, serialize
from transcodely.v1 import common_pb2, job_pb2, watermark_pb2


class TestWatermarkWireFormat:
    def test_serializes_relative_mode_with_snake_case_and_lowercase_anchor(self) -> None:
        req = job_pb2.CreateJobRequest(
            input_url="https://example.com/in.mp4",
            outputs=[
                job_pb2.OutputSpec(
                    type=common_pb2.OUTPUT_FORMAT_HLS,
                    watermark=watermark_pb2.WatermarkConfig(
                        image_url="https://cdn.example.com/logo.png",
                        anchor=watermark_pb2.WATERMARK_ANCHOR_BOTTOM_RIGHT,
                        width_pct=15,
                        margin_pct=2,
                        opacity=0.8,
                    ),
                )
            ],
        )
        obj = json.loads(serialize(req).decode())
        wm = obj["outputs"][0]["watermark"]
        assert wm["image_url"] == "https://cdn.example.com/logo.png"
        assert wm["anchor"] == "bottom_right"
        assert wm["width_pct"] == 15
        assert wm["margin_pct"] == 2
        assert wm["opacity"] == 0.8
        # No camelCase keys must leak onto the wire.
        assert "imageUrl" not in wm
        assert "widthPct" not in wm
        assert "marginPct" not in wm
        # The verbose enum form must never reach the wire.
        assert wm["anchor"] != "WATERMARK_ANCHOR_BOTTOM_RIGHT"

    def test_serializes_pixel_mode_with_snake_case_placement(self) -> None:
        req = job_pb2.CreateJobRequest(
            input_url="https://example.com/in.mp4",
            outputs=[
                job_pb2.OutputSpec(
                    type=common_pb2.OUTPUT_FORMAT_MP4,
                    watermark=watermark_pb2.WatermarkConfig(
                        image_url="https://cdn.example.com/logo.png",
                        opacity=1,
                        pixel=watermark_pb2.WatermarkPixelPlacement(x=40, y=40, width=240),
                    ),
                )
            ],
        )
        obj = json.loads(serialize(req).decode())
        wm = obj["outputs"][0]["watermark"]
        assert wm["image_url"] == "https://cdn.example.com/logo.png"
        assert wm["pixel"] == {"x": 40, "y": 40, "width": 240}
        # Relative-mode anchor is unset in pixel mode and must be omitted.
        assert "anchor" not in wm

    def test_round_trips_relative_mode_preserving_anchor_enum(self) -> None:
        original = job_pb2.CreateJobRequest(
            input_url="https://example.com/in.mp4",
            outputs=[
                job_pb2.OutputSpec(
                    type=common_pb2.OUTPUT_FORMAT_HLS,
                    watermark=watermark_pb2.WatermarkConfig(
                        image_url="https://cdn.example.com/logo.webp",
                        anchor=watermark_pb2.WATERMARK_ANCHOR_TOP_LEFT,
                        width_pct=12.5,
                    ),
                )
            ],
        )
        decoded = deserialize(serialize(original), job_pb2.CreateJobRequest())
        wm = decoded.outputs[0].watermark
        assert wm.image_url == "https://cdn.example.com/logo.webp"
        assert wm.anchor == watermark_pb2.WATERMARK_ANCHOR_TOP_LEFT
        assert wm.width_pct == 12.5


class TestWatermarkFacadeExports:
    """The watermark types surface at the flat facade paths, matching how
    other feature configs (DRMConfig, SubtitleTrack) are re-exported."""

    def test_types_module_reexports(self) -> None:
        from transcodely.types import (
            WatermarkAnchor,
            WatermarkConfig,
            WatermarkPixelPlacement,
        )

        assert WatermarkConfig is watermark_pb2.WatermarkConfig
        assert WatermarkPixelPlacement is watermark_pb2.WatermarkPixelPlacement
        assert WatermarkAnchor is watermark_pb2.WatermarkAnchor

    def test_watermark_config_is_a_top_level_export(self) -> None:
        import transcodely

        assert transcodely.WatermarkConfig is watermark_pb2.WatermarkConfig
        assert "WatermarkConfig" in transcodely.__all__
