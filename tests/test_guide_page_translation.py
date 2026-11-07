"""Tests for the 5.38.0 resync: guide page and caption translation.

Pins ``guide_page`` as the lowercase ``GuidePageSetting`` value in both
directions, ``guide_page_enabled`` as an optional that stays unset when a
webhook-shaped payload omits it, ``HostingConfig.guide_pages_enabled``, the
``TranslateCaptions`` request/response, the facade call, and the translation
fields on tracks and the create requests. Mirror of the TS / Go tests.
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


# ---------------------------------------------------------------- guide page


def test_webhook_shaped_video_has_guide_page_but_no_effective_flag() -> None:
    # video.* webhook payloads never carry guide_page_enabled (the snapshot
    # does not resolve the app default); the optional must stay unset.
    video = deserialize(
        json.dumps({"id": "vid_abc", "guide_page": "on"}).encode(), video_pb2.Video()
    )
    assert video.guide_page == video_pb2.GUIDE_PAGE_SETTING_ON
    assert not video.HasField("guide_page_enabled")
    assert not video.HasField("guide_url")


def test_api_shaped_video_decodes_effective_value_and_url() -> None:
    body = json.dumps(
        {
            "id": "vid_abc",
            "guide_page": "default",
            "guide_page_enabled": True,
            "guide_url": "https://play.example/v/vid_abc/guide",
        }
    ).encode()
    video = deserialize(body, video_pb2.Video())
    assert video.guide_page == video_pb2.GUIDE_PAGE_SETTING_DEFAULT
    assert video.HasField("guide_page_enabled") and video.guide_page_enabled is True
    assert video.guide_url == "https://play.example/v/vid_abc/guide"


def test_update_request_serializes_guide_page_lowercase() -> None:
    req = fill_from_dict(video_pb2.UpdateVideoRequest(), {"id": "vid_abc", "guide_page": "off"})
    assert req.guide_page == video_pb2.GUIDE_PAGE_SETTING_OFF
    obj = json.loads(serialize(req).decode())
    assert obj["guide_page"] == "off"
    assert "guide_page_enabled" not in obj

    obj = json.loads(serialize(video_pb2.UpdateVideoRequest(id="vid_abc")).decode())
    assert "guide_page" not in obj


def test_hosting_config_guide_pages_enabled() -> None:
    obj = json.loads(serialize(app_pb2.HostingConfig(guide_pages_enabled=True)).decode())
    assert obj["guide_pages_enabled"] is True
    assert "guide_pages_enabled" not in json.loads(serialize(app_pb2.HostingConfig()).decode())


def test_guide_page_setting_is_exported() -> None:
    assert transcodely.GuidePageSetting is video_pb2.GuidePageSetting
    assert (
        transcodely.types.GuidePageSetting.Value("GUIDE_PAGE_SETTING_ON")
        == video_pb2.GUIDE_PAGE_SETTING_ON
    )


# -------------------------------------------------------- caption translation


def test_translate_request_serializes_snake_case() -> None:
    req = fill_from_dict(
        video_pb2.TranslateCaptionsRequest(),
        {
            "id": "vid_abc",
            "source_language": "eng",
            "target_languages": ["ger", "spa"],
            "include_insights": False,
        },
    )
    obj = json.loads(serialize(req).decode())
    assert obj == {
        "id": "vid_abc",
        "source_language": "eng",
        "target_languages": ["ger", "spa"],
        "include_insights": False,
    }


def test_translate_response_decodes() -> None:
    body = json.dumps(
        {
            "job_id": "job_a1b2c3d4e5f6",
            "video_id": "vid_abc",
            "source_language": "eng",
            "target_languages": ["ger"],
            "in_flight": [{"language": "spa", "job_id": "job_f6e5d4c3b2a1"}],
            "estimated_fee_eur": 0.36,
            "insights_included": True,
        }
    ).encode()
    res = deserialize(body, video_pb2.TranslateCaptionsResponse())
    assert res.job_id == "job_a1b2c3d4e5f6"
    assert list(res.target_languages) == ["ger"]
    assert [(f.language, f.job_id) for f in res.in_flight] == [("spa", "job_f6e5d4c3b2a1")]
    assert res.estimated_fee_eur == 0.36
    assert res.insights_included is True


def test_translate_captions_facade_sends_request_and_returns_response() -> None:
    resp = video_pb2.TranslateCaptionsResponse(
        job_id="job_a1b2c3d4e5f6",
        video_id="vid_a1b2c3d4e5f6g7",
        source_language="eng",
        target_languages=["ger"],
        in_flight=[video_pb2.TranslationInFlight(language="spa", job_id="job_f6e5d4c3b2a1")],
        estimated_fee_eur=0.36,
        insights_included=True,
    )
    t = _FakeTransport(resp)
    out = Videos(t).translate_captions(  # type: ignore[arg-type]
        id="vid_a1b2c3d4e5f6g7", target_languages=["deu", "spa"], include_insights=False
    )
    method, req = t.calls[0]
    assert method == "TranslateCaptions"
    assert isinstance(req, video_pb2.TranslateCaptionsRequest)
    assert req.id == "vid_a1b2c3d4e5f6g7"
    assert list(req.target_languages) == ["deu", "spa"]
    assert req.HasField("include_insights") and req.include_insights is False
    assert not req.HasField("source_language")
    assert not req.HasField("app_id")
    assert out is resp
    assert out.in_flight[0].language == "spa"
    assert isinstance(out.in_flight[0], transcodely.TranslationInFlight)


def test_translation_fields_on_tracks() -> None:
    obj = json.loads(serialize(subtitles_pb2.SubtitleTrack(translations=["ger", "spa"])).decode())
    assert obj["translations"] == ["ger", "spa"]

    track = deserialize(
        json.dumps({"id": "trk_abc", "language": "ger", "translated_from": "eng"}).encode(),
        video_pb2.VideoTextTrack(),
    )
    assert track.translated_from == "eng"

    result = deserialize(
        json.dumps({"language": "ger", "translated_from": "eng"}).encode(),
        subtitles_pb2.SubtitleResult(),
    )
    assert result.translated_from == "eng"


_REQUESTS: list[tuple[Any, dict[str, Any]]] = [
    (video_pb2.CreateUploadRequest, {"filename": "clip.mp4"}),
    (video_pb2.CreateFromUrlRequest, {"url": "https://example.com/a.mp4"}),
    (video_pb2.CreateMultipartUploadRequest, {"filename": "big.mp4"}),
]


@pytest.mark.parametrize(("cls", "base"), _REQUESTS)
def test_create_auto_translations_serializes(cls: Any, base: dict[str, Any]) -> None:
    req = fill_from_dict(cls(), {**base, "auto_captions": True, "auto_translations": ["ger"]})
    obj = json.loads(serialize(req).decode())
    assert obj["auto_translations"] == ["ger"]
    # The codec emits unpopulated repeated fields, so an unset list rides as [].
    assert json.loads(serialize(fill_from_dict(cls(), base)).decode())["auto_translations"] == []
