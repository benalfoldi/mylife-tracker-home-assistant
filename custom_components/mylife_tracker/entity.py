"""Shared entity helpers."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MyLifeTrackerCoordinator


class MyLifeTrackerEntity(CoordinatorEntity[MyLifeTrackerCoordinator]):
    """Base entity for MyLife Tracker."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: MyLifeTrackerCoordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name="MyLife Tracker",
            manufacturer="MyLife Tracker",
            model="Status API",
        )

    @property
    def _status(self) -> dict:
        return self.coordinator.data or {}
