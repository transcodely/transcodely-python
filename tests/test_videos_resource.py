"""Tests for the Videos resource: create_from_url request construction.

``create_from_url`` is the one-call URL-ingest RPC — no upload step. Mirrors
test_apps_resource.py / test_jobs_resource.py: request construction verified
against a duck-typed FakeTransport (no live server).
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

from transcodely.resources.videos import Videos
from transcodely.v1 import video_pb2


class FakeTransport:
    """Duck-typed stand-in for Transport that returns canned responses per method."""

    def __init__(self, responses: dict[str, Union[Any, Callable[[Any], Any]]]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self,
        service_name: str,
        method_name: str,
        request: Any,
        response: Any,
        opts: Optional[Any] = None,
    ) -> Any:
        self.calls.append((method_name, request))
        r = self._responses[method_name]
        return r(request) if callable(r) else r


def _capture_create_from_url(**kwargs: Any) -> video_pb2.CreateFromUrlRequest:
    """Run ``Videos.create_from_url(**kwargs)`` and return the request sent to the wire."""
    resp = video_pb2.CreateFromUrlResponse(
        video=video_pb2.Video(id="vid_created", status="processing")
    )
    t = FakeTransport({"CreateFromUrl": resp})
    Videos(t).create_from_url(**kwargs)  # type: ignore[arg-type]
    return t.calls[0][1]


class TestVideosCreateFromUrl:
    def test_required_fields(self) -> None:
        req = _capture_create_from_url(
            app_id="app_default000", url="https://example.com/source.mp4"
        )
        assert req.app_id == "app_default000"
        assert req.url == "https://example.com/source.mp4"

    def test_optional_title_and_description(self) -> None:
        req = _capture_create_from_url(
            app_id="app_default000",
            url="https://example.com/source.mp4",
            title="Product demo",
            description="Q3 launch clip",
        )
        assert req.title == "Product demo"
        assert req.description == "Q3 launch clip"

    def test_tags(self) -> None:
        req = _capture_create_from_url(
            app_id="app_default000",
            url="https://example.com/source.mp4",
            tags=["marketing", "launch"],
        )
        assert list(req.tags) == ["marketing", "launch"]

    def test_visibility(self) -> None:
        req = _capture_create_from_url(
            app_id="app_default000",
            url="https://example.com/source.mp4",
            visibility="public",
        )
        assert req.visibility == "public"

    def test_preset_reference(self) -> None:
        req = _capture_create_from_url(
            app_id="app_default000",
            url="https://example.com/source.mp4",
            preset="pst_x9y8z7w6v5",
        )
        assert req.preset == "pst_x9y8z7w6v5"

    def test_all_kwargs_together(self) -> None:
        req = _capture_create_from_url(
            app_id="app_default000",
            url="https://example.com/source.mp4",
            title="Product demo",
            description="Q3 launch clip",
            tags=["marketing"],
            visibility="unlisted",
            preset="web_720p_standard",
        )
        assert req.app_id == "app_default000"
        assert req.url == "https://example.com/source.mp4"
        assert req.title == "Product demo"
        assert req.description == "Q3 launch clip"
        assert list(req.tags) == ["marketing"]
        assert req.visibility == "unlisted"
        assert req.preset == "web_720p_standard"

    def test_returns_video_unwrapped_from_response(self) -> None:
        # CreateFromUrlResponse carries nothing but `video` — the method returns
        # the Video directly, matching apps.create/origins.create/presets.create
        # (not the videos.create_upload style, whose response also carries an
        # upload_url/upload_expires_at the caller needs).
        t = FakeTransport(
            {
                "CreateFromUrl": video_pb2.CreateFromUrlResponse(
                    video=video_pb2.Video(id="vid_abc", status="processing")
                )
            }
        )
        video = Videos(t).create_from_url(  # type: ignore[arg-type]
            app_id="app_default000", url="https://example.com/source.mp4"
        )
        assert isinstance(video, video_pb2.Video)
        assert video.id == "vid_abc"
        assert video.status == "processing"

    def test_conflicting_scheme_not_validated_client_side(self) -> None:
        # Thin client: the SDK forwards whatever URL it's given and lets the
        # server's protovalidate pattern (^https?://.*$) reject gs://, s3://,
        # etc. rather than raising locally.
        req = _capture_create_from_url(app_id="app_default000", url="gs://bucket/in.mp4")
        assert req.url == "gs://bucket/in.mp4"
