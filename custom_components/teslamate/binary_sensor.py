"""Support for TeslaMate binary sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODEL_NAMES, MANUFACTURER, get_model_name
from .coordinator import TeslaMateDataCoordinator

_LOGGER = logging.getLogger(__name__)


BINARY_SENSOR_TYPES = {
    "locked": {
        "name": "Locked",
        "device_class": BinarySensorDeviceClass.LOCK,
        "icon_on": "mdi:lock",
        "icon_off": "mdi:lock-open",
        "invert": True,  # Locked = True means "secure" so invert for binary sensor
    },
    "sentry_mode": {
        "name": "Sentry Mode",
        "icon_on": "mdi:shield-check",
        "icon_off": "mdi:shield-off",
    },
    "windows_open": {
        "name": "Windows",
        "device_class": BinarySensorDeviceClass.WINDOW,
        "icon_on": "mdi:window-open",
        "icon_off": "mdi:window-closed",
    },
    "doors_open": {
        "name": "Doors",
        "device_class": BinarySensorDeviceClass.DOOR,
        "icon_on": "mdi:car-door",
        "icon_off": "mdi:car-door",
    },
    "driver_front_door_open": {
        "name": "Driver Front Door",
        "device_class": BinarySensorDeviceClass.DOOR,
        "icon_on": "mdi:car-door",
        "icon_off": "mdi:car-door",
    },
    "driver_rear_door_open": {
        "name": "Driver Rear Door",
        "device_class": BinarySensorDeviceClass.DOOR,
        "icon_on": "mdi:car-door",
        "icon_off": "mdi:car-door",
    },
    "passenger_front_door_open": {
        "name": "Passenger Front Door",
        "device_class": BinarySensorDeviceClass.DOOR,
        "icon_on": "mdi:car-door",
        "icon_off": "mdi:car-door",
    },
    "passenger_rear_door_open": {
        "name": "Passenger Rear Door",
        "device_class": BinarySensorDeviceClass.DOOR,
        "icon_on": "mdi:car-door",
        "icon_off": "mdi:car-door",
    },
    "trunk_open": {
        "name": "Trunk",
        "device_class": BinarySensorDeviceClass.OPENING,
        "icon_on": "mdi:car-back",
        "icon_off": "mdi:car-back",
    },
    "frunk_open": {
        "name": "Frunk",
        "device_class": BinarySensorDeviceClass.OPENING,
        "icon_on": "mdi:car-back",
        "icon_off": "mdi:car-back",
    },
    "is_user_present": {
        "name": "User Present",
        "device_class": BinarySensorDeviceClass.PRESENCE,
        "icon_on": "mdi:account-check",
        "icon_off": "mdi:account-off",
    },
    "is_climate_on": {
        "name": "Climate",
        "icon_on": "mdi:air-conditioner",
        "icon_off": "mdi:air-conditioner",
    },
    "is_preconditioning": {
        "name": "Preconditioning",
        "icon_on": "mdi:weather-sunny",
        "icon_off": "mdi:weather-sunny",
    },
    "plugged_in": {
        "name": "Plugged In",
        "device_class": BinarySensorDeviceClass.PLUG,
        "icon_on": "mdi:power-plug",
        "icon_off": "mdi:power-plug-off",
    },
    "charge_port_door_open": {
        "name": "Charge Port",
        "device_class": BinarySensorDeviceClass.OPENING,
        "icon_on": "mdi:ev-plug-tesla",
        "icon_off": "mdi:ev-plug-tesla",
    },
    "update_available": {
        "name": "Update Available",
        "device_class": BinarySensorDeviceClass.UPDATE,
        "icon_on": "mdi:update",
        "icon_off": "mdi:update",
    },
    "healthy": {
        "name": "TeslaMate Healthy",
        "device_class": BinarySensorDeviceClass.PROBLEM,
        "icon_on": "mdi:check-circle",
        "icon_off": "mdi:alert-circle",
        "invert": True,  # Healthy = True means "no problem"
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TeslaMate binary sensors based on a config entry."""
    coordinators = hass.data[DOMAIN][config_entry.entry_id]["coordinators"]
    
    entities = []
    for car_id, coordinator in coordinators.items():
        for sensor_type, sensor_config in BINARY_SENSOR_TYPES.items():
            entities.append(
                TeslaMateBinarySensor(
                    coordinator,
                    car_id,
                    sensor_type,
                    sensor_config,
                )
            )
    
    async_add_entities(entities)


class TeslaMateBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a TeslaMate binary sensor."""

    def __init__(
        self,
        coordinator: TeslaMateDataCoordinator,
        car_id: int,
        sensor_type: str,
        config: dict[str, Any],
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._car_id = car_id
        self._sensor_type = sensor_type
        self._config = config
        
        # Entity attributes
        self._attr_unique_id = f"teslamate_{car_id}_{sensor_type}"
        self._attr_device_class = config.get("device_class")
    
    @property
    def name(self) -> str:
        """Return the name of the binary sensor."""
        display_name = self.coordinator.data.get('display_name')
        if display_name:
            return f"{display_name} {self._config['name']}"
        return f"Tesla {self._car_id} {self._config['name']}"
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        model_raw = self.coordinator.data.get("model")
        model_name = get_model_name(model_raw)
        display_name = self.coordinator.data.get("display_name", f"Tesla {self._car_id}")
        
        return {
            "identifiers": {(DOMAIN, f"teslamate_{self._car_id}")},
            "name": display_name,
            "manufacturer": MANUFACTURER,
            "model": model_name,
            "sw_version": self.coordinator.data.get("version"),
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        value = self.coordinator.data.get(self._sensor_type)
        
        if value is None:
            return None
        
        # Convert to boolean
        if isinstance(value, bool):
            result = value
        elif isinstance(value, str):
            result = value.lower() in ("true", "1", "on", "yes")
        else:
            result = bool(value)
        
        # Invert if needed (for lock and healthy sensors)
        if self._config.get("invert"):
            result = not result
        
        return result

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend."""
        if self.is_on:
            return self._config.get("icon_on")
        return self._config.get("icon_off")
