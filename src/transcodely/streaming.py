"""Watch-stream wrapper with auto-reconnect and HEARTBEAT filtering."""

from __future__ import annotations

import random
import time
from typing import Callable, Generator, Optional, TypeVar

from .errors import APIConnectionError

T = TypeVar("T")


def watch(
    factory: Callable[[], Generator[T, None, None]],
    *,
    is_heartbeat: Optional[Callable[[T], bool]] = None,
    include_heartbeats: bool = False,
    max_reconnects: int = 5,
) -> Generator[T, None, None]:
    """Wrap a stream factory with reconnect + heartbeat-filter semantics.

    ``factory`` is called once per connection; if it raises an
    :class:`APIConnectionError` we re-invoke it with backoff up to
    ``max_reconnects`` times. Watch RPCs are idempotent — every reconnect
    starts with a SNAPSHOT event so resumption is safe.
    """
    attempt = 0
    while True:
        try:
            for event in factory():
                if not include_heartbeats and is_heartbeat is not None and is_heartbeat(event):
                    continue
                yield event
            return
        except APIConnectionError:
            attempt += 1
            if attempt > max_reconnects:
                raise
            _backoff(attempt)


def _backoff(attempt: int) -> None:
    base = 0.5
    cap = 5.0
    expo = min(cap, base * 2 ** (attempt - 1))
    time.sleep(expo * (0.5 + random.random() * 0.5))
