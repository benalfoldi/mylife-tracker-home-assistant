"""HTTP client for the MyLife Tracker status API."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_STATUS_PATH

_LOGGER = logging.getLogger(__name__)


class MyLifeTrackerApiError(Exception):
    """Raised when the MyLife Tracker API returns an error."""


class MyLifeTrackerApi:
    """Thin wrapper around GET /api/ha/status."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    async def async_get_status(self, session: aiohttp.ClientSession) -> dict[str, Any]:
        """Fetch the full HA status payload."""
        url = f"{self._base_url}{API_STATUS_PATH}"
        headers = {"X-API-Key": self._api_key}
        try:
            async with session.get(url, headers=headers, timeout=15) as response:
                if response.status == 403:
                    raise MyLifeTrackerApiError("Invalid API key")
                if response.status >= 400:
                    body = await response.text()
                    raise MyLifeTrackerApiError(
                        f"HTTP {response.status}: {body[:200]}"
                    )
                return await response.json()
        except aiohttp.ClientError as err:
            raise MyLifeTrackerApiError(str(err)) from err

    async def async_push_webhook(self, session: aiohttp.ClientSession) -> None:
        """Ask MyLife to POST the current snapshot to HA_WEBHOOK_URL."""
        url = f"{self._base_url}/api/ha/push"
        headers = {"X-API-Key": self._api_key}
        async with session.post(url, headers=headers, timeout=15) as response:
            if response.status >= 400:
                body = await response.text()
                raise MyLifeTrackerApiError(
                    f"Push failed HTTP {response.status}: {body[:200]}"
                )


async def create_api(base_url: str, api_key: str) -> MyLifeTrackerApi:
    """Factory kept for tests and future extension."""
    return MyLifeTrackerApi(base_url, api_key)


def client_session(hass) -> aiohttp.ClientSession:
    """Return Home Assistant's shared aiohttp session."""
    return async_get_clientsession(hass)
