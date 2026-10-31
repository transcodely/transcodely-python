"""Video resource — uploads, get/list/update/delete, watch, usage."""

from __future__ import annotations

import builtins
from collections.abc import Generator
from typing import Any

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..streaming import watch
from ..v1 import subtitles_pb2, video_pb2
from ._helpers import fill_from_dict

_SERVICE = "transcodely.v1.VideoService"


class Videos:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create_upload(self, **kwargs: Any) -> video_pb2.CreateUploadResponse:
        req = fill_from_dict(video_pb2.CreateUploadRequest(), kwargs)
        return self._t.unary(_SERVICE, "CreateUpload", req, video_pb2.CreateUploadResponse())

    def complete_upload(self, **kwargs: Any) -> video_pb2.CompleteUploadResponse:
        req = fill_from_dict(video_pb2.CompleteUploadRequest(), kwargs)
        return self._t.unary(_SERVICE, "CompleteUpload", req, video_pb2.CompleteUploadResponse())

    def create_from_url(self, **kwargs: Any) -> video_pb2.Video:
        """One-call video ingest from a publicly-reachable http(s) URL.

        No upload step: the API records the video in "processing" and hands
        the URL to the transcoding pipeline. Returns the ``Video`` directly
        (``CreateFromUrlResponse`` carries nothing else) — playback/embed
        URLs populate once it reaches "ready" (watch it or subscribe to
        ``video.ready``).
        """
        req = fill_from_dict(video_pb2.CreateFromUrlRequest(), kwargs)
        return self._t.unary(
            _SERVICE, "CreateFromUrl", req, video_pb2.CreateFromUrlResponse()
        ).video

    def create_multipart_upload(self, **kwargs: Any) -> video_pb2.CreateMultipartUploadResponse:
        req = fill_from_dict(video_pb2.CreateMultipartUploadRequest(), kwargs)
        return self._t.unary(
            _SERVICE,
            "CreateMultipartUpload",
            req,
            video_pb2.CreateMultipartUploadResponse(),
        )

    def get_upload_part_urls(self, **kwargs: Any) -> video_pb2.GetUploadPartUrlsResponse:
        req = fill_from_dict(video_pb2.GetUploadPartUrlsRequest(), kwargs)
        return self._t.unary(
            _SERVICE, "GetUploadPartUrls", req, video_pb2.GetUploadPartUrlsResponse()
        )

    def complete_multipart_upload(self, **kwargs: Any) -> video_pb2.CompleteMultipartUploadResponse:
        req = fill_from_dict(video_pb2.CompleteMultipartUploadRequest(), kwargs)
        return self._t.unary(
            _SERVICE,
            "CompleteMultipartUpload",
            req,
            video_pb2.CompleteMultipartUploadResponse(),
        )

    def abort_multipart_upload(self, **kwargs: Any) -> video_pb2.AbortMultipartUploadResponse:
        req = fill_from_dict(video_pb2.AbortMultipartUploadRequest(), kwargs)
        return self._t.unary(
            _SERVICE,
            "AbortMultipartUpload",
            req,
            video_pb2.AbortMultipartUploadResponse(),
        )

    def get(self, id: str, opts: CallOptions | None = None) -> video_pb2.Video:
        req = video_pb2.GetVideoRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, video_pb2.GetVideoResponse(), opts).video

    def list(
        self,
        *,
        page_size: int | None = None,
        status: str | None = None,
        opts: CallOptions | None = None,
    ) -> Page[video_pb2.Video]:
        def fetch(cursor: str | None) -> PageContents[video_pb2.Video]:
            req = video_pb2.ListVideosRequest()
            if page_size is not None:
                req.page_size = page_size
            if status is not None:
                req.status = status
            if cursor is not None:
                req.page_token = cursor
            res = self._t.unary(_SERVICE, "List", req, video_pb2.ListVideosResponse(), opts)
            return PageContents(items=list(res.videos), next_cursor=res.next_page_token or None)

        return Page(fetch)

    def update(self, **kwargs: Any) -> video_pb2.Video:
        req = fill_from_dict(video_pb2.UpdateVideoRequest(), kwargs)
        return self._t.unary(_SERVICE, "Update", req, video_pb2.UpdateVideoResponse()).video

    def delete(self, id: str, opts: CallOptions | None = None) -> None:
        req = video_pb2.DeleteVideoRequest(id=id)
        self._t.unary(_SERVICE, "Delete", req, video_pb2.DeleteVideoResponse(), opts)

    def watch(
        self,
        id: str,
        *,
        include_heartbeats: bool = False,
        max_reconnects: int = 5,
        opts: CallOptions | None = None,
    ) -> Generator[video_pb2.WatchVideoResponse, None, None]:
        def factory() -> Generator[video_pb2.WatchVideoResponse, None, None]:
            req = video_pb2.WatchVideoRequest(id=id)
            yield from self._t.stream(_SERVICE, "Watch", req, video_pb2.WatchVideoResponse, opts)

        yield from watch(
            factory,
            is_heartbeat=lambda e: getattr(e, "event", "") == "heartbeat",
            include_heartbeats=include_heartbeats,
            max_reconnects=max_reconnects,
        )

    def get_usage(self, **kwargs: Any) -> video_pb2.GetUsageResponse:
        req = fill_from_dict(video_pb2.GetUsageRequest(), kwargs)
        return self._t.unary(_SERVICE, "GetUsage", req, video_pb2.GetUsageResponse())

    def get_stats(self, **kwargs: Any) -> video_pb2.GetStatsResponse:
        """Playback analytics for a single video: plays, watch time, and unique
        viewers per UTC day, plus range totals.

        Pass ``video_id`` (required) and optional ``start_date`` / ``end_date``
        (inclusive, ``YYYY-MM-DD``). Returns the full ``GetStatsResponse`` —
        ``.daily`` holds per-day rows (oldest first, activity-only, no zero-fill)
        and ``.totals`` the range aggregate. Stats are best-effort and roll up
        hourly, so recent activity can lag by up to an hour.
        """
        req = fill_from_dict(video_pb2.GetStatsRequest(), kwargs)
        return self._t.unary(_SERVICE, "GetStats", req, video_pb2.GetStatsResponse())

    def list_top_videos(self, **kwargs: Any) -> video_pb2.ListTopVideosResponse:
        """An app's top videos ranked by plays over a date range.

        Optional kwargs: ``app_id`` (API-key callers may omit it — their key's
        app is used), ``start_date`` / ``end_date`` (inclusive, ``YYYY-MM-DD``),
        and ``limit`` (1-100, default 10). Returns the full
        ``ListTopVideosResponse`` — ``.items`` is the ranked list of
        ``TopVideo`` rows (by plays, then watch time, descending).
        """
        req = fill_from_dict(video_pb2.ListTopVideosRequest(), kwargs)
        return self._t.unary(_SERVICE, "ListTopVideos", req, video_pb2.ListTopVideosResponse())

    def get_seo_markup(self, **kwargs: Any) -> video_pb2.GetSeoMarkupResponse:
        """Ready-to-paste SEO markup for a hosted video, built for YOUR watch page.

        Pass ``video_id`` and ``watch_url`` (required; the absolute ``https://``
        URL of the page that shows the video), plus optional ``deep_link_param``
        (query parameter your page reads to start at a time, default ``"t"``)
        and ``language`` (ISO 639-2, when the video has several transcripts).
        Returns the full ``GetSeoMarkupResponse``: ``.json_ld`` (schema.org
        VideoObject, with chapter Clip key moments when insights are ready),
        ``.sitemap_entry`` (a video-sitemap ``<url>`` entry) and
        ``.html_fragment`` (server-renderable summary, key points, chapter links
        and the full transcript). Every string is escaped for its context;
        paste it as-is.
        """
        req = fill_from_dict(video_pb2.GetSeoMarkupRequest(), kwargs)
        return self._t.unary(_SERVICE, "GetSeoMarkup", req, video_pb2.GetSeoMarkupResponse())

    def generate_insights(self, **kwargs: Any) -> subtitles_pb2.TranscriptInsights:
        """Generate AI insights from a hosted video's existing AI captions.

        Runs the insights pass (title suggestions, summary, key points,
        chapters, questions, key terms, highlights, topics) without
        transcribing again. Pass ``id`` (the ``vid_...`` video, required), plus
        optional ``language`` (ISO 639-2; needed only when the video has several
        AI caption tracks), ``hint`` (free-text guidance, at most 300
        characters) and ``app_id``. Returns the ``TranscriptInsights`` entry in
        ``"pending"``; it also appears on ``video.insights``, and
        ``video.insights.ready`` or ``video.insights.failed`` fires when it
        finishes. Billed EUR 0.02 per video plus EUR 0.005 per minute of source,
        charged only when the insights become ready.

        While an entry for the same video and language is pending, the call
        returns that entry and bills nothing new. A video without AI captions is
        refused with failed_precondition (code ``captions_required``).
        """
        req = fill_from_dict(video_pb2.GenerateInsightsRequest(), kwargs)
        return self._t.unary(
            _SERVICE, "GenerateInsights", req, video_pb2.GenerateInsightsResponse()
        ).insights

    def generate_highlights(self, **kwargs: Any) -> builtins.list[video_pb2.VideoHighlight]:
        """Cut highlight clips from a hosted video around its insights' quotes.

        Pass ``id`` (the ``vid_...`` video, required), plus optional
        ``language`` (ISO 639-2; needed only when the video has ready insights
        in several languages), ``config`` (a dict or ``HighlightsConfig``:
        ``max_count`` 1-10, default 5; ``min_seconds`` default 8;
        ``max_seconds`` default 60; ``padding_seconds`` default 1.5) and
        ``app_id``. Returns the highlights in ``"pending"``; they also appear on
        ``video.highlights``, and ``video.highlights.ready`` (or
        ``video.highlights.failed``, when none could be rendered) fires once
        every one has finished.

        Each clip is its own clip job on the video, billed as its rendered
        (clipped) minutes at your effective encoding rate, with no processing
        fee. While any highlight of the video is pending, the call returns the
        current set and bills nothing new; once all are ready or failed, a new
        call replaces them. A video without ready insights is refused with
        failed_precondition (code ``highlights_require_insights``).
        """
        req = fill_from_dict(video_pb2.GenerateHighlightsRequest(), kwargs)
        return list(
            self._t.unary(
                _SERVICE, "GenerateHighlights", req, video_pb2.GenerateHighlightsResponse()
            ).highlights
        )
