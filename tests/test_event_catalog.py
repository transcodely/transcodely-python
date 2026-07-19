"""Guard the webhook event catalog against drift from the API.

``EventType`` in ``transcodely.webhooks.types`` is the one hand-maintained mirror
of the API's emittable event catalog (``api/internal/domain/webhook.go``,
``WebhookEventTypes()`` / ``IsValidWebhookEventType``). If the API adds or drops a
type and this literal isn't updated in lockstep, these tests fail.

Concretely, this would have caught the ``job.updated`` drift: the API dropped it
(Stripe-style terminal-only job events; ``webhook_test.go`` asserts
``IsValidWebhookEventType("job.updated") == false``) while the SDK still declared
it here.
"""

from __future__ import annotations

from typing import get_args

from transcodely import EventType
from transcodely.webhooks.types import RESOURCE_DECODERS, decoder_for_type

# The canonical catalog, mirrored verbatim from the API's
# domain.WebhookEventTypes(). The "*" wildcard is intentionally excluded — it is a
# subscription value only, never the type of an emitted event.
CANONICAL_EVENT_TYPES = {
    "job.created",
    "job.succeeded",
    "job.failed",
    "job.canceled",
    "job.progress",
    "output.created",
    "output.ready",
    "output.failed",
    "output.progress",
    "video.uploaded",
    "video.ready",
    "video.failed",
    "video.deleted",
    "app.created",
    "app.updated",
    "app.spend_limit_warning",
    "app.spend_limit_exceeded",
}

# The two spend-limit events share the "app." prefix but carry a notification
# payload, not a resource snapshot — they intentionally route to no resource
# decoder (their data stays the raw dict).
NOTIFICATION_EVENT_TYPES = {
    "app.spend_limit_warning",
    "app.spend_limit_exceeded",
}


def test_event_type_literal_matches_api_catalog() -> None:
    assert set(get_args(EventType)) == CANONICAL_EVENT_TYPES


def test_catalog_has_exactly_17_types() -> None:
    types = get_args(EventType)
    assert len(types) == 17
    # No accidental duplicates in the literal.
    assert len(set(types)) == 17


def test_job_updated_is_not_in_catalog() -> None:
    # Dropped by the API (terminal-only job events). Regression guard.
    assert "job.updated" not in get_args(EventType)


def test_wildcard_is_not_an_emitted_type() -> None:
    # "*" is a subscribe-only token, never an emitted event's type.
    assert "*" not in get_args(EventType)


def test_every_resource_event_type_has_a_resource_decoder() -> None:
    # RESOURCE_DECODERS is a second hand-maintained mirror (event-type prefix ->
    # resource). Every concrete resource-carrying type must route to a decoder,
    # so a newly added resource family can't silently fall through to the
    # raw-dict path. The notification events are the deliberate exception.
    for event_type in CANONICAL_EVENT_TYPES - NOTIFICATION_EVENT_TYPES:
        assert decoder_for_type(event_type) is not None, event_type


def test_notification_events_have_no_resource_decoder() -> None:
    # Spend-limit events carry a notification payload, not a resource snapshot,
    # so they must NOT decode via the App resource decoder — their data stays the
    # raw dict.
    for event_type in NOTIFICATION_EVENT_TYPES:
        assert decoder_for_type(event_type) is None, event_type


def test_resource_decoder_prefixes_cover_the_catalog() -> None:
    prefixes = {prefix for prefix, _ in RESOURCE_DECODERS}
    assert prefixes == {"job.", "output.", "video.", "app."}
