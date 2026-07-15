"""Tests for the Users resource list-status filter.

Mirrors the jobs.list status tests: ``status`` accepts the simplified lowercase
string ("active") or the raw UserStatus int, routed through resolve_enum.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

import pytest

from transcodely.resources.users import Users
from transcodely.v1 import common_pb2, user_pb2


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


def _list_first_request(**kwargs: Any) -> user_pb2.ListUsersRequest:
    resp = user_pb2.ListUsersResponse(
        users=[user_pb2.User(id="usr_1")],
        pagination=common_pb2.PaginationResponse(next_cursor=""),
    )
    t = FakeTransport({"List": resp})
    Users(t).list(**kwargs).items  # `.items` triggers the first fetch  # type: ignore[arg-type]
    return t.calls[0][1]


class TestUsersList:
    def test_no_status_leaves_field_unset(self) -> None:
        req = _list_first_request()
        assert req.HasField("status") is False

    def test_status_as_lowercase_string(self) -> None:
        req = _list_first_request(status="active")
        assert req.status == user_pb2.USER_STATUS_ACTIVE

    def test_status_suspended_and_deleted_strings(self) -> None:
        assert _list_first_request(status="suspended").status == user_pb2.USER_STATUS_SUSPENDED
        assert _list_first_request(status="deleted").status == user_pb2.USER_STATUS_DELETED

    def test_status_as_int_backward_compatible(self) -> None:
        req = _list_first_request(status=user_pb2.USER_STATUS_SUSPENDED)
        assert req.status == user_pb2.USER_STATUS_SUSPENDED

    def test_status_as_canonical_enum_name(self) -> None:
        req = _list_first_request(status="USER_STATUS_ACTIVE")
        assert req.status == user_pb2.USER_STATUS_ACTIVE

    def test_limit_still_passes_through(self) -> None:
        req = _list_first_request(status="active", limit=20)
        assert req.pagination.limit == 20
        assert req.status == user_pb2.USER_STATUS_ACTIVE

    def test_unknown_status_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown UserStatus value"):
            _list_first_request(status="bogus")

    def test_status_persists_across_auto_paging(self) -> None:
        page1 = user_pb2.ListUsersResponse(
            users=[user_pb2.User(id="usr_1")],
            pagination=common_pb2.PaginationResponse(next_cursor="c1"),
        )
        page2 = user_pb2.ListUsersResponse(
            users=[user_pb2.User(id="usr_2")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        )
        t = FakeTransport({"List": lambda req: page2 if req.pagination.cursor == "c1" else page1})
        page = Users(t).list(status="active")  # type: ignore[arg-type]
        assert [u.id for u in page.auto_paging_iter()] == ["usr_1", "usr_2"]
        assert t.calls[0][1].status == user_pb2.USER_STATUS_ACTIVE
        assert t.calls[1][1].status == user_pb2.USER_STATUS_ACTIVE
        assert t.calls[1][1].pagination.cursor == "c1"
