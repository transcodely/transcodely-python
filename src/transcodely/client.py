"""Transcodely root client (synchronous)."""

from __future__ import annotations

from typing import Any, Callable, Optional

import httpx

from ._transport.transport import LogEvent, Transport
from .resources.api_keys import ApiKeys
from .resources.apps import Apps
from .resources.health import Health
from .resources.jobs import Jobs
from .resources.memberships import Memberships
from .resources.organizations import Organizations
from .resources.origins import Origins
from .resources.presets import Presets
from .resources.users import Users
from .resources.videos import Videos
from .version import API_VERSION, SDK_VERSION


class Transcodely:
    """Synchronous Transcodely API client.

    Use as a context manager (``with Transcodely(api_key=...) as client:``) to
    make sure the underlying HTTP client is closed cleanly.
    """

    API_VERSION: str = API_VERSION
    SDK_VERSION: str = SDK_VERSION

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        api_version: Optional[str] = None,
        default_headers: Optional[dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        logger: Optional[Callable[[LogEvent], None]] = None,
    ) -> None:
        self._transport = Transport(
            api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            api_version=api_version,
            default_headers=default_headers,
            http_client=http_client,
            logger=logger,
        )
        self._jobs: Optional[Jobs] = None
        self._videos: Optional[Videos] = None
        self._presets: Optional[Presets] = None
        self._origins: Optional[Origins] = None
        self._apps: Optional[Apps] = None
        self._api_keys: Optional[ApiKeys] = None
        self._organizations: Optional[Organizations] = None
        self._memberships: Optional[Memberships] = None
        self._users: Optional[Users] = None
        self._health: Optional[Health] = None

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> "Transcodely":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @property
    def last_request_id(self) -> Optional[str]:
        """Stripe-style: ID of the most recent successful or failed request."""
        return self._transport.last_request_id

    @property
    def jobs(self) -> Jobs:
        if self._jobs is None:
            self._jobs = Jobs(self._transport)
        return self._jobs

    @property
    def videos(self) -> Videos:
        if self._videos is None:
            self._videos = Videos(self._transport)
        return self._videos

    @property
    def presets(self) -> Presets:
        if self._presets is None:
            self._presets = Presets(self._transport)
        return self._presets

    @property
    def origins(self) -> Origins:
        if self._origins is None:
            self._origins = Origins(self._transport)
        return self._origins

    @property
    def apps(self) -> Apps:
        if self._apps is None:
            self._apps = Apps(self._transport)
        return self._apps

    @property
    def api_keys(self) -> ApiKeys:
        if self._api_keys is None:
            self._api_keys = ApiKeys(self._transport)
        return self._api_keys

    @property
    def organizations(self) -> Organizations:
        if self._organizations is None:
            self._organizations = Organizations(self._transport)
        return self._organizations

    @property
    def memberships(self) -> Memberships:
        if self._memberships is None:
            self._memberships = Memberships(self._transport)
        return self._memberships

    @property
    def users(self) -> Users:
        if self._users is None:
            self._users = Users(self._transport)
        return self._users

    @property
    def health(self) -> Health:
        if self._health is None:
            self._health = Health(self._transport)
        return self._health
