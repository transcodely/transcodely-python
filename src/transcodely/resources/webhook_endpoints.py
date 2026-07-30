"""Webhook endpoint resource — manage signed endpoints, test deliveries, and health.

Stripe parity: method names match the resource verbs (``create``, ``retrieve``,
``update``, ``delete``, ``list``) without re-stating the "Webhook" prefix already
implied by ``client.webhook_endpoints``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import common_pb2, webhook_pb2

_SERVICE = "transcodely.v1.WebhookService"


class WebhookEndpoints:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(
        self,
        *,
        app_id: str | None = None,
        url: str | None = None,
        enabled_events: list[str] | None = None,
        description: str | None = None,
        api_version: str | None = None,
        metadata: Mapping[str, str] | None = None,
        request: webhook_pb2.CreateWebhookEndpointRequest | None = None,
        opts: CallOptions | None = None,
    ) -> webhook_pb2.WebhookEndpoint:
        """Create a webhook endpoint.

        The signing secret is populated on the returned endpoint **only here**
        (and on :meth:`rotate_secret`) — store it securely; it cannot be
        retrieved again.
        """
        if request is None:
            req = webhook_pb2.CreateWebhookEndpointRequest()
            if app_id is not None:
                req.app_id = app_id
            if url is not None:
                req.url = url
            if enabled_events:
                req.enabled_events.extend(enabled_events)
            if description is not None:
                req.description = description
            if api_version is not None:
                req.api_version = api_version
            if metadata:
                for k, v in metadata.items():
                    req.metadata[k] = v
        else:
            req = request
        res = self._t.unary(
            _SERVICE,
            "CreateWebhookEndpoint",
            req,
            webhook_pb2.CreateWebhookEndpointResponse(),
            opts,
        )
        return res.endpoint

    def retrieve(self, id: str, opts: CallOptions | None = None) -> webhook_pb2.WebhookEndpoint:
        req = webhook_pb2.RetrieveWebhookEndpointRequest(id=id)
        res = self._t.unary(
            _SERVICE,
            "RetrieveWebhookEndpoint",
            req,
            webhook_pb2.RetrieveWebhookEndpointResponse(),
            opts,
        )
        return res.endpoint

    def update(
        self,
        id: str,
        *,
        url: str | None = None,
        description: str | None = None,
        enabled_events: list[str] | None = None,
        status: str | None = None,
        metadata: Mapping[str, str] | None = None,
        request: webhook_pb2.UpdateWebhookEndpointRequest | None = None,
        opts: CallOptions | None = None,
    ) -> webhook_pb2.WebhookEndpoint:
        """Update an endpoint. Only provided fields are changed; omit the rest."""
        if request is None:
            req = webhook_pb2.UpdateWebhookEndpointRequest(id=id)
            if url is not None:
                req.url = url
            if description is not None:
                req.description = description
            if enabled_events is not None:
                req.enabled_events.extend(enabled_events)
            if status is not None:
                req.status = status
            if metadata is not None:
                for k, v in metadata.items():
                    req.metadata[k] = v
        else:
            req = request
        res = self._t.unary(
            _SERVICE,
            "UpdateWebhookEndpoint",
            req,
            webhook_pb2.UpdateWebhookEndpointResponse(),
            opts,
        )
        return res.endpoint

    def delete(self, id: str, opts: CallOptions | None = None) -> None:
        req = webhook_pb2.DeleteWebhookEndpointRequest(id=id)
        self._t.unary(
            _SERVICE,
            "DeleteWebhookEndpoint",
            req,
            webhook_pb2.DeleteWebhookEndpointResponse(),
            opts,
        )

    def list(
        self,
        *,
        app_id: str,
        limit: int | None = None,
        opts: CallOptions | None = None,
    ) -> Page[webhook_pb2.WebhookEndpoint]:
        def fetch(cursor: str | None) -> PageContents[webhook_pb2.WebhookEndpoint]:
            req = webhook_pb2.ListWebhookEndpointsRequest(app_id=app_id)
            pagination = common_pb2.PaginationRequest()
            if limit is not None:
                pagination.limit = limit
            if cursor is not None:
                pagination.cursor = cursor
            req.pagination.CopyFrom(pagination)
            res = self._t.unary(
                _SERVICE,
                "ListWebhookEndpoints",
                req,
                webhook_pb2.ListWebhookEndpointsResponse(),
                opts,
            )
            return PageContents(
                items=list(res.endpoints),
                next_cursor=res.pagination.next_cursor or None,
            )

        return Page(fetch)

    def rotate_secret(
        self, id: str, opts: CallOptions | None = None
    ) -> webhook_pb2.WebhookEndpoint:
        """Rotate the signing secret.

        The previous secret stays valid for 24 h to drain in-flight deliveries.
        The returned endpoint includes the new plain-text ``secret`` — the only
        response besides :meth:`create` that exposes it.
        """
        req = webhook_pb2.RotateWebhookSecretRequest(id=id)
        res = self._t.unary(
            _SERVICE,
            "RotateWebhookSecret",
            req,
            webhook_pb2.RotateWebhookSecretResponse(),
            opts,
        )
        return res.endpoint

    def send_test(
        self, endpoint_id: str, event_type: str, opts: CallOptions | None = None
    ) -> webhook_pb2.WebhookDelivery:
        """Send a synthetic test event to a single endpoint.

        The synthetic event is invisible to ``client.events.list`` and never
        bumps ``pending_webhooks`` on any other event. ``event_type`` must be a
        concrete type (the ``"*"`` wildcard is rejected server-side).
        Rate-limited to 10/min per endpoint.
        """
        req = webhook_pb2.SendTestWebhookRequest(endpoint_id=endpoint_id, event_type=event_type)
        res = self._t.unary(
            _SERVICE, "SendTestWebhook", req, webhook_pb2.SendTestWebhookResponse(), opts
        )
        return res.delivery

    def list_deliveries(
        self,
        *,
        endpoint_id: str | None = None,
        event_id: str | None = None,
        status: str | None = None,
        limit: int | None = None,
        opts: CallOptions | None = None,
    ) -> Page[webhook_pb2.WebhookDelivery]:
        """List delivery attempts. At least one of ``endpoint_id`` / ``event_id``
        is required server-side."""

        def fetch(cursor: str | None) -> PageContents[webhook_pb2.WebhookDelivery]:
            req = webhook_pb2.ListWebhookDeliveriesRequest()
            if endpoint_id is not None:
                req.endpoint_id = endpoint_id
            if event_id is not None:
                req.event_id = event_id
            if status is not None:
                req.status = status
            pagination = common_pb2.PaginationRequest()
            if limit is not None:
                pagination.limit = limit
            if cursor is not None:
                pagination.cursor = cursor
            req.pagination.CopyFrom(pagination)
            res = self._t.unary(
                _SERVICE,
                "ListWebhookDeliveries",
                req,
                webhook_pb2.ListWebhookDeliveriesResponse(),
                opts,
            )
            return PageContents(
                items=list(res.deliveries),
                next_cursor=res.pagination.next_cursor or None,
            )

        return Page(fetch)

    def get_health(
        self,
        endpoint_id: str,
        window: Literal["24h", "7d", "30d"] | None = None,
        opts: CallOptions | None = None,
    ) -> webhook_pb2.GetEndpointHealthResponse:
        """Aggregate delivery health for one endpoint over a rolling window.
        Response is cached server-side for ~30 s."""
        req = webhook_pb2.GetEndpointHealthRequest(endpoint_id=endpoint_id)
        if window is not None:
            req.window = window
        return self._t.unary(
            _SERVICE, "GetEndpointHealth", req, webhook_pb2.GetEndpointHealthResponse(), opts
        )
