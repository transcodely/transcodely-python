"""Tests for the 5.45.0 resync: the free captions trial.

Pins the ``FreeTrial`` wire shape, the ``videos.get_free_trial`` facade call and
the ``transcodely.types`` exports. Mirror of the TS / Go tests.
"""

from __future__ import annotations

import json
from typing import Any

import transcodely
from transcodely._codec.json_codec import deserialize, serialize
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


def test_get_free_trial_unavailable_returns_trial() -> None:
    resp = deserialize(
        json.dumps(
            {
                "free_trial": {
                    "status": "unavailable",
                    "unavailable_reason": "daily_limit",
                    "max_duration_seconds": 300,
                    "max_upload_bytes": "1073741824",
                }
            }
        ).encode(),
        video_pb2.GetFreeTrialResponse(),
    )
    t = _FakeTransport(resp)
    trial = Videos(t).get_free_trial()  # type: ignore[arg-type]
    method, req = t.calls[0]
    assert method == "GetFreeTrial"
    assert isinstance(req, transcodely.types.GetFreeTrialRequest)
    assert trial is resp.free_trial
    assert trial.status == transcodely.types.FreeTrialStatus.Value("FREE_TRIAL_STATUS_UNAVAILABLE")
    assert trial.unavailable_reason == transcodely.types.FreeTrialUnavailableReason.Value(
        "FREE_TRIAL_UNAVAILABLE_REASON_DAILY_LIMIT"
    )
    assert trial.max_duration_seconds == 300
    assert trial.max_upload_bytes == 1073741824


def test_get_free_trial_used_carries_video_id() -> None:
    resp = deserialize(
        json.dumps({"free_trial": {"status": "used", "video_id": "vid_a1b2c3d4e5f6g7"}}).encode(),
        video_pb2.GetFreeTrialResponse(),
    )
    trial = Videos(_FakeTransport(resp)).get_free_trial()  # type: ignore[arg-type]
    assert trial.status == transcodely.types.FreeTrialStatus.Value("FREE_TRIAL_STATUS_USED")
    assert trial.video_id == "vid_a1b2c3d4e5f6g7"
    assert not trial.HasField("unavailable_reason")


def test_free_trial_options_round_trip_on_create_requests() -> None:
    req = video_pb2.CreateUploadRequest(
        free_trial=transcodely.types.FreeTrialOptions(source_duration_seconds=612.5)
    )
    wire = json.loads(serialize(req).decode())
    assert wire["free_trial"] == {"source_duration_seconds": 612.5}
    back = deserialize(serialize(req), video_pb2.CreateUploadRequest())
    assert back.free_trial.source_duration_seconds == 612.5


def test_free_trial_types_exported() -> None:
    for name in (
        "FreeTrial",
        "FreeTrialOptions",
        "FreeTrialStatus",
        "FreeTrialUnavailableReason",
        "VideoFreeTrial",
        "GetFreeTrialRequest",
        "GetFreeTrialResponse",
    ):
        assert name in transcodely.types.__all__
        assert hasattr(transcodely.types, name)
