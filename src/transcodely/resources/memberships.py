"""Membership resource."""

from __future__ import annotations

from typing import Any, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import membership_pb2
from ._helpers import assign_pagination, fill_from_dict

_SERVICE = "transcodely.v1.MembershipService"


class Memberships:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def list(
        self,
        *,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[membership_pb2.MembershipWithUser]:
        def fetch(cursor: Optional[str]) -> PageContents[membership_pb2.MembershipWithUser]:
            req = membership_pb2.ListMembershipsRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, membership_pb2.ListMembershipsResponse(), opts)
            return PageContents(items=list(res.memberships), next_cursor=res.pagination.next_cursor or None)

        return Page(fetch)

    def get(self, id: str, opts: Optional[CallOptions] = None) -> membership_pb2.MembershipWithUser:
        req = membership_pb2.GetMembershipRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, membership_pb2.GetMembershipResponse(), opts).membership

    def update_role(self, **kwargs: Any) -> membership_pb2.Membership:
        req = fill_from_dict(membership_pb2.UpdateMembershipRoleRequest(), kwargs)
        return self._t.unary(
            _SERVICE,
            "UpdateRole",
            req,
            membership_pb2.UpdateMembershipRoleResponse(),
        ).membership

    def remove(self, id: str, opts: Optional[CallOptions] = None) -> None:
        req = membership_pb2.RemoveMembershipRequest(id=id)
        self._t.unary(_SERVICE, "Remove", req, membership_pb2.RemoveMembershipResponse(), opts)
