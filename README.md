# transcodely

Official Python SDK for the [Transcodely](https://transcodely.com) video transcoding API.

```bash
pip install transcodely
```

## Quick start

```python
import os
from transcodely import Transcodely

with Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"]) as client:
    job = client.jobs.create(
        input_url="https://example.com/source.mp4",
        outputs=[{
            "type": "hls",
            "video": [
                {"codec": "h264", "resolution": "1080p"},
                {"codec": "h264", "resolution": "720p"},
            ],
        }],
    )
    print(job.id)  # "job_a1b2c3d4e5f6"

    for event in client.jobs.watch(job.id):
        print(event.job.status, event.job.progress)
        if event.job.status == 4:  # JOB_STATUS_COMPLETED
            break
```

The simplified-string form (`"hls"`, `"h264"`, `"1080p"`) is what the API actually emits over the wire — the SDK round-trips it transparently to and from the proto enum integers.

## Authentication

```python
client = Transcodely(api_key=os.environ["TRANSCODELY_API_KEY"])
```

Test-mode (`ak_test_*`) and live-mode (`ak_live_*`) keys hit the same base URL — the environment is encoded in the prefix.

## Resources

```python
client.jobs            # create / get / list / cancel / confirm / watch
client.videos          # upload helpers, multipart, get / list / update / delete / watch
client.presets         # create / get / get_by_slug / list / update / duplicate / archive
client.origins         # create / get / list / update / validate / archive
client.apps            # create / get / list / update / archive / enable_hosting
client.api_keys        # create / get / list / revoke
client.organizations   # create / get / list / update / check_slug
client.memberships     # list / get / update_role / remove
client.users           # get_me / get / list / update_me
client.health          # check
client.webhook_endpoints  # create / retrieve / update / delete / list / rotate_secret / send_test / list_deliveries / get_health
client.events          # retrieve / list / resend
client.webhooks        # construct_event / verify_signature (signature-verification helpers)
```

## Errors

All exceptions inherit from `TranscodelyError`:

```python
from transcodely import (
    Transcodely,
    TranscodelyError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
)

try:
    client.jobs.create(input_url=..., outputs=[...])
except InvalidRequestError as err:
    for v in err.errors:
        print(f"{v.field}: {v.description}")
except RateLimitError as err:
    time.sleep((err.retry_after_ms or 1000) / 1000)
except TranscodelyError as err:
    print(f"[{err.request_id}] {err.code}: {err}")
```

| Class | Status | When |
|---|---|---|
| `APIConnectionError` | — | Network / DNS / TLS failure |
| `APIError` | 5xx | Server-side error |
| `AuthenticationError` | 401 | Bad / missing / revoked key |
| `PermissionError` | 403 | Authenticated but forbidden |
| `NotFoundError` | 404 | Resource doesn't exist |
| `ConflictError` | 409 | Idempotency conflict, slug taken |
| `RateLimitError` | 429 | Carries `retry_after_ms` |
| `InvalidRequestError` | 400 | Carries `errors: list[FieldViolation]` |
| `PreconditionError` | 412 | Wrong state (e.g. job not cancelable) |

Every error carries `request_id`, `code`, `http_status`, and `raw` for debugging.

Webhook verification raises `WebhookError` (or a subclass) — see [Webhooks](#webhooks).

## Pagination

```python
# One page
page = client.jobs.list(limit=50)
print(page.items, page.next_cursor)

# All items, automatically across pages
for job in client.jobs.list(limit=50).auto_paging_iter():
    print(job.id)
```

## Idempotency

`jobs.create` accepts `idempotency_key`. If you don't pass one, the SDK generates a UUID v4 so retries are safe by default. For cross-process safety, pass your own:

```python
client.jobs.create(
    input_url="...",
    outputs=[...],
    idempotency_key="create-job-for-asset-12345",
)
```

For all other write methods, the SDK ships an `Idempotency-Key` HTTP header automatically.

## Streaming watch

```python
for event in client.jobs.watch(job.id):
    print(event.event, event.job.status, event.job.progress)
```

The SDK auto-reconnects on transient network failures — Watch is read-only and re-emits a SNAPSHOT on every reconnect. HEARTBEAT events are filtered by default.

## Webhooks

Verify a signed delivery and get back a typed `Event`. Pass the **raw** request body (bytes or str — do not re-serialize) and the `Transcodely-Signature` header:

```python
from transcodely import construct_event, WebhookSignatureError

try:
    event = construct_event(
        request.body,                       # raw bytes/str, exactly as received
        request.headers["transcodely-signature"],
        "whsec_...",                        # your endpoint's signing secret
    )
except WebhookSignatureError:
    return Response(status_code=400)

# `event.data` is the decoded resource (a Job, JobOutput, Video, or App).
if event.type == "job.succeeded":
    print("job done:", event.data.id)
elif event.type == "video.uploaded":
    print("new video:", event.data.id)
```

`construct_event` also accepts a **list** of secrets so deliveries keep verifying during a secret rotation's overlap window:

```python
event = construct_event(body, sig_header, ["whsec_previous", "whsec_current"])
```

Tuning and errors:

- `tolerance` (default `300` seconds) bounds clock skew / replay; widen or narrow it per call.
- `WebhookSignatureError` — header malformed or no signature matched.
- `WebhookTimestampError` — timestamp outside the tolerance window.
- `WebhookPayloadError` — body isn't valid JSON or doesn't match the event envelope.

All three inherit from `WebhookError`. `client.webhooks.construct_event(...)` is an alias for the module-level function.

Manage endpoints and replay events via the API:

```python
endpoint = client.webhook_endpoints.create(
    app_id="app_123",
    url="https://example.com/hooks/transcodely",
    enabled_events=["job.succeeded", "job.failed"],   # or ["*"] for all
)
print(endpoint.secret)   # shown only on create + rotate_secret — store it now

# The same typed Event, fetched from the API instead of an HTTP delivery:
event = client.events.retrieve("evt_123")
for event in client.events.list(app_id="app_123").auto_paging_iter():
    print(event.type, event.id)

client.events.resend("evt_123")   # re-queue delivery to all subscribed endpoints
```

The 13 event types are `job.created`, `job.succeeded`, `job.failed`, `job.canceled`, `job.progress`, `output.created`, `output.ready`, `output.failed`, `output.progress`, `video.uploaded`, `video.deleted`, `app.created`, and `app.updated`. Subscribe to `"*"` to receive all of them (including ones added later). An unrecognized future type still verifies; its `event.data` is left as a plain `dict`.

## Configuration

```python
Transcodely(
    api_key,                    # required
    base_url=None,              # default: https://api.transcodely.com
    timeout=30.0,               # seconds
    max_retries=3,
    api_version=None,           # override the pinned API version
    default_headers=None,       # dict, sent on every request
    http_client=None,           # custom httpx.Client
    logger=None,                # callable(LogEvent)
)
```

## Request IDs

```python
client.jobs.get("job_x")
print(client.last_request_id)  # "req_*"
```

Errors also carry the request ID via `err.request_id` for log correlation.

## Versioning

The SDK follows semver, starting at `0.1.0`. Breaking changes are allowed on minor bumps until `1.0.0`. Each release pins a specific calendar-versioned API (`Transcodely.API_VERSION`) and sends `Transcodely-Version` on every request.

## License

[MIT](LICENSE).
