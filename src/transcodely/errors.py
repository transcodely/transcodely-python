"""Typed exception hierarchy for the Transcodely SDK.

Every exception raised by SDK methods inherits from :class:`TranscodelyError`,
so ``except TranscodelyError`` plus ``isinstance`` checks is enough for typed
error handling. Mirrors the TypeScript and Go SDK error classes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


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
        code: Optional[str] = None,
        type: Optional[str] = None,
        errors: Optional[list[FieldViolation]] = None,
        http_status: Optional[int] = None,
        request_id: Optional[str] = None,
        raw: Any = None,
    ) -> None:
        super().__init__(message)
        self.code: Optional[str] = code
        self.type: Optional[str] = type
        self.errors: list[FieldViolation] = errors or []
        self.http_status: Optional[int] = http_status
        self.request_id: Optional[str] = request_id
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
        retry_after_ms: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.retry_after_ms: Optional[int] = retry_after_ms


class InvalidRequestError(TranscodelyError):
    """400 / 422 — request body or parameters were invalid."""


class PreconditionError(TranscodelyError):
    """412 — preconditions not met (e.g. job not cancelable in current state)."""
