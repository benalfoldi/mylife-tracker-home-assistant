"""Config flow for MyLife Tracker."""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlparse

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MyLifeTrackerApi, MyLifeTrackerApiError
from .const import (
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MIN_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=3600)
        ),
    }
)


def _normalize_url(url: str) -> str:
    value = url.strip().rstrip("/")
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("invalid_url")
    return value


async def _validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, str]:
    """Verify URL + API key against /api/ha/status."""
    url = _normalize_url(data[CONF_URL])
    api = MyLifeTrackerApi(url, data[CONF_API_KEY])
    session = async_get_clientsession(hass)
    await api.async_get_status(session)
    return {CONF_URL: url}


class MyLifeTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MyLife Tracker."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                normalized = await _validate_input(self.hass, user_input)
            except ValueError:
                errors[CONF_URL] = "invalid_url"
            except MyLifeTrackerApiError as err:
                if "Invalid API key" in str(err):
                    errors[CONF_API_KEY] = "invalid_api_key"
                else:
                    errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(normalized[CONF_URL])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="MyLife Tracker",
                    data={
                        CONF_URL: normalized[CONF_URL],
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_SCAN_INTERVAL: user_input.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_SCHEMA,
            errors=errors,
        )
