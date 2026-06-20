"""Binary sensor platform for MyLife Tracker."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import MyLifeTrackerCoordinator
from .entity import MyLifeTrackerEntity


class MyLifeTrackerBinarySensor(MyLifeTrackerEntity, BinarySensorEntity):
    """Boolean flag from the status payload."""

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

    @property
    def is_on(self) -> bool:
        return bool(self._status.get(self._field))


BINARY_SPECS: list[tuple[str, str]] = [
    ("has_unpaid_bills", "has_unpaid_bills"),
    ("has_unpaid_extra_costs", "has_unpaid_extra_costs"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MyLife Tracker binary sensors."""
    coordinator: MyLifeTrackerCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    entities: list[BinarySensorEntity] = [
        MyLifeTrackerBinarySensor(coordinator, entry.entry_id, field, key)
        for field, key in BINARY_SPECS
    ]

    # Derived flags not sent as separate booleans by the API.
    entities.append(
        _DerivedBinarySensor(
            coordinator,
            entry.entry_id,
            "has_expired_docs",
            "has_expired_docs",
            lambda s: int(s.get("expired_count", 0)) > 0,
        )
    )
    entities.append(
        _DerivedBinarySensor(
            coordinator,
            entry.entry_id,
            "has_warning_docs",
            "has_warning_docs",
            lambda s: int(s.get("warning_count", 0)) > 0,
        )
    )

    async_add_entities(entities)


class _DerivedBinarySensor(MyLifeTrackerBinarySensor):
    """Binary sensor computed from counts."""

    def __init__(
        self,
        coordinator: MyLifeTrackerCoordinator,
        entry_id: str,
        field: str,
        translation_key: str,
        predicate,
    ) -> None:
        super().__init__(coordinator, entry_id, field, translation_key)
        self._predicate = predicate

    @property
    def is_on(self) -> bool:
        return self._predicate(self._status)
