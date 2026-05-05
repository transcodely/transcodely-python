"""Tests for HTTP-status → typed exception mapping."""

from __future__ import annotations

import pytest

from transcodely.errors import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    ConflictError,
    InvalidRequestError,
    NotFoundError,
    PermissionError,
    PreconditionError,
    RateLimitError,
)
from transcodely._transport.error_mapping import (
    connection_error,
    map_http_error,
)


def _err(status: int, body=None, headers=None):  # type: ignore[no-untyped-def]
    return map_http_error(status=status, body=body or {}, headers=headers or {})


@pytest.mark.parametrize(
    "status,exc",
    [
        (401, AuthenticationError),
        (403, PermissionError),
        (404, NotFoundError),
        (409, ConflictError),
        (412, PreconditionError),
        (422, InvalidRequestError),
        (400, InvalidRequestError),  # generic 4xx
        (500, APIError),
        (502, APIError),
        (503, APIError),
    ],
)
def test_status_maps_to_typed_exception(status: int, exc: type[Exception]) -> None:
    err = _err(status)
    assert isinstance(err, exc)
    assert err.http_status == status


class TestRateLimitError:
    def test_429_maps_to_rate_limit_error(self) -> None:
        err = _err(429, headers={"retry-after": "5"})
        assert isinstance(err, RateLimitError)
        assert err.retry_after_ms == 5_000

    def test_no_retry_after_header(self) -> None:
        err = _err(429)
        assert isinstance(err, RateLimitError)
        assert err.retry_after_ms is None

    def test_negative_retry_after_clamped_to_zero(self) -> None:
        err = _err(429, headers={"retry-after": "-3"})
        assert isinstance(err, RateLimitError)
        assert err.retry_after_ms == 0

    def test_unparseable_retry_after_is_none(self) -> None:
        err = _err(429, headers={"retry-after": "not-a-number"})
        assert isinstance(err, RateLimitError)
        assert err.retry_after_ms is None


class TestPayloadExtraction:
    def test_propagates_server_code_message_type_and_field_violations(self) -> None:
        body = {
            "code": "invalid_argument",
            "message": "validation failed",
            "details": [
                {
                    "type": "transcodely.v1.ErrorDetails",
                    "debug": {
                        "code": "JOB_INPUT_URL_INVALID",
                        "field_violations": [
                            {"field": "input_url", "description": "must be a valid URL"}
                        ],
                    },
                }
            ],
        }
        err = _err(422, body=body)
        assert str(err) == "validation failed"
        assert err.code == "JOB_INPUT_URL_INVALID"
        assert err.type == "invalid_argument"
        assert len(err.errors) == 1
        assert err.errors[0].field == "input_url"
        assert err.errors[0].description == "must be a valid URL"

    def test_accepts_camel_case_field_violations_as_fallback(self) -> None:
        body = {
            "message": "v",
            "details": [
                {
                    "debug": {
                        "fieldViolations": [{"field": "x", "description": "y"}],
                    }
                }
            ],
        }
        err = _err(422, body=body)
        assert err.errors[0].field == "x"

    def test_captures_request_id_from_headers(self) -> None:
        err = _err(500, headers={"x-request-id": "req_abc123"})
        assert err.request_id == "req_abc123"

    def test_parses_string_body_as_json(self) -> None:
        import json

        body = json.dumps({"message": "boom"})
        assert str(_err(500, body=body)) == "boom"

    def test_falls_back_to_message_text_when_string_body_is_not_json(self) -> None:
        assert str(_err(500, body="not json")) == "not json"

    def test_decodes_bytes_body(self) -> None:
        import json

        body = json.dumps({"message": "bytes worked"}).encode("utf-8")
        assert str(_err(500, body=body)) == "bytes worked"


class TestConnectionError:
    def test_wraps_an_exception_cause_and_surfaces_message(self) -> None:
        cause = OSError("ECONNREFUSED")
        err = connection_error(cause)
        assert isinstance(err, APIConnectionError)
        assert str(err) == "ECONNREFUSED"
        assert err.__cause__ is cause

    def test_uses_override_message_when_provided(self) -> None:
        err = connection_error(OSError("x"), "transient network glitch")
        assert str(err) == "transient network glitch"
