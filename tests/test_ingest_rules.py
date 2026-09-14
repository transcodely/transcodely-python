"""Tests for the IngestRuleService surface (Horizon S5).

Two guarantees:

1. **Wire decoding** — an ``IngestRule`` and its event log arrive as snake_case
   JSON with simplified lowercase enum values, and the reveal-once secret rides
   on the create response and nowhere else.
2. **Facade completeness** — every RPC on the service has a method on
   ``IngestRules``, every message is re-exported from ``transcodely.types``, and
   the namespace hangs off the client.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from google.protobuf.descriptor_pool import Default as default_pool

from transcodely import types
from transcodely._codec.json_codec import deserialize
from transcodely.resources.ingest_rules import IngestRules
from transcodely.v1 import common_pb2, ingest_rule_pb2, job_pb2


class FakeTransport:
    """Duck-typed stand-in for Transport that returns canned responses per method."""

    def __init__(self, responses: dict[str, Any | Callable[[Any], Any]]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, str, Any]] = []

    def unary(
        self,
        service_name: str,
        method_name: str,
        request: Any,
        response: Any,
        opts: Any | None = None,
    ) -> Any:
        self.calls.append((service_name, method_name, request))
        r = self._responses[method_name]
        return r(request) if callable(r) else r


def _encode(obj: Any) -> bytes:
    return json.dumps(obj).encode("utf-8")


# ---- Wire decoding -----------------------------------------------------------


def test_create_response_decodes_with_reveal_once_secret() -> None:
    res = deserialize(
        _encode(
            {
                "rule": {
                    "id": "ing_a1b2c3d4e5f6",
                    "app_id": "app_k1l2m3n4o5",
                    "origin_id": "ori_a1b2c3d4e5f6",
                    "name": "Watch uploads/",
                    "enabled": True,
                    "filters": {
                        "prefix": "uploads/",
                        "suffixes": [".mp4", ".mov"],
                        "min_bytes": 1024,
                        "max_bytes": 0,
                    },
                    "action": {
                        "managed": True,
                        "priority": "standard",
                        "output_path_template": "{input_dir}/{input_name}/{resolution}",
                    },
                    "endpoint_url": "https://api.transcodely.com/ingest/ing_a1b2c3d4e5f6",
                    "secret_prefix": "ings_a1b",
                    "secret_hint": "z9y8",
                    "events_received": 0,
                    "jobs_created": 0,
                    "created_at": "2026-09-14T10:00:00Z",
                    "updated_at": "2026-09-14T10:00:00Z",
                },
                "secret": "ings_a1b2c3d4e5f6g7h8i9j0z9y8",
            }
        ),
        ingest_rule_pb2.CreateIngestRuleResponse(),
    )

    assert res.secret == "ings_a1b2c3d4e5f6g7h8i9j0z9y8"
    assert res.rule.id == "ing_a1b2c3d4e5f6"
    assert res.rule.endpoint_url == "https://api.transcodely.com/ingest/ing_a1b2c3d4e5f6"
    assert res.rule.secret_prefix == "ings_a1b"
    assert res.rule.secret_hint == "z9y8"
    assert res.rule.filters.prefix == "uploads/"
    assert list(res.rule.filters.suffixes) == [".mp4", ".mov"]
    assert res.rule.filters.min_bytes == 1024
    assert res.rule.action.managed is True
    # The simplified wire enum expands to the generated constant.
    assert res.rule.action.priority == job_pb2.JOB_PRIORITY_STANDARD
    assert res.rule.action.output_path_template == "{input_dir}/{input_name}/{resolution}"


def test_read_of_the_rule_carries_no_secret() -> None:
    res = deserialize(
        _encode(
            {
                "rule": {
                    "id": "ing_a1b2c3d4e5f6",
                    "app_id": "app_k1l2m3n4o5",
                    "origin_id": "ori_a1b2c3d4e5f6",
                    "name": "Watch uploads/",
                    "enabled": True,
                    "secret_prefix": "ings_a1b",
                    "secret_hint": "z9y8",
                    "events_received": 42,
                    "jobs_created": 40,
                    "last_event_at": "2026-09-14T11:00:00Z",
                    "created_at": "2026-09-14T10:00:00Z",
                    "updated_at": "2026-09-14T10:00:00Z",
                }
            }
        ),
        ingest_rule_pb2.GetIngestRuleResponse(),
    )

    assert res.rule.events_received == 42
    assert res.rule.jobs_created == 40
    assert res.rule.HasField("last_event_at")
    assert not res.rule.HasField("secret_rotated_at")
    # The message has no `secret` field at all: the full value rides on create
    # (and on a rotation) and nowhere else.
    assert "secret" not in {f.name for f in ingest_rule_pb2.IngestRule.DESCRIPTOR.fields}
    assert "secret" in {f.name for f in ingest_rule_pb2.CreateIngestRuleResponse.DESCRIPTOR.fields}


def test_event_log_decodes_with_lowercase_source_and_status() -> None:
    res = deserialize(
        _encode(
            {
                "events": [
                    {
                        "id": "sev_a1b2c3d4e5f6g7",
                        "rule_id": "ing_a1b2c3d4e5f6",
                        "app_id": "app_k1l2m3n4o5",
                        "bucket": "my-uploads",
                        "object_key": "uploads/my clip.mp4",
                        "etag": "d41d8cd98f00b204",
                        "size_bytes": 10485760,
                        "content_type": "video/mp4",
                        "source": "s3_sns",
                        "status": "created",
                        "job_id": "job_a1b2c3d4e5f6",
                        "received_at": "2026-09-14T11:00:00Z",
                        "processed_at": "2026-09-14T11:00:02Z",
                    },
                    {
                        "id": "sev_b2c3d4e5f6g7h8",
                        "rule_id": "ing_a1b2c3d4e5f6",
                        "app_id": "app_k1l2m3n4o5",
                        "bucket": "my-uploads",
                        "object_key": "uploads/notes.txt",
                        "source": "gcs_pubsub",
                        "status": "skipped",
                        "reason": "filter_suffix",
                        "received_at": "2026-09-14T11:05:00Z",
                        "processed_at": "2026-09-14T11:05:00Z",
                    },
                ],
                "pagination": {"next_cursor": ""},
            }
        ),
        ingest_rule_pb2.ListIngestEventsResponse(),
    )

    assert len(res.events) == 2
    assert res.events[0].source == ingest_rule_pb2.STORAGE_EVENT_SOURCE_S3_SNS
    assert res.events[0].status == ingest_rule_pb2.STORAGE_EVENT_STATUS_CREATED
    # Stored URL-decoded: S3 writes a space as "+".
    assert res.events[0].object_key == "uploads/my clip.mp4"
    assert res.events[0].job_id == "job_a1b2c3d4e5f6"

    assert res.events[1].source == ingest_rule_pb2.STORAGE_EVENT_SOURCE_GCS_PUBSUB
    assert res.events[1].status == ingest_rule_pb2.STORAGE_EVENT_STATUS_SKIPPED
    assert res.events[1].reason == "filter_suffix"
    assert res.events[1].job_id == ""


# ---- Facade completeness -----------------------------------------------------


def test_facade_covers_every_rpc() -> None:
    """Adding an RPC without a facade method fails here, not in production."""
    svc = default_pool().FindServiceByName("transcodely.v1.IngestRuleService")
    # "ListEvents" -> "list_events", "ReplayEvent" -> "replay_event".
    expected = {
        "".join("_" + c.lower() if c.isupper() and i else c.lower() for i, c in enumerate(m.name))
        for m in svc.methods
    }
    actual = {n for n in vars(IngestRules) if not n.startswith("_")}
    assert actual == expected


def test_every_ingest_message_is_re_exported_from_types() -> None:
    names = [
        "IngestRule",
        "IngestRuleFilters",
        "IngestRuleAction",
        "StorageEvent",
        "StorageEventSource",
        "StorageEventStatus",
        "CreateIngestRuleRequest",
        "CreateIngestRuleResponse",
        "GetIngestRuleRequest",
        "GetIngestRuleResponse",
        "ListIngestRulesRequest",
        "ListIngestRulesResponse",
        "UpdateIngestRuleRequest",
        "UpdateIngestRuleResponse",
        "DeleteIngestRuleRequest",
        "DeleteIngestRuleResponse",
        "ListIngestEventsRequest",
        "ListIngestEventsResponse",
        "TestIngestRuleRequest",
        "TestIngestRuleResponse",
        "ReplayIngestEventRequest",
        "ReplayIngestEventResponse",
    ]
    for name in names:
        assert name in types.__all__, f"{name} missing from transcodely.types.__all__"
        assert getattr(types, name) is getattr(ingest_rule_pb2, name), name


def test_client_exposes_the_namespace() -> None:
    from transcodely import Transcodely

    client = Transcodely(api_key="ak_test")
    assert isinstance(client.ingest_rules, IngestRules)
    # Lazily built once and cached, like every other namespace.
    assert client.ingest_rules is client.ingest_rules


# ---- Facade behavior ---------------------------------------------------------


def test_create_returns_the_whole_response_so_the_secret_is_reachable() -> None:
    resp = ingest_rule_pb2.CreateIngestRuleResponse(
        rule=ingest_rule_pb2.IngestRule(id="ing_a1b2c3d4e5f6", secret_prefix="ings_a1b"),
        secret="ings_full_secret_value",
    )
    t = FakeTransport({"Create": resp})
    out = IngestRules(t).create(  # type: ignore[arg-type]
        origin_id="ori_a1b2c3d4e5f6",
        name="Watch uploads/",
        action={"managed": True, "priority": "standard"},
    )

    assert out.secret == "ings_full_secret_value"
    assert out.rule.id == "ing_a1b2c3d4e5f6"
    service, method, req = t.calls[0]
    assert (service, method) == ("transcodely.v1.IngestRuleService", "Create")
    assert req.origin_id == "ori_a1b2c3d4e5f6"
    # fill_from_dict expands the simplified enum string in the nested action.
    assert req.action.priority == job_pb2.JOB_PRIORITY_STANDARD


def test_update_surfaces_the_rotated_secret_and_the_backlog() -> None:
    resp = ingest_rule_pb2.UpdateIngestRuleResponse(
        rule=ingest_rule_pb2.IngestRule(id="ing_a1b2c3d4e5f6", enabled=True),
        secret="ings_rotated_secret",
        events_skipped_while_disabled=7,
    )
    t = FakeTransport({"Update": resp})
    out = IngestRules(t).update(  # type: ignore[arg-type]
        id="ing_a1b2c3d4e5f6", enabled=True, rotate_secret=True
    )

    assert out.secret == "ings_rotated_secret"
    assert out.events_skipped_while_disabled == 7
    assert t.calls[0][2].rotate_secret is True


def test_get_delete_and_replay_unwrap_to_the_bare_message() -> None:
    t = FakeTransport(
        {
            "Get": ingest_rule_pb2.GetIngestRuleResponse(
                rule=ingest_rule_pb2.IngestRule(id="ing_a1b2c3d4e5f6")
            ),
            "Delete": ingest_rule_pb2.DeleteIngestRuleResponse(
                rule=ingest_rule_pb2.IngestRule(id="ing_a1b2c3d4e5f6")
            ),
            "ReplayEvent": ingest_rule_pb2.ReplayIngestEventResponse(
                event=ingest_rule_pb2.StorageEvent(
                    id="sev_a1b2c3d4e5f6g7",
                    status=ingest_rule_pb2.STORAGE_EVENT_STATUS_RECEIVED,
                )
            ),
        }
    )
    rules = IngestRules(t)  # type: ignore[arg-type]

    assert rules.get("ing_a1b2c3d4e5f6").id == "ing_a1b2c3d4e5f6"
    assert rules.delete("ing_a1b2c3d4e5f6").id == "ing_a1b2c3d4e5f6"

    replayed = rules.replay_event("sev_a1b2c3d4e5f6g7")
    assert replayed.status == ingest_rule_pb2.STORAGE_EVENT_STATUS_RECEIVED
    assert t.calls[2][2].event_id == "sev_a1b2c3d4e5f6g7"


def test_list_events_accepts_the_simplified_status_string() -> None:
    resp = ingest_rule_pb2.ListIngestEventsResponse(
        events=[ingest_rule_pb2.StorageEvent(id="sev_a1b2c3d4e5f6g7")],
        pagination=common_pb2.PaginationResponse(next_cursor=""),
    )
    t = FakeTransport({"ListEvents": resp})
    page = IngestRules(t).list_events(  # type: ignore[arg-type]
        rule_id="ing_a1b2c3d4e5f6", status="skipped", limit=25
    )
    assert [e.id for e in page.items] == ["sev_a1b2c3d4e5f6g7"]

    req = t.calls[0][2]
    assert req.rule_id == "ing_a1b2c3d4e5f6"
    assert req.status == ingest_rule_pb2.STORAGE_EVENT_STATUS_SKIPPED
    assert req.pagination.limit == 25


def test_list_pages_through_the_cursor() -> None:
    pages = [
        ingest_rule_pb2.ListIngestRulesResponse(
            rules=[ingest_rule_pb2.IngestRule(id="ing_page1")],
            pagination=common_pb2.PaginationResponse(next_cursor="cur1"),
        ),
        ingest_rule_pb2.ListIngestRulesResponse(
            rules=[ingest_rule_pb2.IngestRule(id="ing_page2")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        ),
    ]
    calls = {"n": 0}

    def respond(_req: Any) -> Any:
        page = pages[calls["n"]]
        calls["n"] += 1
        return page

    t = FakeTransport({"List": respond})
    seen = [r.id for r in IngestRules(t).list(origin_id="ori_a1b2c3d4e5f6").auto_paging_iter()]  # type: ignore[arg-type]
    assert seen == ["ing_page1", "ing_page2"]
    assert t.calls[0][2].origin_id == "ori_a1b2c3d4e5f6"


def test_test_dispatches_the_dry_run() -> None:
    resp = ingest_rule_pb2.TestIngestRuleResponse(matched=False, reason="filter_prefix")
    t = FakeTransport({"Test": resp})
    out = IngestRules(t).test(  # type: ignore[arg-type]
        id="ing_a1b2c3d4e5f6", object_key="other/clip.mp4"
    )
    assert out.matched is False
    assert out.reason == "filter_prefix"
    assert not out.HasField("job_request")
    assert t.calls[0][1] == "Test"
