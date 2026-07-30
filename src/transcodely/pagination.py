"""Cursor pagination helper.

Every ``list`` method returns a :class:`Page` you can iterate manually or via
``.auto_paging_iter()`` to walk every result lazily.
"""

from __future__ import annotations

from collections.abc import Callable, Generator, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class PageContents(Generic[T]):
    items: list[T]
    next_cursor: str | None


class Page(Generic[T]):
    """A single page of results plus an opt-in iterator across all pages."""

    def __init__(self, fetcher: Callable[[str | None], PageContents[T]]) -> None:
        self._fetcher = fetcher
        self._first: PageContents[T] | None = None

    @property
    def items(self) -> list[T]:
        return self._first_page().items

    @property
    def next_cursor(self) -> str | None:
        return self._first_page().next_cursor

    def __iter__(self) -> Iterator[T]:
        return iter(self._first_page().items)

    def auto_paging_iter(self) -> Generator[T, None, None]:
        """Yield every item, transparently fetching subsequent pages."""
        cursor: str | None = None
        while True:
            page = self._fetcher(cursor)
            yield from page.items
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    def _first_page(self) -> PageContents[T]:
        if self._first is None:
            self._first = self._fetcher(None)
        return self._first
