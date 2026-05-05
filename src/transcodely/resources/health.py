"""Health resource — liveness check for the API."""

from __future__ import annotations

from typing import Optional

from .._transport.transport import CallOptions, Transport
from ..v1 import health_pb2

_SERVICE = "transcodely.v1.HealthService"


class Health:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def check(self, opts: Optional[CallOptions] = None) -> health_pb2.HealthCheckResponse:
        req = health_pb2.HealthCheckRequest()
        return self._t.unary(_SERVICE, "Check", req, health_pb2.HealthCheckResponse(), opts)
