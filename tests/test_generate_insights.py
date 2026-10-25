"""Wire-shape tests for GenerateInsights and the video-sourced insights fields.

Pins the request as snake_case with optional fields off the wire when unset, and
the new ``TranscriptInsights`` fields (``id``, lowercase ``source``,
``video_id``, ``fee_eur``) in both directions. Mirror of the TS / Go tests.
"""

from __future__ import annotations

import json

from transcodely._codec.json_codec import deserialize, serialize
from transcodely.resources._helpers import fill_from_dict
from transcodely.v1 import subtitles_pb2, video_pb2


def test_request_serializes_snake_case() -> None:
    req = fill_from_dict(
        video_pb2.GenerateInsightsRequest(),
        {"id": "vid_abc", "language": "eng", "hint": "for beginners", "app_id": "app_abc"},
    )
    obj = json.loads(serialize(req).decode())
    assert obj == {"id": "vid_abc", "language": "eng", "hint": "for beginners", "app_id": "app_abc"}


def test_request_omits_unset_optionals() -> None:
    req = fill_from_dict(video_pb2.GenerateInsightsRequest(), {"id": "vid_abc"})
    obj = json.loads(serialize(req).decode())
    assert obj == {"id": "vid_abc"}


def test_response_decodes_video_sourced_entry() -> None:
    body = json.dumps(
        {
            "insights": {
                "id": "ins_abc123",
                "source": "video",
                "video_id": "vid_abc",
                "language": "eng",
                "status": "pending",
                "fee_eur": 0.07,
            }
        }
    ).encode()
    resp = deserialize(body, video_pb2.GenerateInsightsResponse())
    ins = resp.insights
    assert ins.id == "ins_abc123"
    assert ins.source == subtitles_pb2.INSIGHTS_SOURCE_VIDEO
    assert ins.video_id == "vid_abc"
    assert ins.status == subtitles_pb2.INSIGHTS_STATUS_PENDING
    assert ins.HasField("fee_eur")
    assert ins.fee_eur == 0.07


def test_source_enum_is_lowercase_on_the_wire() -> None:
    for value, wire in (
        (subtitles_pb2.INSIGHTS_SOURCE_JOB, "job"),
        (subtitles_pb2.INSIGHTS_SOURCE_VIDEO, "video"),
    ):
        obj = json.loads(serialize(subtitles_pb2.TranscriptInsights(source=value)).decode())
        assert obj["source"] == wire
        # A job-sourced (or unset) fee stays off the wire.
        assert "fee_eur" not in obj
