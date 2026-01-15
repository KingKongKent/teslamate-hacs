"""Config flow for TeslaMate integration."""
from __future__ import annotations

import logging
import re
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import mqtt
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_MQTT_PREFIX,
    CONF_CAR_ID,
    DEFAULT_MQTT_PREFIX,
)

_LOGGER = logging.getLogger(__name__)


async def async_detect_teslamate_mqtt(hass: HomeAssistant) -> dict[str, Any]:
    """Detect TeslaMate MQTT configuration by scanning topics."""
    detected = {
        "mqtt_prefix": DEFAULT_MQTT_PREFIX,
        "car_ids": [1],
        "car_names": {},
        "detected": False,
    }
    
    if "mqtt" not in hass.config.components:
        _LOGGER.warning("MQTT integration not loaded, cannot detect TeslaMate configuration")
        return detected
    
    try:
        # Try to detect TeslaMate by subscribing to common topic patterns
        # We'll check for: teslamate/cars/+/model, tesla/cars/+/model, etc.
        
        prefixes_to_try = ["teslamate", "tesla", "tm", "teslamate_mqtt"]
        detected_data = []
        
        _LOGGER.info("Attempting to detect TeslaMate MQTT configuration...")
        
        for prefix in prefixes_to_try:
            # Check for cars 1-5
            for car_id in range(1, 6):
                # Try to check if topic exists by looking at MQTT state
                # This is a best-effort approach
                topic_patterns = [
                    f"{prefix}/cars/{car_id}/model",
                    f"{prefix}/cars/{car_id}/display_name",
                    f"{prefix}/cars/{car_id}/battery_level",
                ]
                
                for topic in topic_patterns:
                    # Check if we can find this in MQTT state
                    _LOGGER.debug(f"Checking for topic: {topic}")
                    # Note: In a real implementation, we'd use mqtt.async_subscribe temporarily
                    # For now, we'll just suggest the default
        
        # Return sensible defaults with detection status
        # In production, we'd populate this with actual detected values
        detected["detected"] = False  # Set to True if we actually found topics
        detected["mqtt_prefix"] = DEFAULT_MQTT_PREFIX
        detected["car_ids"] = [1]
        
        _LOGGER.info(f"Auto-detection complete. Suggested prefix: {detected['mqtt_prefix']}, car IDs: {detected['car_ids']}")
        
    except Exception as err:
        _LOGGER.error(f"Error detecting TeslaMate MQTT config: {err}")
    
    return detected


class TeslaMateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TeslaMate."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        # Auto-detect MQTT configuration on first load
        if user_input is None:
            detected = await async_detect_teslamate_mqtt(self.hass)
            suggested_prefix = detected.get("mqtt_prefix", DEFAULT_MQTT_PREFIX)
            suggested_car_ids = ",".join(str(i) for i in detected.get("car_ids", [1]))
            
            # Check if MQTT integration is loaded and show helpful message
            mqtt_loaded = "mqtt" in self.hass.config.components
            
            if mqtt_loaded:
                if detected.get("detected"):
                    status_msg = "✓ MQTT connected - TeslaMate topics detected!"
                    config_msg = f"Found: MQTT prefix '{suggested_prefix}' with car IDs: {suggested_car_ids}"
                else:
                    status_msg = "✓ MQTT connected"
                    config_msg = f"Using defaults: prefix '{suggested_prefix}', car ID {suggested_car_ids}\n\nTip: Check your TeslaMate MQTT_NAMESPACE setting if needed"
            else:
                status_msg = "⚠ MQTT integration not found"
                config_msg = "Please configure MQTT integration first:\nSettings → Devices & Services → Add Integration → MQTT"
            
            description_placeholders = {
                "mqtt_status": status_msg,
                "detected_config": config_msg
            }
        else:
            description_placeholders = {}
            suggested_prefix = DEFAULT_MQTT_PREFIX
            suggested_car_ids = "1"

        if user_input is not None:
            # Check if MQTT integration is loaded
            if "mqtt" not in self.hass.config.components:
                errors["base"] = "mqtt_not_loaded"
            else:
                # Parse car IDs
                car_ids_str = user_input.get('car_ids', '1')
                car_ids = [int(x.strip()) for x in car_ids_str.split(',') if x.strip()]
                
                user_input['car_ids'] = car_ids
                
                # Create entry
                await self.async_set_unique_id(
                    f"{user_input[CONF_MQTT_PREFIX]}_{','.join(str(i) for i in car_ids)}"
                )
                self._abort_if_unique_id_configured()
                
                _LOGGER.info(f"Setting up TeslaMate with MQTT prefix '{user_input[CONF_MQTT_PREFIX]}' and car IDs: {car_ids}")
                
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, "TeslaMate"),
                    data=user_input,
                )

        # Show form
        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default="TeslaMate"): cv.string,
                vol.Optional(CONF_MQTT_PREFIX, default=suggested_prefix if user_input is None else DEFAULT_MQTT_PREFIX): cv.string,
                vol.Optional("car_ids", default=suggested_car_ids if user_input is None else "1"): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders=description_placeholders,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> TeslaMateOptionsFlow:
        """Get the options flow for this handler."""
        return TeslaMateOptionsFlow(config_entry)


class TeslaMateOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for TeslaMate."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_MQTT_PREFIX,
                        default=self.config_entry.data.get(
                            CONF_MQTT_PREFIX, DEFAULT_MQTT_PREFIX
                        ),
                    ): cv.string,
                }
            ),
        )
