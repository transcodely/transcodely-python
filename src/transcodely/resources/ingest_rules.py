"""Ingest rule resource — watch a bucket, transcode what lands in it.

An ingest rule is a standing instruction on one readable storage origin: when
an object matching its filters appears, create the job its action describes.
Your storage provider posts object-created events to the rule's
``endpoint_url``, authenticated with the rule's secret, so no server of yours is
in the path. Amazon S3 via SNS, Google Cloud Storage via a Pub/Sub push
subscription, Supabase Storage via a database webhook, and a generic shape for
anything else are all recognised from the payload.

Duplicate deliveries are absorbed: an object is identified by
(rule, bucket, key, etag) and produces exactly one job.

The inbound endpoint itself is not part of this SDK — your storage provider
calls it, not you.
"""

from __future__ import annotations

from typing import Any, cast

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import ingest_rule_pb2
from ._helpers import assign_pagination, fill_from_dict, resolve_enum

_SERVICE = "transcodely.v1.IngestRuleService"


class IngestRules:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(self, **kwargs: Any) -> ingest_rule_pb2.CreateIngestRuleResponse:
        """Create a rule on a readable origin.

        The whole response is returned because ``secret`` rides on it: the
        inbound secret is shown once, here, and cannot be read back. Store it
        wherever the event sender will read it from.
        """
        req = fill_from_dict(ingest_rule_pb2.CreateIngestRuleRequest(), kwargs)
        return self._t.unary(_SERVICE, "Create", req, ingest_rule_pb2.CreateIngestRuleResponse())

    def get(self, id: str, opts: CallOptions | None = None) -> ingest_rule_pb2.IngestRule:
        """Fetch a rule by ID (``ing_*``).

        The secret is never returned again — the rule carries only
        ``secret_prefix`` and ``secret_hint``.
        """
        req = ingest_rule_pb2.GetIngestRuleRequest(id=id)
        return self._t.unary(
            _SERVICE, "Get", req, ingest_rule_pb2.GetIngestRuleResponse(), opts
        ).rule

    def list(
        self,
        *,
        origin_id: str | None = None,
        enabled: bool | None = None,
        app_id: str | None = None,
        limit: int | None = None,
        opts: CallOptions | None = None,
    ) -> Page[ingest_rule_pb2.IngestRule]:
        """Rules in scope, newest first."""

        def fetch(cursor: str | None) -> PageContents[ingest_rule_pb2.IngestRule]:
            req = ingest_rule_pb2.ListIngestRulesRequest()
            if origin_id is not None:
                req.origin_id = origin_id
            if enabled is not None:
                req.enabled = enabled
            if app_id is not None:
                req.app_id = app_id
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(
                _SERVICE, "List", req, ingest_rule_pb2.ListIngestRulesResponse(), opts
            )
            return PageContents(
                items=list(res.rules), next_cursor=res.pagination.next_cursor or None
            )

        return Page(fetch)

    def update(self, **kwargs: Any) -> ingest_rule_pb2.UpdateIngestRuleResponse:
        """Update name, enabled state, filters or action, optionally rotating the secret.

        The update MERGES: it applies only what it carries, down to the
        individual filters and the individual parts of the action. Narrowing a
        rule to a new prefix is ``filters={"prefix": "raw/"}`` and nothing else
        — the suffix, content-type and size filters are untouched.

        Removing something rather than changing it takes the two clear flags.
        ``clear_filters=True`` empties the filter set before ``filters`` is
        applied, so on its own it widens the rule to everything in the bucket.
        ``clear_action=True`` replaces the action outright, and ``action`` must
        then be complete — at least one output and exactly one destination.
        That is the only way to drop an action's thumbnails or metadata, since
        a repeated or map field sent empty reads as "not sent". For the same
        reason ``managed=False`` does not turn managed storage off; it leaves
        the destination alone, so send ``output_origin_id`` instead.

        The whole response is returned: a rotation puts the new secret on it
        (once, and the previous secret keeps working for 24 hours), and
        switching a paused rule back on reports how many deliveries it declined
        while off in ``events_skipped_while_disabled``.
        """
        req = fill_from_dict(ingest_rule_pb2.UpdateIngestRuleRequest(), kwargs)
        return self._t.unary(_SERVICE, "Update", req, ingest_rule_pb2.UpdateIngestRuleResponse())

    def delete(self, id: str, opts: CallOptions | None = None) -> ingest_rule_pb2.IngestRule:
        """Delete a rule; its endpoint stops accepting events immediately.

        The events it already received are kept, and the rule as it stood at
        deletion is returned.
        """
        req = ingest_rule_pb2.DeleteIngestRuleRequest(id=id)
        return self._t.unary(
            _SERVICE, "Delete", req, ingest_rule_pb2.DeleteIngestRuleResponse(), opts
        ).rule

    def list_events(
        self,
        *,
        rule_id: str | None = None,
        status: int | str | None = None,
        app_id: str | None = None,
        limit: int | None = None,
        opts: CallOptions | None = None,
    ) -> Page[ingest_rule_pb2.StorageEvent]:
        """Every delivery received and what came of it, newest first.

        ``status`` accepts the simplified wire string (``"skipped"``) as well as
        the generated constant.
        """
        resolved_status = (
            None
            if status is None
            else resolve_enum(status, ingest_rule_pb2.StorageEventStatus.DESCRIPTOR)
        )

        def fetch(cursor: str | None) -> PageContents[ingest_rule_pb2.StorageEvent]:
            req = ingest_rule_pb2.ListIngestEventsRequest()
            if rule_id is not None:
                req.rule_id = rule_id
            if resolved_status is not None:
                # resolve_enum returns a plain int; the field is typed as the enum.
                req.status = cast("ingest_rule_pb2.StorageEventStatus", resolved_status)
            if app_id is not None:
                req.app_id = app_id
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(
                _SERVICE, "ListEvents", req, ingest_rule_pb2.ListIngestEventsResponse(), opts
            )
            return PageContents(
                items=list(res.events), next_cursor=res.pagination.next_cursor or None
            )

        return Page(fetch)

    def test(self, **kwargs: Any) -> ingest_rule_pb2.TestIngestRuleResponse:
        """Dry-run an object key against a rule. Nothing is stored, no job is created.

        Reports whether the filters match and, when they do, the exact job
        request the rule would submit. Supply ``etag`` when you want the
        preview to name the idempotency key a real delivery would carry — the
        key is derived from it.
        """
        req = fill_from_dict(ingest_rule_pb2.TestIngestRuleRequest(), kwargs)
        return self._t.unary(_SERVICE, "Test", req, ingest_rule_pb2.TestIngestRuleResponse())

    def replay_event(
        self, event_id: str, opts: CallOptions | None = None
    ) -> ingest_rule_pb2.StorageEvent:
        """Re-queue a skipped or refused event (``sev_*``).

        Deduplication is permanent: re-sending the event, or re-uploading the
        same bytes, is absorbed and produces nothing. The event is reset rather
        than duplicated, so it keeps its id and its history.
        """
        req = ingest_rule_pb2.ReplayIngestEventRequest(event_id=event_id)
        return self._t.unary(
            _SERVICE, "ReplayEvent", req, ingest_rule_pb2.ReplayIngestEventResponse(), opts
        ).event
