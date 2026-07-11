"""Verify a signed webhook delivery and dispatch on the event type.

The framework is irrelevant — what matters is passing the *raw* request body
(bytes or str, exactly as received) and the ``Transcodely-Signature`` header to
``construct_event``. Below is a dependency-free WSGI handler so the example runs
anywhere; swap in Flask/FastAPI/Django request objects as needed.
"""

import os

from transcodely import (
    Event,
    WebhookSignatureError,
    WebhookTimestampError,
    construct_event,
)

# Your endpoint's signing secret, from `client.webhook_endpoints.create(...)`.
WEBHOOK_SECRET = os.environ.get("TRANSCODELY_WEBHOOK_SECRET", "whsec_...")


def handle_event(event: Event) -> None:
    """Dispatch on event.type. event.data is the decoded resource."""
    if event.type == "job.succeeded":
        print(f"job {event.data.id} finished")
    elif event.type == "job.failed":
        print(f"job {event.data.id} failed")
    elif event.type == "output.ready":
        print(f"output {event.data.id} ready: {event.data.output_url}")
    elif event.type == "video.uploaded":
        print(f"video {event.data.id} uploaded")
    else:
        # Forward-compatible: unknown future types still verify; data is a dict.
        print(f"unhandled event {event.type}")


def webhook_app(environ, start_response):  # type: ignore[no-untyped-def]
    """Minimal WSGI endpoint that verifies and processes one delivery."""
    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw_body = environ["wsgi.input"].read(length)  # raw bytes — never re-serialize
    sig_header = environ.get("HTTP_TRANSCODELY_SIGNATURE", "")

    try:
        event = construct_event(raw_body, sig_header, WEBHOOK_SECRET)
    except (WebhookSignatureError, WebhookTimestampError) as err:
        # Reject unverified or replayed deliveries.
        start_response("400 Bad Request", [("Content-Type", "text/plain")])
        return [f"signature check failed: {err}".encode()]

    handle_event(event)

    # Ack quickly (2xx) so the platform marks the delivery succeeded.
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"ok"]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    port = int(os.environ.get("PORT", "8000"))
    print(f"Listening for webhooks on http://localhost:{port}")
    make_server("", port, webhook_app).serve_forever()
