"""Preset resource."""

from __future__ import annotations

from typing import Any

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import preset_pb2
from ._helpers import assign_pagination, fill_from_dict

_SERVICE = "transcodely.v1.PresetService"


class Presets:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(self, **kwargs: Any) -> preset_pb2.Preset:
        req = fill_from_dict(preset_pb2.CreatePresetRequest(), kwargs)
        return self._t.unary(_SERVICE, "Create", req, preset_pb2.CreatePresetResponse()).preset

    def get(self, id: str, opts: CallOptions | None = None) -> preset_pb2.Preset:
        req = preset_pb2.GetPresetRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, preset_pb2.GetPresetResponse(), opts).preset

    def get_by_slug(self, slug: str, opts: CallOptions | None = None) -> preset_pb2.Preset:
        req = preset_pb2.GetPresetBySlugRequest(slug=slug)
        return self._t.unary(
            _SERVICE, "GetBySlug", req, preset_pb2.GetPresetBySlugResponse(), opts
        ).preset

    def list(
        self,
        *,
        limit: int | None = None,
        opts: CallOptions | None = None,
    ) -> Page[preset_pb2.Preset]:
        def fetch(cursor: str | None) -> PageContents[preset_pb2.Preset]:
            req = preset_pb2.ListPresetsRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, preset_pb2.ListPresetsResponse(), opts)
            return PageContents(
                items=list(res.presets), next_cursor=res.pagination.next_cursor or None
            )

        return Page(fetch)

    def update(self, **kwargs: Any) -> preset_pb2.Preset:
        req = fill_from_dict(preset_pb2.UpdatePresetRequest(), kwargs)
        return self._t.unary(_SERVICE, "Update", req, preset_pb2.UpdatePresetResponse()).preset

    def duplicate(self, **kwargs: Any) -> preset_pb2.Preset:
        req = fill_from_dict(preset_pb2.DuplicatePresetRequest(), kwargs)
        return self._t.unary(
            _SERVICE, "Duplicate", req, preset_pb2.DuplicatePresetResponse()
        ).preset

    def archive(self, id: str, opts: CallOptions | None = None) -> preset_pb2.Preset:
        req = preset_pb2.ArchivePresetRequest(id=id)
        return self._t.unary(
            _SERVICE, "Archive", req, preset_pb2.ArchivePresetResponse(), opts
        ).preset
