"""Config flow for TeslaMate integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
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


class TeslaMateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TeslaMate."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Check if MQTT integration is loaded
            if "mqtt" not in self.hass.config.components:
                errors["base"] = "mqtt_not_loaded"
            else:
                # Create entry
                await self.async_set_unique_id(
                    f"{user_input[CONF_MQTT_PREFIX]}_{user_input.get('car_ids', [1])}"
                )
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, "TeslaMate"),
                    data=user_input,
                )

        # Show form
        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default="TeslaMate"): cv.string,
                vol.Optional(CONF_MQTT_PREFIX, default=DEFAULT_MQTT_PREFIX): cv.string,
                vol.Optional("car_ids", default="1"): cv.string,  # Comma-separated car IDs
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
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
