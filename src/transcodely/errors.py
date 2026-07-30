"""Typed exception hierarchy for the Transcodely SDK.

Every exception raised by SDK methods inherits from :class:`TranscodelyError`,
so ``except TranscodelyError`` plus ``isinstance`` checks is enough for typed
error handling. Mirrors the TypeScript and Go SDK error classes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FieldViolation:
    """A field-level validation violation from an :class:`InvalidRequestError`."""

    field: str
    description: str


class TranscodelyError(Exception):
    """Base class for every Transcodely SDK exception."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        type: str | None = None,
        errors: list[FieldViolation] | None = None,
        http_status: int | None = None,
        request_id: str | None = None,
        raw: Any = None,
    ) -> None:
        super().__init__(message)
        self.code: str | None = code
        self.type: str | None = type
        self.errors: list[FieldViolation] = errors or []
        self.http_status: int | None = http_status
        self.request_id: str | None = request_id
        self.raw: Any = raw

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(message={super().__str__()!r}, code={self.code!r}, "
            f"http_status={self.http_status!r}, request_id={self.request_id!r})"
        )


class APIConnectionError(TranscodelyError):
    """Network failure: DNS, TLS, connection refused, no HTTP response."""


class APIError(TranscodelyError):
    """5xx server-side error."""


class AuthenticationError(TranscodelyError):
    """401 — invalid, missing, revoked, or expired API key."""


class PermissionError(TranscodelyError):
    """403 — authenticated but lacking permission."""


class NotFoundError(TranscodelyError):
    """404 — entity not found."""


class ConflictError(TranscodelyError):
    """409 — already exists, idempotency conflict, slug taken."""


class RateLimitError(TranscodelyError):
    """429 — rate-limited. ``retry_after_ms`` reflects the ``Retry-After`` header."""

    def __init__(
        self,
        message: str,
        *,
        retry_after_ms: int | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.retry_after_ms: int | None = retry_after_ms


class InvalidRequestError(TranscodelyError):
    """400 / 422 — request body or parameters were invalid."""


class PreconditionError(TranscodelyError):
    """412 — preconditions not met (e.g. job not cancelable in current state)."""


class WebhookError(TranscodelyError):
    """Base class for webhook signature-verification failures.

    Raised by :func:`transcodely.construct_event` /
    :func:`transcodely.verify_signature`. Catch this to handle any verification
    failure, or one of its subclasses to distinguish the cause.
    """


class WebhookSignatureError(WebhookError):
    """The signature header was malformed or no signature matched the body."""


class WebhookTimestampError(WebhookError):
    """The signature timestamp fell outside the allowed tolerance window."""


class WebhookPayloadError(WebhookError):
    """The body was not valid JSON or did not match the event-envelope shape."""
