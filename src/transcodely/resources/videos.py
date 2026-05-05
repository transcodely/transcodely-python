"""Video resource — uploads, get/list/update/delete, watch, usage."""

from __future__ import annotations

from typing import Any, Generator, Mapping, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..streaming import watch
from ..v1 import video_pb2
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
        return self._t.unary(_SERVICE, "GetUploadPartUrls", req, video_pb2.GetUploadPartUrlsResponse())

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

    def get(self, id: str, opts: Optional[CallOptions] = None) -> video_pb2.Video:
        req = video_pb2.GetVideoRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, video_pb2.GetVideoResponse(), opts).video

    def list(
        self,
        *,
        page_size: Optional[int] = None,
        status: Optional[str] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[video_pb2.Video]:
        def fetch(cursor: Optional[str]) -> PageContents[video_pb2.Video]:
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

    def delete(self, id: str, opts: Optional[CallOptions] = None) -> None:
        req = video_pb2.DeleteVideoRequest(id=id)
        self._t.unary(_SERVICE, "Delete", req, video_pb2.DeleteVideoResponse(), opts)

    def watch(
        self,
        id: str,
        *,
        include_heartbeats: bool = False,
        max_reconnects: int = 5,
        opts: Optional[CallOptions] = None,
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
