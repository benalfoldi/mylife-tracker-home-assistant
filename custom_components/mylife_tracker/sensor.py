"""Sensor platform for MyLife Tracker."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    ATTR_DOCS_BADGE_COUNT,
    ATTR_EXPIRED_DOCS,
    ATTR_LAST_UPDATED,
    ATTR_PAYMENTS_BADGE_COUNT,
    ATTR_UNPAID_BILLS,
    ATTR_UNPAID_EXTRA_COSTS,
    ATTR_WARNING_DOCS,
    DOMAIN,
)
from .coordinator import MyLifeTrackerCoordinator
from .entity import MyLifeTrackerEntity


class MyLifeTrackerCountSensor(MyLifeTrackerEntity, SensorEntity):
    """Numeric sensor mapped to a top-level count field."""

    def __init__(
        self,
        coordinator: MyLifeTrackerCoordinator,
        entry_id: str,
        field: str,
        translation_key: str,
    ) -> None:
        super().__init__(coordinator, entry_id)
        self._field = field
        self._attr_translation_key = translation_key
        self._attr_unique_id = f"{entry_id}_{field}"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        value = self._status.get(self._field)
        return int(value) if value is not None else 0


class MyLifeTrackerStatusSensor(MyLifeTrackerEntity, SensorEntity):
    """Master sensor exposing list attributes for automations and the Lovelace card."""

    def __init__(self, coordinator: MyLifeTrackerCoordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_translation_key = "status"
        self._attr_unique_id = f"{entry_id}_status"
        self._attr_icon = "mdi:home-account"

    @property
    def native_value(self) -> StateType:
        return self._status.get("badge_count", 0)

    @property
    def extra_state_attributes(self) -> dict:
        data = self._status
        return {
            ATTR_DOCS_BADGE_COUNT: data.get("docs_badge_count", 0),
            ATTR_PAYMENTS_BADGE_COUNT: data.get("payments_badge_count", 0),
            ATTR_EXPIRED_DOCS: data.get("expired_docs", []),
            ATTR_WARNING_DOCS: data.get("warning_docs", []),
            ATTR_UNPAID_BILLS: data.get("unpaid_bills", []),
            ATTR_UNPAID_EXTRA_COSTS: data.get("unpaid_extra_costs", []),
            ATTR_LAST_UPDATED: data.get("last_updated"),
            "expired_count": data.get("expired_count", 0),
            "warning_count": data.get("warning_count", 0),
            "total_count": data.get("total_count", 0),
            "unpaid_bills_count": data.get("unpaid_bills_count", 0),
            "unpaid_extra_costs_count": data.get("unpaid_extra_costs_count", 0),
            "has_unpaid_bills": data.get("has_unpaid_bills", False),
            "has_unpaid_extra_costs": data.get("has_unpaid_extra_costs", False),
        }


SENSOR_SPECS: list[tuple[str, str]] = [
    ("badge_count", "badge_count"),
    ("docs_badge_count", "docs_badge_count"),
    ("payments_badge_count", "payments_badge_count"),
    ("unpaid_bills_count", "unpaid_bills_count"),
    ("unpaid_extra_costs_count", "unpaid_extra_costs_count"),
    ("expired_count", "expired_count"),
    ("warning_count", "warning_count"),
    ("total_count", "total_count"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MyLife Tracker sensors."""
    coordinator: MyLifeTrackerCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    entities: list[SensorEntity] = [
        MyLifeTrackerStatusSensor(coordinator, entry.entry_id),
    ]
    entities.extend(
        MyLifeTrackerCountSensor(coordinator, entry.entry_id, field, key)
        for field, key in SENSOR_SPECS
    )
    async_add_entities(entities)
