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
