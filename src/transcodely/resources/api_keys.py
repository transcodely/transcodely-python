"""API key resource."""

from __future__ import annotations

from typing import Any, Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import api_key_pb2
from ._helpers import assign_pagination, fill_from_dict

_SERVICE = "transcodely.v1.APIKeyService"


class ApiKeys:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def create(self, **kwargs: Any) -> api_key_pb2.CreateAPIKeyResponse:
        """Create a new key. The full secret is only present on this response — store it safely."""
        req = fill_from_dict(api_key_pb2.CreateAPIKeyRequest(), kwargs)
        return self._t.unary(_SERVICE, "Create", req, api_key_pb2.CreateAPIKeyResponse())

    def get(self, id: str, opts: Optional[CallOptions] = None) -> api_key_pb2.APIKey:
        req = api_key_pb2.GetAPIKeyRequest(id=id)
        return self._t.unary(_SERVICE, "Get", req, api_key_pb2.GetAPIKeyResponse(), opts).api_key

    def list(
        self,
        *,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[api_key_pb2.APIKey]:
        def fetch(cursor: Optional[str]) -> PageContents[api_key_pb2.APIKey]:
            req = api_key_pb2.ListAPIKeysRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(_SERVICE, "List", req, api_key_pb2.ListAPIKeysResponse(), opts)
            return PageContents(
                items=list(res.api_keys), next_cursor=res.pagination.next_cursor or None
            )

        return Page(fetch)

    def revoke(self, id: str, opts: Optional[CallOptions] = None) -> api_key_pb2.APIKey:
        req = api_key_pb2.RevokeAPIKeyRequest(id=id)
        return self._t.unary(
            _SERVICE, "Revoke", req, api_key_pb2.RevokeAPIKeyResponse(), opts
        ).api_key
