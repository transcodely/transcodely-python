"""Event resource — query and replay events.

Every event handed back is the same unified :class:`~transcodely.webhooks.types.Event`
that :func:`transcodely.construct_event` produces, so a ``job.succeeded`` handler
can be exercised against an event pulled from :meth:`Events.retrieve` and behave
identically. The bridge from the proto-shape ``Event`` (which carries the inner
resource as a JSON string) to the SDK-shape :class:`Event` is
:func:`proto_event_to_sdk`.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import common_pb2, webhook_pb2
from ..webhooks.types import Event, EventRequest, decoder_for_type

_SERVICE = "transcodely.v1.WebhookService"


class Events:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def retrieve(self, id: str, opts: Optional[CallOptions] = None) -> Event:
        req = webhook_pb2.RetrieveEventRequest(id=id)
        res = self._t.unary(
            _SERVICE, "RetrieveEvent", req, webhook_pb2.RetrieveEventResponse(), opts
        )
        return proto_event_to_sdk(res.event)

    def resend(
        self,
        id: str,
        *,
        endpoint_ids: Optional[list[str]] = None,
        opts: Optional[CallOptions] = None,
    ) -> list[webhook_pb2.WebhookDelivery]:
        """Resend an existing event, creating new pending delivery records — one
        per target endpoint. When ``endpoint_ids`` is omitted, resends to every
        currently-subscribed enabled endpoint."""
        req = webhook_pb2.ResendEventRequest(id=id)
        if endpoint_ids:
            req.endpoint_ids.extend(endpoint_ids)
        res = self._t.unary(_SERVICE, "ResendEvent", req, webhook_pb2.ResendEventResponse(), opts)
        return list(res.deliveries)

    def list(
        self,
        *,
        app_id: str,
        type: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[Event]:
        def fetch(cursor: Optional[str]) -> PageContents[Event]:
            req = webhook_pb2.ListEventsRequest(app_id=app_id)
            if type is not None:
                req.type = type
            if created_after is not None:
                req.created_after.FromDatetime(created_after)
            if created_before is not None:
                req.created_before.FromDatetime(created_before)
            pagination = common_pb2.PaginationRequest()
            if limit is not None:
                pagination.limit = limit
            if cursor is not None:
                pagination.cursor = cursor
            req.pagination.CopyFrom(pagination)
            res = self._t.unary(_SERVICE, "ListEvents", req, webhook_pb2.ListEventsResponse(), opts)
            return PageContents(
                items=[proto_event_to_sdk(e) for e in res.events],
                next_cursor=res.pagination.next_cursor or None,
            )

        return Page(fetch)


def proto_event_to_sdk(proto: webhook_pb2.Event) -> Event:
    """Bridge a proto ``Event`` (``data`` as a JSON string, ``created_at`` as a
    ``Timestamp``) to the SDK :class:`Event` (decoded resource, RFC 3339 string).

    Used by :meth:`Events.retrieve` and :meth:`Events.list`.
    """
    parsed_data: Any = {}
    if proto.data:
        try:
            parsed_data = json.loads(proto.data)
        except ValueError:
            # Server-controlled; if it ever fails, leave the placeholder so the
            # event still surfaces.
            pass

    decode = decoder_for_type(proto.type)
    data: Any = decode(parsed_data) if decode and isinstance(parsed_data, dict) else parsed_data

    created = proto.created_at.ToJsonString() if proto.HasField("created_at") else ""

    return Event(
        id=proto.id,
        object="event",
        api_version=proto.api_version,
        created=created,
        type=proto.type,
        data=data,
        livemode=proto.livemode,
        pending_webhooks=proto.pending_webhooks,
        # proto Event carries only request_id; idempotency_key is always None
        # until JobService.Create propagates it. An unset request_id maps to
        # None so this path matches the webhook envelope path (both use None for
        # events emitted outside a request scope).
        request=EventRequest(id=proto.request_id or None, idempotency_key=None),
    )
