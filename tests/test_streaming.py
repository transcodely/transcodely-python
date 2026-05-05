"""Tests for the watch() reconnect + heartbeat-filter wrapper."""

from __future__ import annotations

from typing import Generator, Iterable

import pytest

from transcodely.errors import APIConnectionError, NotFoundError
from transcodely.streaming import watch


def _gen(items: Iterable[dict]) -> Generator[dict, None, None]:
    for item in items:
        yield item


def _gen_then_raise(items: Iterable[dict], err: Exception) -> Generator[dict, None, None]:
    for item in items:
        yield item
    raise err


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip the random backoff sleep so tests run instantly."""
    monkeypatch.setattr("transcodely.streaming.time.sleep", lambda _s: None)


class TestWatch:
    def test_yields_events_in_order_when_no_filter(self) -> None:
        events = [
            {"kind": "snapshot", "n": 0},
            {"kind": "update", "n": 1},
            {"kind": "heartbeat", "n": 2},
        ]
        out = list(watch(lambda: _gen(events)))
        assert out == events

    def test_filters_heartbeats_with_predicate(self) -> None:
        events = [
            {"kind": "snapshot", "n": 0},
            {"kind": "heartbeat", "n": 1},
            {"kind": "update", "n": 2},
            {"kind": "heartbeat", "n": 3},
        ]
        out = list(watch(lambda: _gen(events), is_heartbeat=lambda e: e["kind"] == "heartbeat"))
        assert [e["n"] for e in out] == [0, 2]

    def test_include_heartbeats_overrides_filter(self) -> None:
        events = [
            {"kind": "snapshot", "n": 0},
            {"kind": "heartbeat", "n": 1},
        ]
        out = list(
            watch(
                lambda: _gen(events),
                is_heartbeat=lambda e: e["kind"] == "heartbeat",
                include_heartbeats=True,
            )
        )
        assert out == events

    def test_reconnects_on_api_connection_error(self) -> None:
        attempts = {"n": 0}

        def factory() -> Generator[dict, None, None]:
            attempts["n"] += 1
            if attempts["n"] == 1:
                raise APIConnectionError("transient")
            yield {"kind": "snapshot", "n": 99}

        out = list(watch(factory, max_reconnects=3))
        assert out == [{"kind": "snapshot", "n": 99}]
        assert attempts["n"] == 2

    def test_does_not_reconnect_on_non_connection_error(self) -> None:
        def factory() -> Generator[dict, None, None]:
            raise NotFoundError("missing")
            yield  # unreachable, makes this a generator

        with pytest.raises(NotFoundError):
            list(watch(factory))

    def test_gives_up_after_max_reconnects(self) -> None:
        attempts = {"n": 0}

        def factory() -> Generator[dict, None, None]:
            attempts["n"] += 1
            raise APIConnectionError("down")
            yield  # unreachable

        with pytest.raises(APIConnectionError):
            list(watch(factory, max_reconnects=2))
        assert attempts["n"] == 3  # initial + 2 reconnects

    def test_reconnects_after_partial_stream_then_failure(self) -> None:
        attempts = {"n": 0}

        def factory() -> Generator[dict, None, None]:
            attempts["n"] += 1
            if attempts["n"] == 1:
                yield from _gen_then_raise(
                    [{"kind": "snapshot", "n": 0}, {"kind": "update", "n": 1}],
                    APIConnectionError("dropped mid-stream"),
                )
                return
            yield {"kind": "snapshot", "n": 2}

        out = list(watch(factory))
        assert [e["n"] for e in out] == [0, 1, 2]
