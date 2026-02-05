# TeslaMate Home Assistant Integration

A comprehensive Home Assistant Custom Component (HACS) integration for [TeslaMate](https://github.com/teslamate-org/teslamate) via MQTT.

![TeslaMate Logo](https://raw.githubusercontent.com/teslamate-org/teslamate/master/website/static/img/logo.svg)

## Features

- 🚗 **Full Vehicle Monitoring**: Battery, charging, climate, location, and more
- 📍 **GPS Device Tracker**: Track your Tesla's location on a map
- 🔋 **Battery & Charging Sensors**: Monitor battery level, range, charging state, power, and time to full charge
- 🌡️ **Climate Sensors**: Inside/outside temperature and climate status
- 🔒 **Security Binary Sensors**: Lock status, sentry mode, doors, windows, trunk, frunk
- 🚦 **Driving Sensors**: Speed, heading, shift state, power consumption
- 🛞 **Tire Pressure Monitoring**: All four tire pressures with visual gauges
- 📊 **Pre-configured Dashboard**: Beautiful dashboard with car picture and all important data
- 🔄 **Real-time Updates**: Instant updates via MQTT
- 🏠 **Geofence Support**: Shows location name when in defined geofence

## Prerequisites

1. **TeslaMate** must be installed and running
   - Follow the [TeslaMate installation guide](https://docs.teslamate.org/docs/installation/)
   
2. **MQTT Broker** must be configured in TeslaMate
   - Typically Mosquitto or another MQTT broker
   - TeslaMate must be publishing to MQTT topics
   
3. **Home Assistant MQTT Integration** must be configured
   - Configuration → Integrations → Add Integration → MQTT
   - Configure with your MQTT broker details

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/KingKongKent/teslamate-hacs`
6. Category: Integration
7. Click "Add"
8. Click "Install" on the TeslaMate integration
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/teslamate` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Add Integration

1. Go to **Configuration** → **Integrations**
2. Click **"+ Add Integration"**
3. Search for **"TeslaMate"**
4. Enter your configuration:
   - **Name**: Friendly name for your Tesla (e.g., "My Tesla")
   - **MQTT Prefix**: The MQTT topic prefix (default: `teslamate`)
   - **Car IDs**: Comma-separated list of car IDs (default: `1`)
5. Click **Submit**

### MQTT Topics

The integration automatically subscribes to all TeslaMate MQTT topics:
```
teslamate/cars/{car_id}/*
```

Default car_id is usually `1`. If you have multiple cars, enter them as comma-separated values (e.g., `1,2,3`).

## Dashboard Setup

### 1. Add Car Picture

The integration includes an icon, but you'll want to add a photo of your specific Tesla for the dashboard.

**Quick Steps:**
1. Get a photo of your Tesla (or download from tesla.com)
2. Save it to `config/www/tesla_images/my_tesla.jpg`
3. Update the dashboard picture entity to use `/local/tesla_images/my_tesla.jpg`

**Detailed instructions:** See [ADDING_CAR_IMAGE.md](ADDING_CAR_IMAGE.md) for:
- How to get Tesla Model Y Performance official images
- Image specifications and best practices
- Multiple car setup
- Troubleshooting

### 2. Import Dashboard

The integration includes a pre-configured dashboard. To use it:

**Option A: Manual Dashboard Creation**

1. Go to **Overview** in Home Assistant
2. Click the three dots in the top right
3. Select **"Edit Dashboard"**
4. Click **"+ Add View"**
5. Copy the dashboard configuration from `custom_components/teslamate/dashboard.py`
6. Use the YAML editor to paste the configuration

**Option B: Using Lovelace UI**

Create cards manually following the structure in the dashboard configuration.

## Available Entities

### Sensors

- Battery Level & Charge Limit
- Estimated/Rated/Ideal Range
- Odometer
- Inside/Outside Temperature
- Speed, Heading, Elevation
- Charging State & Power
- Charger Voltage, Current, Phases
- Time to Full Charge
- Software Version & Updates
- Tire Pressures (all 4)
- And many more...

### Binary Sensors

- Locked/Unlocked
- Sentry Mode
- Doors (individual & combined)
- Windows
- Trunk/Frunk
- Climate Status
- Plugged In
- User Present
- Update Available

### Device Tracker

- GPS Location with map integration
- Location name (geofence)
- Speed and heading attributes

## Customization

### Entity Naming

Entities are automatically named based on your car's display name from TeslaMate:
```
sensor.{display_name}_{sensor_name}
```

Example: `sensor.blue_thunder_battery_level`

### Custom Dashboard

You can customize the dashboard by:
1. Adding your own cards
2. Changing the layout
3. Adding custom themes
4. Creating automations based on the entities

## Troubleshooting

### No Entities Appearing

1. Verify MQTT integration is working:
   - Developer Tools → MQTT → Listen to `teslamate/#`
   - You should see messages coming in
   
2. Check your car_id:
   - Default is `1`, but yours might be different
   - Listen to `teslamate/cars/#` to see available car IDs

3. Verify TeslaMate is publishing to MQTT:
   - Check TeslaMate logs
   - Verify MQTT broker is running

### Entities Show "Unavailable"

- Check if TeslaMate is running and connected to your Tesla
- Verify MQTT broker is running
- Check Home Assistant logs for errors

### Car Picture Not Showing

- Ensure the image is at `config/www/tesla_car.png`
- Restart Home Assistant after adding the image
- Check file permissions

## Supported TeslaMate Versions

This integration works with TeslaMate v1.27.0 and later.

## Support

For issues, questions, or feature requests:
- [GitHub Issues](https://github.com/KingKongKent/teslamate-hacs/issues)
- [Home Assistant Community](https://community.home-assistant.io/)

### Sponsor This Project

If you find this integration useful, consider supporting its development:

[![Sponsor](https://img.shields.io/badge/Sponsor-PayPal-blue.svg)](https://www.paypal.com/paypalme/KingKongKent)

### Sponsor This Project

If you find this integration useful, consider supporting its development:

[![Sponsor](https://img.shields.io/badge/Sponsor-PayPal-blue.svg)](https://www.paypal.com/paypalme/KingKongKent)

## Credits

- [TeslaMate](https://github.com/teslamate-org/teslamate) - The awesome Tesla data logger
- Home Assistant Community

## License

MIT License - See LICENSE file for details

## Disclaimer

This project is not affiliated with Tesla Inc. or TeslaMate. Use at your own risk.
