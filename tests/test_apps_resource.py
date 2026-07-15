"""Tests for the Apps resource list filters.

``apps.list`` must set the required ``org_id`` (ListAppsRequest.org_id is
required=true) and the optional ``include_archived`` bool, matching the
documented API and the TS/Go SDKs.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

from transcodely.resources.apps import Apps
from transcodely.v1 import app_pb2, common_pb2


class FakeTransport:
    """Duck-typed stand-in for Transport that returns canned responses per method."""

    def __init__(self, responses: dict[str, Union[Any, Callable[[Any], Any]]]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self,
        service_name: str,
        method_name: str,
        request: Any,
        response: Any,
        opts: Optional[Any] = None,
    ) -> Any:
        self.calls.append((method_name, request))
        r = self._responses[method_name]
        return r(request) if callable(r) else r


def _list_first_request(**kwargs: Any) -> app_pb2.ListAppsRequest:
    resp = app_pb2.ListAppsResponse(
        apps=[app_pb2.App(id="app_1")],
        pagination=common_pb2.PaginationResponse(next_cursor=""),
    )
    t = FakeTransport({"List": resp})
    Apps(t).list(**kwargs).items  # `.items` triggers the first fetch  # type: ignore[arg-type]
    return t.calls[0][1]


class TestAppsList:
    def test_org_id_is_set(self) -> None:
        req = _list_first_request(org_id="org_a1b2c3d4e5")
        assert req.org_id == "org_a1b2c3d4e5"

    def test_include_archived_true(self) -> None:
        req = _list_first_request(org_id="org_a1b2c3d4e5", include_archived=True)
        assert req.include_archived is True

    def test_include_archived_false(self) -> None:
        req = _list_first_request(org_id="org_a1b2c3d4e5", include_archived=False)
        assert req.include_archived is False

    def test_limit_passes_through(self) -> None:
        req = _list_first_request(org_id="org_a1b2c3d4e5", limit=20)
        assert req.pagination.limit == 20

    def test_all_kwargs_together(self) -> None:
        req = _list_first_request(org_id="org_a1b2c3d4e5", limit=20, include_archived=False)
        assert req.org_id == "org_a1b2c3d4e5"
        assert req.pagination.limit == 20
        assert req.include_archived is False

    def test_org_id_omitted_left_empty_for_server_to_reject(self) -> None:
        # Thin client: no local required-field validation — the server enforces
        # ListAppsRequest.org_id (required=true).
        req = _list_first_request()
        assert req.org_id == ""

    def test_org_id_persists_across_auto_paging(self) -> None:
        page1 = app_pb2.ListAppsResponse(
            apps=[app_pb2.App(id="app_1")],
            pagination=common_pb2.PaginationResponse(next_cursor="c1"),
        )
        page2 = app_pb2.ListAppsResponse(
            apps=[app_pb2.App(id="app_2")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        )
        t = FakeTransport({"List": lambda req: page2 if req.pagination.cursor == "c1" else page1})
        page = Apps(t).list(org_id="org_a1b2c3d4e5", include_archived=True)  # type: ignore[arg-type]
        assert [a.id for a in page.auto_paging_iter()] == ["app_1", "app_2"]
        assert t.calls[0][1].org_id == "org_a1b2c3d4e5"
        assert t.calls[1][1].org_id == "org_a1b2c3d4e5"
        assert t.calls[1][1].include_archived is True
        assert t.calls[1][1].pagination.cursor == "c1"
