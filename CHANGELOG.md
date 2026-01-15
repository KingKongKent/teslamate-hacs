# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-15

### Added
- Initial release of TeslaMate HACS integration
- Full MQTT integration with TeslaMate
- 40+ sensor entities including:
  - Battery level and charge limit
  - Range sensors (estimated, rated, ideal)
  - Charging sensors (state, power, voltage, current)
  - Climate sensors (inside/outside temperature)
  - Speed, heading, elevation
  - Software version and update status
  - Tire pressure monitoring (all 4 tires)
  - Odometer
- 15+ binary sensor entities including:
  - Lock status
  - Sentry mode
  - Doors (individual and combined)
  - Windows
  - Trunk and frunk
  - User presence
  - Climate status
  - Plugged in status
  - Update available
- Device tracker entity with GPS location
- Pre-configured dashboard with:
  - Car picture card
  - Battery and charging information
  - Climate controls
  - Security status
  - Location map
  - Tire pressure gauges
  - Vehicle information
- Config flow for easy setup
- Multi-car support
- Comprehensive documentation
- Example automations
- HACS compatibility

### Features
- Real-time updates via MQTT
- Automatic device registration
- Proper device classes for all sensors
- State classes for statistics
- Geofence support
- Active route information
- Full Home Assistant entity registry support

## [Unreleased]

### Planned
- [ ] Service calls for climate control (if TeslaMate adds MQTT control)
- [ ] Service calls for lock/unlock (if TeslaMate adds MQTT control)
- [ ] Service calls for charging start/stop (if TeslaMate adds MQTT control)
- [ ] Charge scheduling automation helper
- [ ] Energy dashboard integration
- [ ] Historical data graphs
- [ ] Trip statistics sensor
- [ ] Charging session cost calculator
- [ ] Custom card for Lovelace UI
- [ ] Blueprint automations
- [ ] Integration with Tesla API for commands

### Under Consideration
- [ ] Support for TeslaMate webhooks
- [ ] Integration with Home Assistant energy management
- [ ] Carbon intensity tracking
- [ ] Charging efficiency calculations
- [ ] Predictive range based on route
- [ ] Integration with calendar for trip planning
- [ ] Voice assistant integration improvements

## Version History

### Version 1.0.0 (2026-01-15)
- Initial stable release
- Full feature set as documented
- Tested with TeslaMate v1.27.0+
- Tested with Home Assistant 2024.1+

---

## How to Upgrade

### Via HACS
1. Open HACS
2. Go to Integrations
3. Find TeslaMate
4. Click Update
5. Restart Home Assistant

### Manual Update
1. Download the latest release
2. Replace the `custom_components/teslamate` folder
3. Restart Home Assistant

### Breaking Changes
None in v1.0.0 (initial release)

---

## Support
For issues, feature requests, or questions:
- GitHub Issues: https://github.com/your-username/teslamate-hacs/issues
- Home Assistant Community: https://community.home-assistant.io/

## Credits
- TeslaMate team for the amazing Tesla logger
- Home Assistant community for support and feedback
