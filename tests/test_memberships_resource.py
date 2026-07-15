"""Tests for the Memberships resource list-status filter.

Mirrors the jobs.list status tests: ``status`` accepts the simplified lowercase
string ("active"/"invited"/"suspended") or the raw MembershipStatus int.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

import pytest

from transcodely.resources.memberships import Memberships
from transcodely.v1 import common_pb2, membership_pb2


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


def _list_first_request(**kwargs: Any) -> membership_pb2.ListMembershipsRequest:
    resp = membership_pb2.ListMembershipsResponse(
        memberships=[membership_pb2.MembershipWithUser(user_email="a@x.test")],
        pagination=common_pb2.PaginationResponse(next_cursor=""),
    )
    t = FakeTransport({"List": resp})
    Memberships(t).list(
        **kwargs
    ).items  # `.items` triggers the first fetch  # type: ignore[arg-type]
    return t.calls[0][1]


class TestMembershipsList:
    def test_no_status_leaves_field_unset(self) -> None:
        req = _list_first_request()
        assert req.HasField("status") is False

    def test_status_as_lowercase_string(self) -> None:
        req = _list_first_request(status="active")
        assert req.status == membership_pb2.MEMBERSHIP_STATUS_ACTIVE

    def test_status_invited_and_suspended_strings(self) -> None:
        assert (
            _list_first_request(status="invited").status == membership_pb2.MEMBERSHIP_STATUS_INVITED
        )
        assert (
            _list_first_request(status="suspended").status
            == membership_pb2.MEMBERSHIP_STATUS_SUSPENDED
        )

    def test_status_as_int_backward_compatible(self) -> None:
        req = _list_first_request(status=membership_pb2.MEMBERSHIP_STATUS_INVITED)
        assert req.status == membership_pb2.MEMBERSHIP_STATUS_INVITED

    def test_status_as_canonical_enum_name(self) -> None:
        req = _list_first_request(status="MEMBERSHIP_STATUS_SUSPENDED")
        assert req.status == membership_pb2.MEMBERSHIP_STATUS_SUSPENDED

    def test_limit_still_passes_through(self) -> None:
        req = _list_first_request(status="active", limit=20)
        assert req.pagination.limit == 20
        assert req.status == membership_pb2.MEMBERSHIP_STATUS_ACTIVE

    def test_unknown_status_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown MembershipStatus value"):
            _list_first_request(status="bogus")

    def test_status_persists_across_auto_paging(self) -> None:
        page1 = membership_pb2.ListMembershipsResponse(
            memberships=[membership_pb2.MembershipWithUser(user_email="a@x.test")],
            pagination=common_pb2.PaginationResponse(next_cursor="c1"),
        )
        page2 = membership_pb2.ListMembershipsResponse(
            memberships=[membership_pb2.MembershipWithUser(user_email="b@x.test")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        )
        t = FakeTransport({"List": lambda req: page2 if req.pagination.cursor == "c1" else page1})
        page = Memberships(t).list(status="invited")  # type: ignore[arg-type]
        assert [m.user_email for m in page.auto_paging_iter()] == ["a@x.test", "b@x.test"]
        assert t.calls[0][1].status == membership_pb2.MEMBERSHIP_STATUS_INVITED
        assert t.calls[1][1].status == membership_pb2.MEMBERSHIP_STATUS_INVITED
        assert t.calls[1][1].pagination.cursor == "c1"
