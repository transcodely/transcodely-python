"""Transcodely root client (synchronous)."""

from __future__ import annotations

from collections.abc import Callable

import httpx
from typing_extensions import Self

from ._transport.transport import LogEvent, Transport
from .resources.api_keys import ApiKeys
from .resources.apps import Apps
from .resources.billing import Billing
from .resources.events import Events
from .resources.health import Health
from .resources.jobs import Jobs
from .resources.memberships import Memberships
from .resources.organizations import Organizations
from .resources.origins import Origins
from .resources.presets import Presets
from .resources.users import Users
from .resources.videos import Videos
from .resources.webhook_endpoints import WebhookEndpoints
from .version import API_VERSION, SDK_VERSION
from .webhooks import Webhooks


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
        organization_id: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        api_version: str | None = None,
        default_headers: dict[str, str] | None = None,
        http_client: httpx.Client | None = None,
        logger: Callable[[LogEvent], None] | None = None,
    ) -> None:
        self._transport = Transport(
            api_key,
            organization_id=organization_id,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            api_version=api_version,
            default_headers=default_headers,
            http_client=http_client,
            logger=logger,
        )
        self._jobs: Jobs | None = None
        self._videos: Videos | None = None
        self._presets: Presets | None = None
        self._origins: Origins | None = None
        self._apps: Apps | None = None
        self._api_keys: ApiKeys | None = None
        self._organizations: Organizations | None = None
        self._memberships: Memberships | None = None
        self._users: Users | None = None
        self._health: Health | None = None
        self._webhook_endpoints: WebhookEndpoints | None = None
        self._events: Events | None = None
        self._billing: Billing | None = None

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    @property
    def last_request_id(self) -> str | None:
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

    @property
    def webhook_endpoints(self) -> WebhookEndpoints:
        if self._webhook_endpoints is None:
            self._webhook_endpoints = WebhookEndpoints(self._transport)
        return self._webhook_endpoints

    @property
    def events(self) -> Events:
        if self._events is None:
            self._events = Events(self._transport)
        return self._events

    @property
    def billing(self) -> Billing:
        """The organization's invoices.

        Needs a dashboard session token for an organization owner plus
        ``organization_id`` on the client; API keys are rejected. See
        :class:`~transcodely.resources.billing.Billing`.
        """
        if self._billing is None:
            self._billing = Billing(self._transport)
        return self._billing

    @property
    def webhooks(self) -> type[Webhooks]:
        """Stripe-style facade: ``client.webhooks.construct_event(body, sig, secret)``."""
        return Webhooks
