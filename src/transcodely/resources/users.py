"""User resource."""

from __future__ import annotations

from typing import Any, Optional, Union, cast

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import user_pb2
from ._helpers import assign_pagination, fill_from_dict, resolve_enum

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
        status: Optional[Union[int, str]] = None,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[user_pb2.User]:
        """List users, optionally filtered by ``status``.

        ``status`` accepts the simplified lowercase string (``"active"``,
        ``"suspended"``, ``"deleted"``) or the raw ``UserStatus`` int.
        """
        status_value = (
            resolve_enum(status, user_pb2.UserStatus.DESCRIPTOR) if status is not None else None
        )

        def fetch(cursor: Optional[str]) -> PageContents[user_pb2.User]:
            req = user_pb2.ListUsersRequest()
            if status_value is not None:
                # resolve_enum returns a plain int; the field is typed as the enum.
                req.status = cast("user_pb2.UserStatus", status_value)
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, user_pb2.ListUsersResponse(), opts)
            return PageContents(
                items=list(res.users), next_cursor=res.pagination.next_cursor or None
            )

        return Page(fetch)
