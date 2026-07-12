"""Tests for the events/webhook-endpoints resources and the proto->SDK bridge."""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

from transcodely import Event
from transcodely.resources.events import Events, proto_event_to_sdk
from transcodely.resources.webhook_endpoints import WebhookEndpoints
from transcodely.v1 import common_pb2, webhook_pb2


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


# ---- proto_event_to_sdk bridge ----------------------------------------------


def _proto_event(**kwargs: Any) -> webhook_pb2.Event:
    return webhook_pb2.Event(**kwargs)


def test_bridge_decodes_resource_and_maps_fields() -> None:
    e = _proto_event(
        id="evt_x",
        app_id="app_1",
        type="job.succeeded",
        data='{"id":"job_z","object":"job","status":"completed"}',
        request_id="req_z",
        pending_webhooks=3,
        api_version="2026-05-23",
        object="event",
    )
    e.created_at.FromJsonString("2026-05-24T10:55:08Z")

    sdk = proto_event_to_sdk(e)
    assert isinstance(sdk, Event)
    assert sdk.id == "evt_x"
    assert sdk.type == "job.succeeded"
    assert sdk.data.id == "job_z"
    assert sdk.pending_webhooks == 3
    assert sdk.request.id == "req_z"
    assert sdk.request.idempotency_key is None
    # No-millis RFC 3339 form (protobuf Timestamp.ToJsonString).
    assert sdk.created == "2026-05-24T10:55:08Z"


def test_bridge_empty_data_known_type_yields_default_message() -> None:
    sdk = proto_event_to_sdk(_proto_event(id="evt_y", type="video.uploaded", data=""))
    assert type(sdk.data).__name__ == "Video"
    assert sdk.created == ""  # no created_at set


def test_bridge_unknown_type_passes_dict_through() -> None:
    sdk = proto_event_to_sdk(_proto_event(id="evt_u", type="future.thing", data='{"foo":"bar"}'))
    assert sdk.data == {"foo": "bar"}


# ---- Events resource --------------------------------------------------------


def test_events_retrieve_returns_unified_event() -> None:
    proto = _proto_event(id="evt_1", type="job.succeeded", data='{"id":"job_1"}')
    t = FakeTransport({"RetrieveEvent": webhook_pb2.RetrieveEventResponse(event=proto)})
    ev = Events(t).retrieve("evt_1")  # type: ignore[arg-type]
    assert isinstance(ev, Event)
    assert ev.id == "evt_1"
    assert ev.data.id == "job_1"
    assert t.calls[0][0] == "RetrieveEvent"


def test_events_list_auto_paginates() -> None:
    page1 = webhook_pb2.ListEventsResponse(
        events=[_proto_event(id="evt_1", type="job.created", data='{"id":"job_1"}')],
        pagination=common_pb2.PaginationResponse(next_cursor="c1"),
    )
    page2 = webhook_pb2.ListEventsResponse(
        events=[_proto_event(id="evt_2", type="job.created", data='{"id":"job_2"}')],
        pagination=common_pb2.PaginationResponse(next_cursor=""),
    )

    def respond(req: webhook_pb2.ListEventsRequest) -> webhook_pb2.ListEventsResponse:
        return page2 if req.pagination.cursor == "c1" else page1

    t = FakeTransport({"ListEvents": respond})
    page = Events(t).list(app_id="app_1")  # type: ignore[arg-type]
    ids = [e.id for e in page.auto_paging_iter()]
    assert ids == ["evt_1", "evt_2"]
    # First call carries the app_id filter; cursor empty on the first fetch.
    assert t.calls[0][1].app_id == "app_1"


def test_events_resend_sets_endpoint_ids() -> None:
    resp = webhook_pb2.ResendEventResponse(
        deliveries=[
            webhook_pb2.WebhookDelivery(id="whd_1"),
            webhook_pb2.WebhookDelivery(id="whd_2"),
        ]
    )
    t = FakeTransport({"ResendEvent": resp})
    out = Events(t).resend("evt_1", endpoint_ids=["whe_1", "whe_2"])  # type: ignore[arg-type]
    assert [d.id for d in out] == ["whd_1", "whd_2"]
    assert list(t.calls[0][1].endpoint_ids) == ["whe_1", "whe_2"]


def test_events_resend_omits_endpoint_ids_by_default() -> None:
    t = FakeTransport({"ResendEvent": webhook_pb2.ResendEventResponse()})
    Events(t).resend("evt_1")  # type: ignore[arg-type]
    assert list(t.calls[0][1].endpoint_ids) == []


# ---- WebhookEndpoints resource ----------------------------------------------


def test_endpoints_create_builds_request_and_unwraps_endpoint() -> None:
    endpoint = webhook_pb2.WebhookEndpoint(
        id="whe_1", url="https://x.test/hook", secret="whsec_abc"
    )
    t = FakeTransport(
        {"CreateWebhookEndpoint": webhook_pb2.CreateWebhookEndpointResponse(endpoint=endpoint)}
    )
    out = WebhookEndpoints(t).create(  # type: ignore[arg-type]
        app_id="app_1",
        url="https://x.test/hook",
        enabled_events=["job.succeeded", "video.uploaded"],
        metadata={"team": "media"},
    )
    assert out.id == "whe_1"
    assert out.secret == "whsec_abc"
    req = t.calls[0][1]
    assert req.app_id == "app_1"
    assert list(req.enabled_events) == ["job.succeeded", "video.uploaded"]
    assert req.metadata["team"] == "media"


def test_endpoints_rotate_secret_returns_new_secret() -> None:
    endpoint = webhook_pb2.WebhookEndpoint(id="whe_1", secret="whsec_new")
    t = FakeTransport(
        {"RotateWebhookSecret": webhook_pb2.RotateWebhookSecretResponse(endpoint=endpoint)}
    )
    out = WebhookEndpoints(t).rotate_secret("whe_1")  # type: ignore[arg-type]
    assert out.secret == "whsec_new"


def test_endpoints_send_test_returns_delivery() -> None:
    t = FakeTransport(
        {
            "SendTestWebhook": webhook_pb2.SendTestWebhookResponse(
                delivery=webhook_pb2.WebhookDelivery(id="whd_1")
            )
        }
    )
    out = WebhookEndpoints(t).send_test("whe_1", "job.succeeded")  # type: ignore[arg-type]
    assert out.id == "whd_1"
    req = t.calls[0][1]
    assert req.endpoint_id == "whe_1" and req.event_type == "job.succeeded"


def test_endpoints_delete_returns_none() -> None:
    t = FakeTransport({"DeleteWebhookEndpoint": webhook_pb2.DeleteWebhookEndpointResponse()})
    assert WebhookEndpoints(t).delete("whe_1") is None  # type: ignore[arg-type]


def test_endpoints_list_deliveries_filters_and_paginates() -> None:
    resp = webhook_pb2.ListWebhookDeliveriesResponse(
        deliveries=[webhook_pb2.WebhookDelivery(id="whd_1")],
        pagination=common_pb2.PaginationResponse(next_cursor=""),
    )
    t = FakeTransport({"ListWebhookDeliveries": resp})
    page = WebhookEndpoints(t).list_deliveries(event_id="evt_1", status="failed")  # type: ignore[arg-type]
    assert [d.id for d in page.auto_paging_iter()] == ["whd_1"]
    req = t.calls[0][1]
    assert req.event_id == "evt_1" and req.status == "failed"


def test_endpoints_get_health_passes_window() -> None:
    t = FakeTransport(
        {"GetEndpointHealth": webhook_pb2.GetEndpointHealthResponse(window="7d", total_attempts=10)}
    )
    out = WebhookEndpoints(t).get_health("whe_1", "7d")  # type: ignore[arg-type]
    assert out.window == "7d"
    assert t.calls[0][1].window == "7d"
