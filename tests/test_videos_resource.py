"""Tests for the Videos resource: create_from_url + playback analytics.

``create_from_url`` is the one-call URL-ingest RPC — no upload step.
``get_stats`` / ``list_top_videos`` are the playback-analytics RPCs. Mirrors
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


def _capture_get_stats(**kwargs: Any) -> video_pb2.GetStatsRequest:
    """Run ``Videos.get_stats(**kwargs)`` and return the request sent to the wire."""
    t = FakeTransport({"GetStats": video_pb2.GetStatsResponse()})
    Videos(t).get_stats(**kwargs)  # type: ignore[arg-type]
    return t.calls[0][1]


class TestVideosGetStats:
    def test_required_video_id(self) -> None:
        req = _capture_get_stats(video_id="vid_abc123def456")
        assert req.video_id == "vid_abc123def456"
        # Unset optional date bounds stay empty (proto3 string default).
        assert req.start_date == ""
        assert req.end_date == ""

    def test_optional_date_range(self) -> None:
        req = _capture_get_stats(
            video_id="vid_abc123def456",
            start_date="2026-07-01",
            end_date="2026-07-16",
        )
        assert req.start_date == "2026-07-01"
        assert req.end_date == "2026-07-16"

    def test_returns_full_response_with_daily_and_totals(self) -> None:
        # GetStatsResponse carries both daily rows and range totals — the method
        # returns the whole response (matching get_usage), not a single field.
        resp = video_pb2.GetStatsResponse(
            daily=[
                video_pb2.VideoStatsDay(
                    date="2026-07-15", plays=10, watch_seconds=1200, unique_viewers=7
                ),
                video_pb2.VideoStatsDay(
                    date="2026-07-16", plays=4, watch_seconds=480, unique_viewers=3
                ),
            ],
            totals=video_pb2.VideoStatsTotals(plays=14, watch_seconds=1680, unique_viewers=10),
        )
        t = FakeTransport({"GetStats": resp})
        out = Videos(t).get_stats(video_id="vid_abc123def456")  # type: ignore[arg-type]
        assert isinstance(out, video_pb2.GetStatsResponse)
        assert [d.date for d in out.daily] == ["2026-07-15", "2026-07-16"]
        assert out.daily[0].plays == 10
        assert out.daily[0].watch_seconds == 1200
        assert out.daily[0].unique_viewers == 7
        assert out.totals.plays == 14
        assert out.totals.watch_seconds == 1680
        assert out.totals.unique_viewers == 10

    def test_sends_get_stats_method(self) -> None:
        t = FakeTransport({"GetStats": video_pb2.GetStatsResponse()})
        Videos(t).get_stats(video_id="vid_abc123def456")  # type: ignore[arg-type]
        assert t.calls[0][0] == "GetStats"


def _capture_list_top_videos(**kwargs: Any) -> video_pb2.ListTopVideosRequest:
    """Run ``Videos.list_top_videos(**kwargs)`` and return the request sent to the wire."""
    t = FakeTransport({"ListTopVideos": video_pb2.ListTopVideosResponse()})
    Videos(t).list_top_videos(**kwargs)  # type: ignore[arg-type]
    return t.calls[0][1]


class TestVideosListTopVideos:
    def test_no_kwargs_sends_empty_request(self) -> None:
        # app_id is optional (API-key callers may omit it); an empty request is
        # valid and resolves the app server-side.
        req = _capture_list_top_videos()
        assert req.app_id == ""
        assert req.limit == 0  # unset int32 default

    def test_app_id_and_limit(self) -> None:
        req = _capture_list_top_videos(app_id="app_k1l2m3n4o5", limit=25)
        assert req.app_id == "app_k1l2m3n4o5"
        assert req.limit == 25

    def test_optional_date_range(self) -> None:
        req = _capture_list_top_videos(
            app_id="app_k1l2m3n4o5",
            start_date="2026-07-01",
            end_date="2026-07-16",
        )
        assert req.start_date == "2026-07-01"
        assert req.end_date == "2026-07-16"

    def test_returns_full_response_with_items(self) -> None:
        # ListTopVideos is not paginated (no page_token) — the method returns the
        # whole ListTopVideosResponse, whose `items` is the ranked leaderboard.
        resp = video_pb2.ListTopVideosResponse(
            items=[
                video_pb2.TopVideo(
                    video_id="vid_top1",
                    title="Most watched",
                    poster_url="https://cdn.example.com/vid_top1/poster.jpg",
                    plays=500,
                    watch_seconds=60000,
                    unique_viewers=320,
                ),
                video_pb2.TopVideo(video_id="vid_top2", plays=210, watch_seconds=25000),
            ]
        )
        t = FakeTransport({"ListTopVideos": resp})
        out = Videos(t).list_top_videos(app_id="app_k1l2m3n4o5")  # type: ignore[arg-type]
        assert isinstance(out, video_pb2.ListTopVideosResponse)
        assert [v.video_id for v in out.items] == ["vid_top1", "vid_top2"]
        assert out.items[0].title == "Most watched"
        assert out.items[0].poster_url == "https://cdn.example.com/vid_top1/poster.jpg"
        assert out.items[0].plays == 500
        assert out.items[0].watch_seconds == 60000
        assert out.items[0].unique_viewers == 320
        # Unset optional title/poster on the second row are empty strings.
        assert out.items[1].title == ""
        assert out.items[1].poster_url == ""

    def test_sends_list_top_videos_method(self) -> None:
        t = FakeTransport({"ListTopVideos": video_pb2.ListTopVideosResponse()})
        Videos(t).list_top_videos(app_id="app_k1l2m3n4o5")  # type: ignore[arg-type]
        assert t.calls[0][0] == "ListTopVideos"
