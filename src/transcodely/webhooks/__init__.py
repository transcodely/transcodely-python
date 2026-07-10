"""Public webhook surface.

The canonical entry point is the module-level :func:`construct_event` (also
re-exported from the top-level ``transcodely`` package). The :class:`Webhooks`
facade mirrors the TypeScript SDK so customer code can also read
``client.webhooks.construct_event(...)``.
"""

from __future__ import annotations

from .construct_event import construct_event
from .signature import DEFAULT_TOLERANCE_SECONDS, SIGNATURE_HEADER, verify_signature
from .types import Event, EventRequest, EventType, WebhookEvent


class Webhooks:
    """Stripe-style facade exposing the webhook verify helpers.

    Used as ``client.webhooks.construct_event(...)``. The verify helpers are
    pure functions (no transport needed); webhook errors are imported from
    ``transcodely`` / ``transcodely.errors`` like every other SDK exception.
    """

    construct_event = staticmethod(construct_event)
    verify_signature = staticmethod(verify_signature)


__all__ = [
    "DEFAULT_TOLERANCE_SECONDS",
    "SIGNATURE_HEADER",
    "Event",
    "EventRequest",
    "EventType",
    "WebhookEvent",
    "Webhooks",
    "construct_event",
    "verify_signature",
]
