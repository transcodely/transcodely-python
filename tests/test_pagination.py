"""Tests for the cursor-pagination helper."""

from __future__ import annotations

from typing import Optional

import pytest

from transcodely.pagination import Page, PageContents


def fake_pages(pages: list[PageContents[int]]):  # type: ignore[no-untyped-def]
    cursors: list[Optional[str]] = []
    i = {"n": 0}

    def fetch(cursor: Optional[str]) -> PageContents[int]:
        cursors.append(cursor)
        if i["n"] >= len(pages):
            raise RuntimeError("ran out of pages")
        page = pages[i["n"]]
        i["n"] += 1
        return page

    return fetch, cursors


class TestPage:
    def test_first_page_is_lazy_and_cached(self) -> None:
        calls = {"n": 0}

        def fetch(cursor: Optional[str]) -> PageContents[int]:
            calls["n"] += 1
            return PageContents(items=[1, 2, 3], next_cursor=None)

        page = Page(fetch)
        assert calls["n"] == 0  # constructor doesn't fetch
        assert page.items == [1, 2, 3]
        assert page.next_cursor is None
        assert calls["n"] == 1
        # Second access reuses the cache.
        assert page.items == [1, 2, 3]
        assert calls["n"] == 1

    def test_iter_walks_first_page_only(self) -> None:
        fetch, _ = fake_pages(
            [
                PageContents(items=[1, 2], next_cursor="c1"),
            ]
        )
        page = Page(fetch)
        assert list(page) == [1, 2]

    def test_auto_paging_iter_walks_all_pages_and_stops_on_empty_cursor(self) -> None:
        fetch, cursors = fake_pages(
            [
                PageContents(items=[1, 2], next_cursor="c1"),
                PageContents(items=[3, 4], next_cursor="c2"),
                PageContents(items=[5], next_cursor=None),
            ]
        )
        page = Page(fetch)
        assert list(page.auto_paging_iter()) == [1, 2, 3, 4, 5]
        assert cursors == [None, "c1", "c2"]

    def test_auto_paging_stops_immediately_on_empty_first_page(self) -> None:
        fetch, _ = fake_pages([PageContents(items=[], next_cursor=None)])
        page = Page(fetch)
        assert list(page.auto_paging_iter()) == []

    def test_auto_paging_propagates_fetcher_errors(self) -> None:
        def fetch(cursor: Optional[str]) -> PageContents[int]:
            if cursor is None:
                return PageContents(items=[1], next_cursor="c1")
            raise RuntimeError("boom")

        page = Page(fetch)
        it = page.auto_paging_iter()
        assert next(it) == 1
        with pytest.raises(RuntimeError, match="boom"):
            next(it)
