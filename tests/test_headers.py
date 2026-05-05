"""Tests for header builders + idempotency-key generation."""

from __future__ import annotations

import json
import re
import uuid

from transcodely._transport.headers import (
    client_user_agent_json,
    new_idempotency_key,
    user_agent,
)
from transcodely.version import SDK_VERSION


class TestUserAgent:
    def test_includes_sdk_version_and_python(self) -> None:
        ua = user_agent()
        assert f"Transcodely/{SDK_VERSION}" in ua
        assert "python" in ua


class TestClientUserAgentJson:
    def test_returns_parseable_json_object_with_expected_keys(self) -> None:
        parsed = json.loads(client_user_agent_json())
        assert parsed["lang"] == "python"
        assert parsed["publisher"] == "transcodely"
        assert parsed["version"] == SDK_VERSION
        assert isinstance(parsed["lang_version"], str)
        assert isinstance(parsed["platform"], str)


class TestIdempotencyKey:
    UUID_RE = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        re.IGNORECASE,
    )

    def test_matches_uuid_v4_format(self) -> None:
        for _ in range(50):
            key = new_idempotency_key()
            assert self.UUID_RE.match(key)
            # Round-trip through stdlib uuid as a stronger sanity check.
            assert uuid.UUID(key).version == 4

    def test_unique_across_calls(self) -> None:
        keys = {new_idempotency_key() for _ in range(200)}
        assert len(keys) == 200
