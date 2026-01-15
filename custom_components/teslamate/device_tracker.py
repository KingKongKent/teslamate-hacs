"""Support for TeslaMate device tracker."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODEL_NAMES, MANUFACTURER, get_model_name
from .coordinator import TeslaMateDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TeslaMate device tracker based on a config entry."""
    coordinators = hass.data[DOMAIN][config_entry.entry_id]["coordinators"]
    
    entities = []
    for car_id, coordinator in coordinators.items():
        entities.append(TeslaMateDeviceTracker(coordinator, car_id))
    
    async_add_entities(entities)


class TeslaMateDeviceTracker(CoordinatorEntity, TrackerEntity):
    """Representation of a TeslaMate device tracker."""

    def __init__(
        self,
        coordinator: TeslaMateDataCoordinator,
        car_id: int,
    ) -> None:
        """Initialize the device tracker."""
        super().__init__(coordinator)
        self._car_id = car_id
        
        # Entity attributes
        self._attr_unique_id = f"teslamate_{car_id}_location"
        self._attr_has_entity_name = True
        self._attr_name = "Location"
        self._attr_suggested_object_id = f"tesla_{car_id}_location"
        self._attr_icon = "mdi:car"
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        model_raw = self.coordinator.data.get("model")
        model_name = get_model_name(model_raw)
        
        # Use display_name if available, otherwise use a friendly default
        display_name = self.coordinator.data.get("display_name")
        if not display_name:
            # Generate friendly name from model or use generic
            if model_raw in ("Y", "3", "S", "X"):
                display_name = f"Tesla {model_name}"
            else:
                display_name = f"Tesla Car {self._car_id}"
        
        return {
            "identifiers": {(DOMAIN, f"teslamate_{self._car_id}")},
            "name": display_name,
            "manufacturer": MANUFACTURER,
            "model": model_name,
            "sw_version": self.coordinator.data.get("version"),
        }

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        location = self.coordinator.data.get("location")
        if isinstance(location, dict):
            return location.get("latitude")
        return self.coordinator.data.get("latitude")

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        location = self.coordinator.data.get("location")
        if isinstance(location, dict):
            return location.get("longitude")
        return self.coordinator.data.get("longitude")

    @property
    def source_type(self) -> SourceType:
        """Return the source type."""
        return SourceType.GPS

    @property
    def location_name(self) -> str | None:
        """Return the location name."""
        return self.coordinator.data.get("geofence")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return device state attributes."""
        attrs = {}
        
        if heading := self.coordinator.data.get("heading"):
            attrs["heading"] = heading
        
        if speed := self.coordinator.data.get("speed"):
            attrs["speed"] = speed
        
        if elevation := self.coordinator.data.get("elevation"):
            attrs["elevation"] = elevation
        
        if shift_state := self.coordinator.data.get("shift_state"):
            attrs["shift_state"] = shift_state
        
        if power := self.coordinator.data.get("power"):
            attrs["power"] = power
        
        return attrs
