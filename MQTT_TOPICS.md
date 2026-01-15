# MQTT Topics Reference

Complete reference of all TeslaMate MQTT topics supported by this integration.

## Topic Structure

```
teslamate/cars/{car_id}/{topic}
```

Where `{car_id}` is typically `1` for the first car, `2` for second, etc.

## All Supported Topics

### Vehicle Information

| Topic | Type | Example | Description |
|-------|------|---------|-------------|
| `display_name` | string | "Blue Thunder" | Vehicle display name |
| `model` | string | "3" | Model (S, 3, X, Y) |
| `trim_badging` | string | "Long Range" | Trim badging |
| `exterior_color` | string | "Blue" | Exterior color |
| `wheel_type` | string | "19 inch Sport" | Wheel type |
| `spoiler_type` | string | "None" | Spoiler type |

### Status & Health

| Topic | Type | Example | Description |
|-------|------|---------|-------------|
| `state` | string | "online" | Vehicle state (online, asleep, charging) |
| `since` | datetime | "2026-01-15T10:30:00Z" | Last state change |
| `healthy` | boolean | true | TeslaMate health status |

### Software

| Topic | Type | Example | Description |
|-------|------|---------|-------------|
| `version` | string | "2024.38.4" | Current software version |
| `update_available` | boolean | true | Software update available |
| `update_version` | string | "2024.44.1" | Available update version |

### Battery & Range

| Topic | Type | Unit | Example | Description |
|-------|------|------|---------|-------------|
| `battery_level` | integer | % | 85 | Battery percentage |
| `usable_battery_level` | integer | % | 82 | Usable battery percentage |
| `charge_limit_soc` | integer | % | 90 | Charge limit |
| `est_battery_range_km` | float | km | 320.5 | Estimated range |
| `rated_battery_range_km` | float | km | 345.2 | Rated range |
| `ideal_battery_range_km` | float | km | 335.8 | Ideal range |

### Charging

| Topic | Type | Unit | Example | Description |
|-------|------|------|---------|-------------|
| `plugged_in` | boolean | - | true | Plugged into charger |
| `charging_state` | string | - | "Charging" | Charging state |
| `charge_energy_added` | float | kWh | 5.06 | Energy added this session |
| `charge_port_door_open` | boolean | - | true | Charge port open |
| `charger_actual_current` | float | A | 16.0 | Actual current |
| `charger_phases` | integer | - | 3 | Number of phases |
| `charger_power` | float | kW | 11.5 | Charger power |
| `charger_voltage` | integer | V | 240 | Charger voltage |
| `charge_current_request` | integer | A | 40 | Requested current |
| `charge_current_request_max` | integer | A | 40 | Max available current |
| `scheduled_charging_start_time` | datetime | - | "2026-01-16T02:00:00Z" | Scheduled start |
| `time_to_full_charge` | float | hours | 1.83 | Time to full charge |

### Location

| Topic | Type | Unit | Example | Description |
|-------|------|------|---------|-------------|
| `location` | json | - | `{"latitude": 35.278, "longitude": 29.745}` | GPS coordinates |
| `latitude` | float | ° | 35.278131 | Latitude (deprecated) |
| `longitude` | float | ° | 29.744801 | Longitude (deprecated) |
| `geofence` | string | - | "🏡 Home" | Geofence name |
| `heading` | integer | ° | 245 | Compass heading (0-360) |
| `elevation` | integer | m | 70 | Elevation above sea level |

### Driving

| Topic | Type | Unit | Example | Description |
|-------|------|------|---------|-------------|
| `speed` | integer | km/h | 85 | Current speed |
| `shift_state` | string | - | "D" | Shift state (P/R/N/D) |
| `power` | integer | W | -18000 | Power (+ discharge, - charge) |

### Climate

| Topic | Type | Unit | Example | Description |
|-------|------|------|---------|-------------|
| `is_climate_on` | boolean | - | true | Climate control on |
| `inside_temp` | float | °C | 21.5 | Inside temperature |
| `outside_temp` | float | °C | 18.4 | Outside temperature |
| `is_preconditioning` | boolean | - | false | Preconditioning active |

### Security & Status

| Topic | Type | Example | Description |
|-------|------|---------|-------------|
| `locked` | boolean | true | Vehicle locked |
| `sentry_mode` | boolean | true | Sentry mode active |
| `is_user_present` | boolean | false | User in vehicle |

### Doors & Windows

| Topic | Type | Example | Description |
|-------|------|---------|-------------|
| `windows_open` | boolean | false | Any window open |
| `doors_open` | boolean | false | Any door open |
| `driver_front_door_open` | boolean | false | Driver front door |
| `driver_rear_door_open` | boolean | false | Driver rear door |
| `passenger_front_door_open` | boolean | false | Passenger front door |
| `passenger_rear_door_open` | boolean | false | Passenger rear door |
| `trunk_open` | boolean | false | Trunk open |
| `frunk_open` | boolean | false | Frunk open |

### Tire Pressure

| Topic | Type | Unit | Example | Description |
|-------|------|------|---------|-------------|
| `tpms_pressure_fl` | float | BAR | 2.9 | Front left tire |
| `tpms_pressure_fr` | float | BAR | 2.8 | Front right tire |
| `tpms_pressure_rl` | float | BAR | 2.9 | Rear left tire |
| `tpms_pressure_rr` | float | BAR | 2.8 | Rear right tire |
| `tpms_soft_warning_fl` | boolean | false | FL soft warning |
| `tpms_soft_warning_fr` | boolean | false | FR soft warning |
| `tpms_soft_warning_rl` | boolean | false | RL soft warning |
| `tpms_soft_warning_rr` | boolean | false | RR soft warning |

### Navigation

| Topic | Type | Example | Description |
|-------|------|---------|-------------|
| `active_route` | json | See below | Active navigation route |
| `active_route_destination` | string | "Home" | Destination (deprecated) |
| `active_route_latitude` | float | 35.278131 | Dest latitude (deprecated) |
| `active_route_longitude` | float | 29.744801 | Dest longitude (deprecated) |

### Other

| Topic | Type | Unit | Example | Description |
|-------|------|------|---------|-------------|
| `odometer` | float | km | 45230.5 | Total odometer reading |
| `center_display_state` | integer | - | 0 | Center display state |

## JSON Payloads

### location
```json
{
  "latitude": 35.278131,
  "longitude": 29.744801
}
```

### active_route (with navigation)
```json
{
  "destination": "Home",
  "energy_at_arrival": 73,
  "miles_to_arrival": 6.485299,
  "minutes_to_arrival": 23.466667,
  "traffic_minutes_delay": 0.0,
  "location": {
    "latitude": 35.278131,
    "longitude": 29.744801
  },
  "error": null
}
```

### active_route (no navigation)
```json
{
  "error": "No active route available"
}
```

## State Values

### state
- `online` - Car is awake and connected
- `asleep` - Car is sleeping
- `charging` - Car is charging
- `driving` - Car is being driven
- `offline` - Car is offline

### charging_state
- `Charging` - Actively charging
- `Complete` - Charging complete
- `Stopped` - Charging stopped
- `Disconnected` - Not plugged in
- `NoPower` - Plugged but no power

### shift_state
- `P` - Park
- `R` - Reverse
- `N` - Neutral
- `D` - Drive

## MQTT Examples

### Subscribe to All Topics
```bash
mosquitto_sub -h localhost -t "teslamate/#" -v
```

### Subscribe to One Car
```bash
mosquitto_sub -h localhost -t "teslamate/cars/1/#" -v
```

### Subscribe to Battery Level
```bash
mosquitto_sub -h localhost -t "teslamate/cars/1/battery_level" -v
```

### Subscribe to All Cars Battery
```bash
mosquitto_sub -h localhost -t "teslamate/cars/+/battery_level" -v
```

### Test Publish (for testing)
```bash
mosquitto_pub -h localhost -t "teslamate/cars/1/battery_level" -m "85"
```

## Integration Mapping

### Sensor Entities
All numeric and string topics become sensors:
- `battery_level` → `sensor.tesla_1_battery_level`
- `charging_state` → `sensor.tesla_1_charging_state`
- `inside_temp` → `sensor.tesla_1_inside_temperature`

### Binary Sensor Entities
All boolean topics become binary sensors:
- `locked` → `binary_sensor.tesla_1_locked`
- `plugged_in` → `binary_sensor.tesla_1_plugged_in`
- `doors_open` → `binary_sensor.tesla_1_doors`

### Device Tracker
Location data becomes device tracker:
- `location` → `device_tracker.tesla_1_location`
- With attributes: `geofence`, `speed`, `heading`

## Update Frequency

### While Driving
- Location: Every 1-2 seconds
- Speed/heading: Every 1-2 seconds
- Power: Every 1-2 seconds

### While Charging
- Battery level: Every 5-10 seconds
- Charger data: Every 5-10 seconds
- Energy added: Every 5-10 seconds

### While Parked (Awake)
- Most sensors: Every 30-60 seconds
- Climate: Every 30-60 seconds
- Lock status: On change

### While Asleep
- No updates (car is sleeping)
- Resume when car wakes

## Data Retention

TeslaMate stores all historical data in PostgreSQL database.
Home Assistant stores sensor history based on recorder configuration.

Recommended recorder settings:
```yaml
recorder:
  purge_keep_days: 30
  include:
    domains:
      - sensor
      - binary_sensor
      - device_tracker
    entity_globs:
      - sensor.tesla_*
      - binary_sensor.tesla_*
      - device_tracker.tesla_*
```

## QoS Settings

Recommended MQTT QoS:
- **QoS 0**: Fire and forget (fastest, may lose messages)
- **QoS 1**: At least once delivery (recommended)
- **QoS 2**: Exactly once (slowest, guaranteed)

TeslaMate default: QoS 1

## Retained Messages

TeslaMate publishes with retain flag:
- Last known state available immediately
- New subscribers get current state
- Survives broker restart

## Wildcards

### Single Level (+)
```bash
# All battery levels
teslamate/cars/+/battery_level

# All topics for car 1
teslamate/cars/1/+
```

### Multi Level (#)
```bash
# Everything
teslamate/#

# All car data
teslamate/cars/#

# All for car 1
teslamate/cars/1/#
```

## Topic Naming Convention

TeslaMate uses snake_case for all topics:
- `battery_level` (not `batteryLevel` or `battery-level`)
- `inside_temp` (not `insideTemp` or `inside-temp`)
- `charge_port_door_open` (not `chargePortDoorOpen`)

## Custom Topics

To add custom topics:
1. Update `const.py` with new topic constant
2. Add to `SENSOR_TYPES` or `BINARY_SENSOR_TYPES`
3. Coordinator auto-subscribes to all topics

## Debugging MQTT

### View All Messages
```bash
mosquitto_sub -h localhost -t "#" -v
```

### Check TeslaMate Topics
```bash
mosquitto_sub -h localhost -t "teslamate/#" -v | grep "cars/1"
```

### Monitor Specific Sensor
```bash
watch -n 1 'mosquitto_sub -h localhost -t "teslamate/cars/1/battery_level" -C 1'
```

### Count Messages
```bash
mosquitto_sub -h localhost -t "teslamate/cars/1/#" | wc -l
```

---

For more information:
- [TeslaMate MQTT Documentation](https://docs.teslamate.org/docs/integrations/mqtt)
- [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
- [Home Assistant MQTT](https://www.home-assistant.io/integrations/mqtt/)
