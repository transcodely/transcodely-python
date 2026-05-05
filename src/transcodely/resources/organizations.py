"""Organization resource."""

from __future__ import annotations

from typing import Any, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import organization_pb2
from ._helpers import assign_pagination, fill_from_dict

_SERVICE = "transcodely.v1.OrganizationService"


class Organizations:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def check_slug(self, slug: str, opts: Optional[CallOptions] = None) -> organization_pb2.CheckSlugResponse:
        req = organization_pb2.CheckSlugRequest(slug=slug)
        return self._t.unary(_SERVICE, "CheckSlug", req, organization_pb2.CheckSlugResponse(), opts)

    def create(self, **kwargs: Any) -> organization_pb2.Organization:
        req = fill_from_dict(organization_pb2.CreateOrganizationRequest(), kwargs)
        return self._t.unary(
            _SERVICE,
            "Create",
            req,
            organization_pb2.CreateOrganizationResponse(),
        ).organization

    def get(self, id_or_slug: str, opts: Optional[CallOptions] = None) -> organization_pb2.Organization:
        """Look up by ID (``org_*``) or slug."""
        req = organization_pb2.GetOrganizationRequest(id_or_slug=id_or_slug)
        return self._t.unary(
            _SERVICE,
            "Get",
            req,
            organization_pb2.GetOrganizationResponse(),
            opts,
        ).organization

    def update(self, **kwargs: Any) -> organization_pb2.Organization:
        req = fill_from_dict(organization_pb2.UpdateOrganizationRequest(), kwargs)
        return self._t.unary(
            _SERVICE,
            "Update",
            req,
            organization_pb2.UpdateOrganizationResponse(),
        ).organization

    def list(
        self,
        *,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[organization_pb2.Organization]:
        def fetch(cursor: Optional[str]) -> PageContents[organization_pb2.Organization]:
            req = organization_pb2.ListOrganizationsRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, organization_pb2.ListOrganizationsResponse(), opts)
            return PageContents(
                items=list(res.organizations),
                next_cursor=res.pagination.next_cursor or None,
            )

        return Page(fetch)
