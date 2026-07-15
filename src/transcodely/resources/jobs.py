"""Job resource — create / get / list / cancel / confirm / watch."""

from __future__ import annotations

from typing import Any, Generator, Mapping, Optional, Union

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..streaming import watch
from ..v1 import job_pb2
from ._helpers import assign_pagination, fill_from_dict, resolve_enum

_SERVICE = "transcodely.v1.JobService"


class Jobs:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(
        self,
        input_url: Optional[str] = None,
        outputs: Optional[list[Mapping[str, Any]]] = None,
        *,
        output_origin_id: Optional[str] = None,
        output_path_template: Optional[str] = None,
        input_origin_id: Optional[str] = None,
        input_path: Optional[str] = None,
        priority: Optional[Union[int, str]] = None,
        delayed_start: Optional[bool] = None,
        webhook_url: Optional[str] = None,
        metadata: Optional[Mapping[str, str]] = None,
        idempotency_key: Optional[str] = None,
        request: Optional[job_pb2.CreateJobRequest] = None,
        opts: Optional[CallOptions] = None,
    ) -> job_pb2.Job:
        """Create a new transcoding job.

        Keyword arguments mirror the API's snake_case fields. Enum-valued fields —
        ``priority`` here, plus any enum inside ``outputs`` dicts — accept either the
        simplified lowercase string (``"standard"``, ``"h264"``) or the raw proto int.
        Provide inputs via ``input_url`` (direct URL) OR ``input_origin_id`` +
        ``input_path`` (origin mode); the server rejects both. Pass a fully-built
        ``request=`` to bypass the convenience kwargs entirely. ``idempotency_key`` is
        auto-filled with a uuid4 when omitted. ``output_path_template`` overrides where
        rendered outputs are written within the output origin (e.g.
        ``"videos/{job_id}/{output}"``).
        """
        if request is None:
            payload: dict[str, Any] = {}
            if input_url is not None:
                payload["input_url"] = input_url
            if input_origin_id is not None:
                payload["input_origin_id"] = input_origin_id
            if input_path is not None:
                payload["input_path"] = input_path
            if output_origin_id is not None:
                payload["output_origin_id"] = output_origin_id
            if output_path_template is not None:
                payload["output_path_template"] = output_path_template
            if outputs:
                payload["outputs"] = list(outputs)
            if priority is not None:
                payload["priority"] = priority
            if delayed_start is not None:
                payload["delayed_start"] = delayed_start
            if webhook_url is not None:
                payload["webhook_url"] = webhook_url
            if metadata:
                payload["metadata"] = dict(metadata)
            req = job_pb2.CreateJobRequest()
            fill_from_dict(req, payload)
        else:
            req = request
        if not req.idempotency_key:
            from .._transport.headers import new_idempotency_key

            req.idempotency_key = idempotency_key or new_idempotency_key()
        res = self._t.unary(_SERVICE, "Create", req, job_pb2.CreateJobResponse(), opts)
        return res.job

    def get(self, id: str, opts: Optional[CallOptions] = None) -> job_pb2.Job:
        req = job_pb2.GetJobRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, job_pb2.GetJobResponse(), opts).job

    def list(
        self,
        *,
        status: Optional[Union[int, str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        pagination: Optional[Mapping[str, Any]] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[job_pb2.Job]:
        """List jobs, optionally filtered by ``status``.

        ``status`` accepts the simplified lowercase string (``"processing"``) or the
        raw ``JobStatus`` int. Pagination may be given as ``limit`` / ``offset``
        keyword args or as a ``pagination={"limit": ..., "offset": ..., "cursor": ...}``
        mapping; explicit keyword args take precedence over the mapping.
        """
        status_value = (
            resolve_enum(status, job_pb2.JobStatus.DESCRIPTOR) if status is not None else None
        )
        pag = dict(pagination) if pagination else {}
        eff_limit = limit if limit is not None else pag.get("limit")
        eff_offset = offset if offset is not None else pag.get("offset")
        start_cursor = pag.get("cursor")

        def fetch(cursor: Optional[str]) -> PageContents[job_pb2.Job]:
            req = job_pb2.ListJobsRequest()
            if status_value is not None:
                req.status = status_value
            assign_pagination(
                req.pagination,
                limit=eff_limit,
                cursor=cursor if cursor is not None else start_cursor,
                offset=eff_offset,
            )
            res = self._t.unary(_SERVICE, "List", req, job_pb2.ListJobsResponse(), opts)
            return PageContents(
                items=list(res.jobs),
                next_cursor=res.pagination.next_cursor or None,
            )

        return Page(fetch)

    def cancel(self, id: str, opts: Optional[CallOptions] = None) -> job_pb2.Job:
        req = job_pb2.CancelJobRequest(id=id)
        return self._t.unary(_SERVICE, "Cancel", req, job_pb2.CancelJobResponse(), opts).job

    def confirm(self, id: str, opts: Optional[CallOptions] = None) -> job_pb2.Job:
        req = job_pb2.ConfirmJobRequest(id=id)
        return self._t.unary(_SERVICE, "Confirm", req, job_pb2.ConfirmJobResponse(), opts).job

    def watch(
        self,
        id: str,
        *,
        include_heartbeats: bool = False,
        max_reconnects: int = 5,
        opts: Optional[CallOptions] = None,
    ) -> Generator[job_pb2.WatchJobResponse, None, None]:
        """Stream live job state. Auto-reconnects + filters HEARTBEAT events by default."""

        def factory() -> Generator[job_pb2.WatchJobResponse, None, None]:
            req = job_pb2.WatchJobRequest(id=id)
            yield from self._t.stream(_SERVICE, "Watch", req, job_pb2.WatchJobResponse, opts)

        yield from watch(
            factory,
            is_heartbeat=lambda e: e.event == job_pb2.WATCH_EVENT_TYPE_HEARTBEAT,
            include_heartbeats=include_heartbeats,
            max_reconnects=max_reconnects,
        )
