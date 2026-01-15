# TeslaMate Home Assistant Custom Component

This folder contains the core integration code for the TeslaMate Home Assistant Custom Component.

## Files Overview

### Core Integration Files

- **`__init__.py`** - Main integration entry point, platform setup, and lifecycle management
- **`manifest.json`** - Integration metadata, dependencies, and HACS configuration
- **`config_flow.py`** - Configuration UI flow for easy setup via Home Assistant UI
- **`const.py`** - Constants, MQTT topic definitions, and configuration defaults
- **`coordinator.py`** - MQTT data coordinator handling subscriptions and updates
- **`strings.json`** - UI text translations for configuration flow

### Entity Platforms

- **`sensor.py`** - 40+ sensor entities (battery, charging, climate, location, etc.)
- **`binary_sensor.py`** - 15+ binary sensor entities (locks, doors, windows, etc.)
- **`device_tracker.py`** - GPS device tracker for location with map integration

### Additional

- **`dashboard.py`** - Pre-configured dashboard YAML configuration

## Installation

### Via HACS (Recommended)

1. Add this repository as a custom repository in HACS
2. Search for "TeslaMate" in HACS integrations
3. Click Install
4. Restart Home Assistant

### Manual Installation

1. Copy this entire `teslamate` folder to `config/custom_components/teslamate/`
2. Restart Home Assistant
3. Add integration via UI: Settings → Integrations → Add Integration → TeslaMate

## Configuration

After installation:

1. Go to **Settings** → **Integrations**
2. Click **Add Integration**
3. Search for **TeslaMate**
4. Fill in:
   - Name: Your car's name
   - MQTT Prefix: `teslamate` (default)
   - Car IDs: `1` (or comma-separated for multiple cars)
5. Click **Submit**

## Requirements

- Home Assistant 2024.1+
- MQTT integration configured
- TeslaMate v1.27.0+ running and publishing to MQTT

## What It Creates

### Per Car

- **1 Device** (your Tesla)
- **40+ Sensors** (battery, charging, climate, location, etc.)
- **15+ Binary Sensors** (locks, doors, windows, etc.)
- **1 Device Tracker** (GPS location)

### Entity Examples

```yaml
sensor.tesla_1_battery_level
sensor.tesla_1_estimated_range
sensor.tesla_1_charging_state
binary_sensor.tesla_1_locked
binary_sensor.tesla_1_plugged_in
device_tracker.tesla_1_location
```

## Dashboard

A complete dashboard configuration is included in `dashboard.py`.

Import it to get:
- Car picture card
- Status overview
- Battery & charging details
- Climate controls
- Security status
- Interactive map
- Tire pressure gauges
- Vehicle information

## Documentation

Complete documentation is available in the repository root:

- **README.md** - Main documentation
- **QUICKSTART.md** - 5-minute quick start
- **INSTALLATION.md** - Detailed installation guide
- **AUTOMATIONS.md** - 12+ automation examples
- **TROUBLESHOOTING.md** - Problem solving guide
- **And more...**

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/teslamate-hacs/issues)
- **Community**: [Home Assistant Forum](https://community.home-assistant.io/)
- **Documentation**: See repository root for detailed guides

## Credits

- [TeslaMate](https://github.com/teslamate-org/teslamate) - Amazing Tesla data logger
- Home Assistant Community - Support and feedback

## License

MIT License - See LICENSE file in repository root
