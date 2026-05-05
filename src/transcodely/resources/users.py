"""User resource."""

from __future__ import annotations

from typing import Any, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import user_pb2
from ._helpers import assign_pagination, fill_from_dict

_SERVICE = "transcodely.v1.UserService"


class Users:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def get_me(self, opts: Optional[CallOptions] = None) -> user_pb2.UserWithOrganizations:
        """Returns the authenticated user enriched with org memberships."""
        req = user_pb2.GetMeRequest()
        return self._t.unary(_SERVICE, "GetMe", req, user_pb2.GetMeResponse(), opts).user

    def update_me(self, **kwargs: Any) -> user_pb2.User:
        req = fill_from_dict(user_pb2.UpdateMeRequest(), kwargs)
        return self._t.unary(_SERVICE, "UpdateMe", req, user_pb2.UpdateMeResponse()).user

    def get(self, id: str, opts: Optional[CallOptions] = None) -> user_pb2.User:
        req = user_pb2.GetUserRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, user_pb2.GetUserResponse(), opts).user

    def list(
        self,
        *,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[user_pb2.User]:
        def fetch(cursor: Optional[str]) -> PageContents[user_pb2.User]:
            req = user_pb2.ListUsersRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, user_pb2.ListUsersResponse(), opts)
            return PageContents(items=list(res.users), next_cursor=res.pagination.next_cursor or None)

        return Page(fetch)
