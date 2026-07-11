"""Shared conformance corpus for webhook verification.

``tests/webhooks/fixtures/vectors.json`` is the language-agnostic corpus copied
verbatim from the other Transcodely SDKs. Every SDK that implements
``construct_event`` must pass each vector. We derive the signature header at
runtime exactly as the corpus' ``$description`` specifies.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

import pytest

from transcodely import construct_event
from transcodely.errors import (
    WebhookPayloadError,
    WebhookSignatureError,
    WebhookTimestampError,
)

_VECTORS = json.loads(
    (Path(__file__).parent / "webhooks" / "fixtures" / "vectors.json").read_text()
)["vectors"]

_ERROR_FOR_RESULT = {
    "signature_error": WebhookSignatureError,
    "timestamp_error": WebhookTimestampError,
    "payload_error": WebhookPayloadError,
}


def _hmac_hex(secret: str, ts: int, body: str) -> str:
    return hmac.new(secret.encode(), f"{ts}.{body}".encode(), hashlib.sha256).hexdigest()


def _derive_header(v: dict[str, Any]) -> str:
    """Build the ``Transcodely-Signature`` header for a vector at runtime."""
    if "signature_header" in v:
        return str(v["signature_header"])
    # The secret the body was signed with: an explicit signing_secret override,
    # else the single `secret`, else the first of `secrets`.
    sign_secret = v.get("signing_secret") or v.get("secret") or v["secrets"][0]
    sign_body = v.get("signing_body", v["body"])
    return f"t={v['ts']},v1={_hmac_hex(sign_secret, v['ts'], sign_body)}"


@pytest.mark.parametrize("v", _VECTORS, ids=[v["name"] for v in _VECTORS])
def test_vector(v: dict[str, Any]) -> None:
    header = _derive_header(v)
    verify_secret = v["secrets"] if "secrets" in v else v["secret"]
    now = v["now"]

    def run() -> Any:
        return construct_event(
            v["body"], header, verify_secret, tolerance=v["tolerance"], now=lambda: now
        )

    expect = v["expect"]
    result = expect["result"]

    if result == "ok":
        event = run()
        assert event.type == expect["event_type"]
        assert event.id == expect["event_id"]
        assert event.data.id == expect["data_id"]
        if "idempotency_key" in expect:
            assert event.request.idempotency_key == expect["idempotency_key"]
    else:
        with pytest.raises(_ERROR_FOR_RESULT[result]):
            run()
