"""Data update coordinator for MyLife Tracker."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MyLifeTrackerApi, MyLifeTrackerApiError, client_session
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MyLifeTrackerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Poll /api/ha/status on a fixed interval."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: MyLifeTrackerApi,
        scan_interval: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        session = client_session(self.hass)
        try:
            return await self.api.async_get_status(session)
        except MyLifeTrackerApiError as err:
            raise UpdateFailed(str(err)) from err
