"""Job resource — create / get / list / cancel / confirm / watch."""

from __future__ import annotations

from typing import Any, Generator, Mapping, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..streaming import watch
from ..v1 import job_pb2

_SERVICE = "transcodely.v1.JobService"


class Jobs:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(
        self,
        input_url: Optional[str] = None,
        outputs: Optional[list[Mapping[str, Any]]] = None,
        *,
        idempotency_key: Optional[str] = None,
        webhook_url: Optional[str] = None,
        priority: Optional[int] = None,
        metadata: Optional[Mapping[str, str]] = None,
        request: Optional[job_pb2.CreateJobRequest] = None,
        opts: Optional[CallOptions] = None,
    ) -> job_pb2.Job:
        """Create a new transcoding job. Auto-fills ``idempotency_key`` if omitted."""
        if request is None:
            req = job_pb2.CreateJobRequest()
            if input_url is not None:
                req.input_url = input_url
            if outputs:
                from google.protobuf import json_format

                from .._codec.json_codec import expand_enum_value, transform_enums_in_dict

                # Outputs are nested messages — round-trip through JSON so callers can
                # pass plain dicts with simplified-enum strings.
                payload = {"outputs": list(outputs)}
                transform_enums_in_dict(payload, req.DESCRIPTOR, mode="expand")
                json_format.ParseDict(payload, req, ignore_unknown_fields=True)
            if webhook_url is not None:
                req.webhook_url = webhook_url
            if priority is not None:
                req.priority = priority
            if metadata:
                for k, v in metadata.items():
                    req.metadata[k] = v
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
        status: Optional[int] = None,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[job_pb2.Job]:
        from ..v1 import common_pb2

        def fetch(cursor: Optional[str]) -> PageContents[job_pb2.Job]:
            req = job_pb2.ListJobsRequest()
            if status is not None:
                req.status = status
            pagination = common_pb2.PaginationRequest()
            if limit is not None:
                pagination.limit = limit
            if cursor is not None:
                pagination.cursor = cursor
            req.pagination.CopyFrom(pagination)
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
