"""Constants for the TeslaMate integration."""
from typing import Final

DOMAIN: Final = "teslamate"

# Configuration
CONF_MQTT_PREFIX: Final = "mqtt_prefix"
CONF_CAR_ID: Final = "car_id"

# Defaults
DEFAULT_MQTT_PREFIX: Final = "teslamate"
DEFAULT_SCAN_INTERVAL: Final = 30

# Device info
MANUFACTURER: Final = "Tesla"

# Model mapping
MODEL_NAMES = {
    "3": "Model 3",
    "S": "Model S",
    "X": "Model X",
    "Y": "Model Y",
}

# MQTT Topics (relative to base topic)
TOPIC_DISPLAY_NAME = "display_name"
TOPIC_STATE = "state"
TOPIC_SINCE = "since"
TOPIC_HEALTHY = "healthy"
TOPIC_VERSION = "version"
TOPIC_UPDATE_AVAILABLE = "update_available"
TOPIC_UPDATE_VERSION = "update_version"
TOPIC_MODEL = "model"
TOPIC_TRIM_BADGING = "trim_badging"
TOPIC_EXTERIOR_COLOR = "exterior_color"
TOPIC_WHEEL_TYPE = "wheel_type"
TOPIC_SPOILER_TYPE = "spoiler_type"
TOPIC_GEOFENCE = "geofence"
TOPIC_LOCATION = "location"
TOPIC_LATITUDE = "latitude"
TOPIC_LONGITUDE = "longitude"
TOPIC_SHIFT_STATE = "shift_state"
TOPIC_POWER = "power"
TOPIC_SPEED = "speed"
TOPIC_HEADING = "heading"
TOPIC_ELEVATION = "elevation"
TOPIC_LOCKED = "locked"
TOPIC_SENTRY_MODE = "sentry_mode"
TOPIC_WINDOWS_OPEN = "windows_open"
TOPIC_DOORS_OPEN = "doors_open"
TOPIC_TRUNK_OPEN = "trunk_open"
TOPIC_FRUNK_OPEN = "frunk_open"
TOPIC_IS_USER_PRESENT = "is_user_present"
TOPIC_IS_CLIMATE_ON = "is_climate_on"
TOPIC_INSIDE_TEMP = "inside_temp"
TOPIC_OUTSIDE_TEMP = "outside_temp"
TOPIC_IS_PRECONDITIONING = "is_preconditioning"
TOPIC_ODOMETER = "odometer"
TOPIC_EST_BATTERY_RANGE_KM = "est_battery_range_km"
TOPIC_RATED_BATTERY_RANGE_KM = "rated_battery_range_km"
TOPIC_IDEAL_BATTERY_RANGE_KM = "ideal_battery_range_km"
TOPIC_BATTERY_LEVEL = "battery_level"
TOPIC_USABLE_BATTERY_LEVEL = "usable_battery_level"
TOPIC_PLUGGED_IN = "plugged_in"
TOPIC_CHARGING_STATE = "charging_state"
TOPIC_CHARGE_ENERGY_ADDED = "charge_energy_added"
TOPIC_CHARGE_LIMIT_SOC = "charge_limit_soc"
TOPIC_CHARGE_PORT_DOOR_OPEN = "charge_port_door_open"
TOPIC_CHARGER_ACTUAL_CURRENT = "charger_actual_current"
TOPIC_CHARGER_PHASES = "charger_phases"
TOPIC_CHARGER_POWER = "charger_power"
TOPIC_CHARGER_VOLTAGE = "charger_voltage"
TOPIC_CHARGE_CURRENT_REQUEST = "charge_current_request"
TOPIC_CHARGE_CURRENT_REQUEST_MAX = "charge_current_request_max"
TOPIC_SCHEDULED_CHARGING_START_TIME = "scheduled_charging_start_time"
TOPIC_TIME_TO_FULL_CHARGE = "time_to_full_charge"
TOPIC_TPMS_PRESSURE_FL = "tpms_pressure_fl"
TOPIC_TPMS_PRESSURE_FR = "tpms_pressure_fr"
TOPIC_TPMS_PRESSURE_RL = "tpms_pressure_rl"
TOPIC_TPMS_PRESSURE_RR = "tpms_pressure_rr"
TOPIC_ACTIVE_ROUTE = "active_route"
TOPIC_CENTER_DISPLAY_STATE = "center_display_state"
