"""Wire-format tests for delivery regions on the hosting config and the
per-region egress breakdown on usage summaries."""

from __future__ import annotations

import json

from transcodely._codec.json_codec import deserialize, serialize
from transcodely.v1 import app_pb2, video_pb2


class TestDeliveryRegionsWireFormat:
    def test_update_hosting_config_serializes_delivery_regions_snake_case(self) -> None:
        req = app_pb2.UpdateHostingConfigRequest(
            id="app_abc",
            hosting_config=app_pb2.HostingConfig(delivery_regions=["europe"]),
        )
        obj = json.loads(serialize(req))
        assert obj["hosting_config"]["delivery_regions"] == ["europe"]
        assert "deliveryRegions" not in obj["hosting_config"]

    def test_usage_summary_parses_egress_by_region(self) -> None:
        body = json.dumps(
            {
                "usage": {
                    "egress_gb": 3,
                    "egress_by_region": [
                        {"region": "europe", "egress_bytes": "2147483648", "egress_gb": 2},
                        {"region": "", "egress_bytes": "1073741824", "egress_gb": 1},
                    ],
                    "daily": [
                        {
                            "date": "2026-11-01",
                            "egress_bytes": "3221225472",
                            "egress_by_region": [
                                {"region": "europe", "egress_bytes": "2147483648"},
                                {"egress_bytes": "1073741824"},
                            ],
                        }
                    ],
                }
            }
        ).encode()
        resp = deserialize(body, video_pb2.GetUsageResponse())
        by = resp.usage.egress_by_region
        assert [r.region for r in by] == ["europe", ""]
        assert by[0].egress_bytes == 2147483648
        assert by[0].egress_gb == 2
        assert resp.usage.daily[0].egress_by_region[0].region == "europe"
