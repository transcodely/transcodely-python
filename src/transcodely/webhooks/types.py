"""Public types for the webhook surface.

Python port of the TypeScript SDK's ``webhooks/types.ts`` — the customer-facing
:class:`Event` shape plus the resource-decoder table shared between the verify
helper (:func:`transcodely.construct_event`) and the ``client.events`` resource
bridge. Both paths converge on the same :class:`Event`, so a ``job.succeeded``
handler behaves identically whether the event arrived over an HTTP delivery or
was pulled from :meth:`Events.retrieve`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal, Mapping, Optional

from google.protobuf.message import Message

from ..resources._helpers import fill_from_dict
from ..v1 import app_pb2, job_pb2, video_pb2

#: The 13 canonical event types the webhook system can emit, mirroring the API's
#: ``domain.WebhookEventTypes()``. The ``"*"`` wildcard is intentionally absent —
#: it is a subscription value only, never the ``type`` of an emitted event. Used
#: for annotations and documentation; the ``Event.type`` field is a plain ``str``
#: so an older SDK still parses a ``type`` the API has since added (forward
#: compatibility).
EventType = Literal[
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
    "video.deleted",
    "app.created",
    "app.updated",
]


@dataclass(frozen=True)
class EventRequest:
    """The originating API request that triggered an event, if known."""

    #: Request ID (``req_*``), or ``None`` for events emitted outside a request
    #: scope (worker-callback events like ``job.succeeded`` and every test send).
    id: Optional[str]
    #: Idempotency key the original request carried, or ``None``.
    idempotency_key: Optional[str]


@dataclass(frozen=True, kw_only=True)
class Event:
    """A webhook event, unified across the HTTP delivery envelope and the API.

    ``data`` carries the decoded resource snapshot — a :class:`~transcodely.Job`,
    :class:`~transcodely.JobOutput`, :class:`~transcodely.Video`, or
    :class:`~transcodely.App` for a known ``type``, or the raw ``dict`` for an
    unrecognized one (forward compatibility).
    """

    #: Event ID (``evt_*``).
    id: str
    #: Resource discriminator. Always ``"event"``.
    object: str = "event"
    #: API version at emit time (e.g. ``"2026-05-23"``). Frozen for the event's life.
    api_version: str
    #: RFC 3339 UTC timestamp of when the event was created.
    created: str
    #: Event type, e.g. ``"job.succeeded"``. See :data:`EventType`.
    type: str
    #: The decoded resource snapshot (a proto message, or ``dict`` for unknown types).
    data: Any
    #: ``True`` for production-mode events. Reserved for a future test-mode concept.
    livemode: bool
    #: Delivery attempts still pending across all subscribed endpoints.
    pending_webhooks: int
    #: The originating API request.
    request: EventRequest


#: Alias matching the TypeScript SDK's ``WebhookEvent`` name.
WebhookEvent = Event

Decoder = Callable[[Mapping[str, Any]], Message]

#: Event-type prefix → resource decoder. Shared by ``construct_event`` (verify
#: path; ``data`` arrives pre-parsed) and the ``events`` resource bridge (API
#: path; ``data`` arrives as a JSON string on the proto ``Event``). ``output.``
#: is listed first to make the intent explicit; the prefixes are disjoint.
RESOURCE_DECODERS: list[tuple[str, Decoder]] = [
    ("output.", lambda d: fill_from_dict(job_pb2.JobOutput(), d)),
    ("job.", lambda d: fill_from_dict(job_pb2.Job(), d)),
    ("video.", lambda d: fill_from_dict(video_pb2.Video(), d)),
    ("app.", lambda d: fill_from_dict(app_pb2.App(), d)),
]


def decoder_for_type(type: str) -> Optional[Decoder]:
    """Return a resource decoder for ``type``, or ``None`` if the type is unknown."""
    for prefix, decode in RESOURCE_DECODERS:
        if type.startswith(prefix):
            return decode
    return None


__all__ = [
    "Event",
    "EventRequest",
    "EventType",
    "RESOURCE_DECODERS",
    "WebhookEvent",
    "decoder_for_type",
]
