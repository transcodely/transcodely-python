"""App resource."""

from __future__ import annotations

from typing import Any, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import app_pb2
from ._helpers import assign_pagination, fill_from_dict

_SERVICE = "transcodely.v1.AppService"


class Apps:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(self, **kwargs: Any) -> app_pb2.App:
        req = fill_from_dict(app_pb2.CreateAppRequest(), kwargs)
        return self._t.unary(_SERVICE, "Create", req, app_pb2.CreateAppResponse()).app

    def get(self, id: str, opts: Optional[CallOptions] = None) -> app_pb2.App:
        req = app_pb2.GetAppRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, app_pb2.GetAppResponse(), opts).app

    def update(self, **kwargs: Any) -> app_pb2.App:
        req = fill_from_dict(app_pb2.UpdateAppRequest(), kwargs)
        return self._t.unary(_SERVICE, "Update", req, app_pb2.UpdateAppResponse()).app

    def list(
        self,
        *,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[app_pb2.App]:
        def fetch(cursor: Optional[str]) -> PageContents[app_pb2.App]:
            req = app_pb2.ListAppsRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, app_pb2.ListAppsResponse(), opts)
            return PageContents(
                items=list(res.apps), next_cursor=res.pagination.next_cursor or None
            )

        return Page(fetch)

    def archive(self, id: str, opts: Optional[CallOptions] = None) -> app_pb2.App:
        req = app_pb2.ArchiveAppRequest(id=id)
        return self._t.unary(_SERVICE, "Archive", req, app_pb2.ArchiveAppResponse(), opts).app

    def enable_hosting(self, **kwargs: Any) -> app_pb2.EnableHostingResponse:
        req = fill_from_dict(app_pb2.EnableHostingRequest(), kwargs)
        return self._t.unary(_SERVICE, "EnableHosting", req, app_pb2.EnableHostingResponse())

    def update_hosting_config(self, **kwargs: Any) -> app_pb2.UpdateHostingConfigResponse:
        req = fill_from_dict(app_pb2.UpdateHostingConfigRequest(), kwargs)
        return self._t.unary(
            _SERVICE, "UpdateHostingConfig", req, app_pb2.UpdateHostingConfigResponse()
        )
