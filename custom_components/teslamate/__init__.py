"""The TeslaMate integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX
from .coordinator import TeslaMateDataCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TeslaMate from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    mqtt_prefix = entry.data.get(CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX)
    
    # Create coordinator for each car
    coordinators = {}
    car_ids = entry.data.get("car_ids", [1])  # Default to car_id 1
    
    for car_id in car_ids:
        coordinator = TeslaMateDataCoordinator(hass, entry, car_id, mqtt_prefix)
        await coordinator.async_config_entry_first_refresh()
        coordinators[car_id] = coordinator
    
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinators": coordinators,
        "mqtt_prefix": mqtt_prefix,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
