"""Data coordinator for TeslaMate."""
from __future__ import annotations

import json
import logging
from datetime import timedelta
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class TeslaMateDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching TeslaMate data from MQTT."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        car_id: int,
        mqtt_prefix: str,
    ) -> None:
        """Initialize the coordinator."""
        self.car_id = car_id
        self.mqtt_prefix = mqtt_prefix
        self.base_topic = f"{mqtt_prefix}/cars/{car_id}"
        self._subscriptions = []
        
        _LOGGER.info(f"Initializing TeslaMate coordinator for car {car_id}, MQTT topic: {self.base_topic}")
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{car_id}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        
        # Initialize data dict
        self.data = {}
        
        # Subscribe to all topics
        self.hass.async_create_task(self._subscribe_to_topics())

    async def _subscribe_to_topics(self) -> None:
        """Subscribe to all TeslaMate MQTT topics."""
        topics = [
            "display_name", "state", "since", "healthy", "version",
            "update_available", "update_version", "model", "trim_badging",
            "exterior_color", "wheel_type", "spoiler_type", "geofence",
            "location", "latitude", "longitude", "shift_state", "power",
            "speed", "heading", "elevation", "locked", "sentry_mode",
            "windows_open", "doors_open", "trunk_open", "frunk_open",
            "is_user_present", "is_climate_on", "inside_temp", "outside_temp",
            "is_preconditioning", "odometer", "est_battery_range_km",
            "rated_battery_range_km", "ideal_battery_range_km", "battery_level",
            "usable_battery_level", "plugged_in", "charging_state",
            "charge_energy_added", "charge_limit_soc", "charge_port_door_open",
            "charger_actual_current", "charger_phases", "charger_power",
            "charger_voltage", "charge_current_request", "charge_current_request_max",
            "scheduled_charging_start_time", "time_to_full_charge",
            "tpms_pressure_fl", "tpms_pressure_fr", "tpms_pressure_rl",
            "tpms_pressure_rr", "active_route", "center_display_state",
            "driver_front_door_open", "driver_rear_door_open",
            "passenger_front_door_open", "passenger_rear_door_open",
        ]
        
        for topic in topics:
            full_topic = f"{self.base_topic}/{topic}"
            
            @callback
            def message_received(msg, topic_name=topic):
                """Handle new MQTT messages."""
                try:
                    payload = msg.payload
                    
                    # Try to parse JSON
                    if isinstance(payload, str) and (payload.startswith("{") or payload.startswith("[")):
                        try:
                            payload = json.loads(payload)
                        except json.JSONDecodeError:
                            pass
                    # Parse boolean values
                    elif isinstance(payload, str) and payload.lower() in ("true", "false"):
                        payload = payload.lower() == "true"
                    # Try to parse as number
                    elif isinstance(payload, str):
                        try:
                            if "." in payload:
                                payload = float(payload)
                            else:
                                payload = int(payload)
                        except ValueError:
                            pass  # Keep as string
                    
                    self.data[topic_name] = payload
                    self.async_set_updated_data(self.data)
                    _LOGGER.debug(f"Updated {topic_name} = {payload}")
                except Exception as err:
                    _LOGGER.error(f"Error processing message for {topic_name}: {err}")
            
            # Subscribe to MQTT topic
            unsubscribe = await mqtt.async_subscribe(self.hass, full_topic, message_received)
            self._subscriptions.append(unsubscribe)
        
        _LOGGER.info(f"Subscribed to {len(self._subscriptions)} MQTT topics for car {self.car_id}")

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from MQTT."""
        # Data is updated via MQTT subscriptions, so we just return current data
        return self.data

    async def async_shutdown(self) -> None:
        """Unsubscribe from MQTT topics."""
        for unsub in self._subscriptions:
            unsub()
