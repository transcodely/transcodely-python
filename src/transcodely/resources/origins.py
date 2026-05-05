"""Origin resource — input/output storage destinations."""

from __future__ import annotations

from typing import Any, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import origin_pb2
from ._helpers import assign_pagination, fill_from_dict

_SERVICE = "transcodely.v1.OriginService"


class Origins:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(self, **kwargs: Any) -> origin_pb2.Origin:
        req = fill_from_dict(origin_pb2.CreateOriginRequest(), kwargs)
        return self._t.unary(_SERVICE, "Create", req, origin_pb2.CreateOriginResponse()).origin

    def get(self, id: str, opts: Optional[CallOptions] = None) -> origin_pb2.Origin:
        req = origin_pb2.GetOriginRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, origin_pb2.GetOriginResponse(), opts).origin

    def list(
        self,
        *,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[origin_pb2.Origin]:
        def fetch(cursor: Optional[str]) -> PageContents[origin_pb2.Origin]:
            req = origin_pb2.ListOriginsRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, origin_pb2.ListOriginsResponse(), opts)
            return PageContents(
                items=list(res.origins), next_cursor=res.pagination.next_cursor or None
            )

        return Page(fetch)

    def update(self, **kwargs: Any) -> origin_pb2.Origin:
        req = fill_from_dict(origin_pb2.UpdateOriginRequest(), kwargs)
        return self._t.unary(_SERVICE, "Update", req, origin_pb2.UpdateOriginResponse()).origin

    def validate(self, **kwargs: Any) -> origin_pb2.ValidateOriginResponse:
        req = fill_from_dict(origin_pb2.ValidateOriginRequest(), kwargs)
        return self._t.unary(_SERVICE, "Validate", req, origin_pb2.ValidateOriginResponse())

    def archive(self, id: str, opts: Optional[CallOptions] = None) -> origin_pb2.Origin:
        req = origin_pb2.ArchiveOriginRequest(id=id)
        return self._t.unary(
            _SERVICE, "Archive", req, origin_pb2.ArchiveOriginResponse(), opts
        ).origin
