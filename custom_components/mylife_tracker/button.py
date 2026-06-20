"""Button platform for MyLife Tracker."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import MyLifeTrackerApiError, client_session
from .const import DOMAIN
from .coordinator import MyLifeTrackerCoordinator
from .entity import MyLifeTrackerEntity

_LOGGER = logging.getLogger(__name__)


class MyLifeTrackerRefreshButton(MyLifeTrackerEntity, ButtonEntity):
    """Immediately poll /api/ha/status."""

    def __init__(self, coordinator: MyLifeTrackerCoordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_translation_key = "refresh"
        self._attr_unique_id = f"{entry_id}_refresh"
        self._attr_icon = "mdi:refresh"

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()


class MyLifeTrackerPushButton(MyLifeTrackerEntity, ButtonEntity):
    """Ask MyLife to POST the snapshot to HA_WEBHOOK_URL, then refresh."""

    def __init__(
        self,
        coordinator: MyLifeTrackerCoordinator,
        entry_id: str,
        api,
    ) -> None:
        super().__init__(coordinator, entry_id)
        self._api = api
        self._attr_translation_key = "push_webhook"
        self._attr_unique_id = f"{entry_id}_push_webhook"
        self._attr_icon = "mdi:webhook"

    async def async_press(self) -> None:
        session = client_session(self.hass)
        try:
            await self._api.async_push_webhook(session)
        except MyLifeTrackerApiError as err:
            _LOGGER.warning("Webhook push failed: %s", err)
        await self.coordinator.async_request_refresh()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MyLife Tracker buttons."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    coordinator: MyLifeTrackerCoordinator = entry_data["coordinator"]
    api = entry_data["api"]
    async_add_entities(
        [
            MyLifeTrackerRefreshButton(coordinator, entry.entry_id),
            MyLifeTrackerPushButton(coordinator, entry.entry_id, api),
        ]
    )
