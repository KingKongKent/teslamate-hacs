"""Support for TeslaMate sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfPower,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODEL_NAMES, MANUFACTURER
from .coordinator import TeslaMateDataCoordinator

_LOGGER = logging.getLogger(__name__)


SENSOR_TYPES = {
    "battery_level": {
        "name": "Battery Level",
        "icon": "mdi:battery",
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
    },
    "usable_battery_level": {
        "name": "Usable Battery Level",
        "icon": "mdi:battery",
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
    },
    "charge_limit_soc": {
        "name": "Charge Limit",
        "icon": "mdi:battery-charging-80",
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
    },
    "est_battery_range_km": {
        "name": "Estimated Range",
        "icon": "mdi:map-marker-distance",
        "device_class": SensorDeviceClass.DISTANCE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfLength.KILOMETERS,
    },
    "rated_battery_range_km": {
        "name": "Rated Range",
        "icon": "mdi:map-marker-distance",
        "device_class": SensorDeviceClass.DISTANCE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfLength.KILOMETERS,
    },
    "ideal_battery_range_km": {
        "name": "Ideal Range",
        "icon": "mdi:map-marker-distance",
        "device_class": SensorDeviceClass.DISTANCE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfLength.KILOMETERS,
    },
    "odometer": {
        "name": "Odometer",
        "icon": "mdi:counter",
        "device_class": SensorDeviceClass.DISTANCE,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfLength.KILOMETERS,
    },
    "inside_temp": {
        "name": "Inside Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
    },
    "outside_temp": {
        "name": "Outside Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
    },
    "speed": {
        "name": "Speed",
        "icon": "mdi:speedometer",
        "device_class": SensorDeviceClass.SPEED,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfSpeed.KILOMETERS_PER_HOUR,
    },
    "power": {
        "name": "Power",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
    },
    "charger_power": {
        "name": "Charger Power",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.KILO_WATT,
    },
    "charger_voltage": {
        "name": "Charger Voltage",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
    },
    "charger_actual_current": {
        "name": "Charger Current",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
    },
    "charge_energy_added": {
        "name": "Charge Energy Added",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
    },
    "charger_phases": {
        "name": "Charger Phases",
        "icon": "mdi:sine-wave",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "charge_current_request": {
        "name": "Charge Current Request",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
    },
    "charge_current_request_max": {
        "name": "Charge Current Request Max",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
    },
    "time_to_full_charge": {
        "name": "Time to Full Charge",
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTime.HOURS,
        "icon": "mdi:clock-outline",
    },
    "charging_state": {
        "name": "Charging State",
        "icon": "mdi:ev-station",
    },
    "state": {
        "name": "State",
        "icon": "mdi:car-connected",
    },
    "shift_state": {
        "name": "Shift State",
        "icon": "mdi:car-shift-pattern",
    },
    "heading": {
        "name": "Heading",
        "icon": "mdi:compass",
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": "°",
    },
    "elevation": {
        "name": "Elevation",
        "icon": "mdi:elevation-rise",
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfLength.METERS,
    },
    "geofence": {
        "name": "Geofence",
        "icon": "mdi:map-marker-radius",
    },
    "version": {
        "name": "Software Version",
        "icon": "mdi:update",
    },
    "update_version": {
        "name": "Available Update Version",
        "icon": "mdi:update",
    },
    "model": {
        "name": "Model",
        "icon": "mdi:car-info",
    },
    "trim_badging": {
        "name": "Trim Badging",
        "icon": "mdi:car-info",
    },
    "exterior_color": {
        "name": "Exterior Color",
        "icon": "mdi:palette",
    },
    "wheel_type": {
        "name": "Wheel Type",
        "icon": "mdi:tire",
    },
    "tpms_pressure_fl": {
        "name": "Tire Pressure Front Left",
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPressure.BAR,
        "icon": "mdi:car-tire-alert",
    },
    "tpms_pressure_fr": {
        "name": "Tire Pressure Front Right",
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPressure.BAR,
        "icon": "mdi:car-tire-alert",
    },
    "tpms_pressure_rl": {
        "name": "Tire Pressure Rear Left",
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPressure.BAR,
        "icon": "mdi:car-tire-alert",
    },
    "tpms_pressure_rr": {
        "name": "Tire Pressure Rear Right",
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPressure.BAR,
        "icon": "mdi:car-tire-alert",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TeslaMate sensors based on a config entry."""
    coordinators = hass.data[DOMAIN][config_entry.entry_id]["coordinators"]
    
    entities = []
    for car_id, coordinator in coordinators.items():
        for sensor_type, sensor_config in SENSOR_TYPES.items():
            entities.append(
                TeslaMateSensor(
                    coordinator,
                    car_id,
                    sensor_type,
                    sensor_config,
                )
            )
    
    async_add_entities(entities)


class TeslaMateSensor(CoordinatorEntity, SensorEntity):
    """Representation of a TeslaMate sensor."""

    def __init__(
        self,
        coordinator: TeslaMateDataCoordinator,
        car_id: int,
        sensor_type: str,
        config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._car_id = car_id
        self._sensor_type = sensor_type
        self._config = config
        
        # Entity attributes
        self._attr_unique_id = f"teslamate_{car_id}_{sensor_type}"
        self._attr_icon = config.get("icon")
        self._attr_device_class = config.get("device_class")
        self._attr_state_class = config.get("state_class")
        self._attr_native_unit_of_measurement = config.get("unit")
    
    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        display_name = self.coordinator.data.get('display_name')
        if display_name:
            return f"{display_name} {self._config['name']}"
        return f"Tesla {self._car_id} {self._config['name']}"
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        model = self.coordinator.data.get("model", "Unknown")
        model_name = MODEL_NAMES.get(model, f"Model {model}")
        display_name = self.coordinator.data.get("display_name", f"Tesla {self._car_id}")
        
        return {
            "identifiers": {(DOMAIN, f"teslamate_{self._car_id}")},
            "name": display_name,
            "manufacturer": MANUFACTURER,
            "model": model_name,
            "sw_version": self.coordinator.data.get("version"),
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_type)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        attrs = {}
        
        # Add location data for geofence sensor
        if self._sensor_type == "geofence":
            if location := self.coordinator.data.get("location"):
                if isinstance(location, dict):
                    attrs["latitude"] = location.get("latitude")
                    attrs["longitude"] = location.get("longitude")
        
        # Add active route data
        if self._sensor_type == "state":
            if active_route := self.coordinator.data.get("active_route"):
                if isinstance(active_route, dict):
                    attrs["active_route"] = active_route
        
        return attrs
