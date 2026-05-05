"""Version constants exposed at the top of the package."""

#: SDK package version. Bumped by release-please from pyproject.toml.
SDK_VERSION = "0.1.0"

#: Calendar-versioned API this release pins. Sent on every request as
#: `Transcodely-Version`. Override per-client via ``api_version=``.
API_VERSION = "2026-05-03"

#: Default base URL for the production Transcodely API.
DEFAULT_BASE_URL = "https://api.transcodely.com"
