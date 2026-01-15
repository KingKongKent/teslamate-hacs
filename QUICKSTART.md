# TeslaMate HACS Integration - Quick Start

Welcome! This is your complete Home Assistant integration for TeslaMate.

## 🚀 Quick Start (5 minutes)

### Prerequisites Checklist
- ✅ Home Assistant running
- ✅ TeslaMate installed and working
- ✅ MQTT broker (Mosquitto) running
- ✅ Home Assistant MQTT integration configured

### Installation Steps

1. **Install via HACS**
   - HACS → Integrations → Custom Repositories
   - Add this repo → Download → Restart HA

2. **Add Integration**
   - Settings → Integrations → Add Integration
   - Search "TeslaMate" → Configure → Submit

3. **Add Car Picture** (Optional)
   - Save image to: `config/www/tesla_car.png`
   - Use 16:9 aspect ratio (1920x1080 recommended)

4. **Import Dashboard**
   - Copy dashboard from `custom_components/teslamate/dashboard.py`
   - Settings → Dashboards → Add Dashboard → YAML mode

5. **Done!** 🎉
   - View your Tesla dashboard
   - All sensors are now available

## 📊 What You Get

### Sensors (40+)
- Battery level, charge limit, range
- Charging state, power, voltage, current
- Temperature (inside/outside)
- Speed, heading, location
- Tire pressures (all 4)
- Software version
- And much more!

### Binary Sensors (15+)
- Locked/unlocked
- Sentry mode
- Doors, windows, trunk, frunk
- Climate on/off
- Plugged in
- User present
- Update available

### Device Tracker
- GPS location on map
- Location name (geofence)
- Real-time updates

### Dashboard
- Beautiful car picture card
- Battery and charging info
- Climate controls
- Security status
- Map with location
- Tire pressure gauges
- Vehicle information

## 📝 Example Uses

### Quick Automations
```yaml
# Battery low alert
- Battery < 20% → Send notification

# Charging complete
- Charging state = Complete → Notify

# Unlocked away from home
- Locked = False + Location ≠ Home → Alert

# Start climate before departure
- Time = 7:50 AM → Start climate
```

See [AUTOMATIONS.md](AUTOMATIONS.md) for 12+ ready-to-use automation examples!

## 🔧 Configuration

### Default Setup
```
Name: TeslaMate
MQTT Prefix: teslamate
Car ID: 1
```

### Multiple Cars
```
Car IDs: 1,2,3
```

Each car gets its own device with all sensors.

## 📱 Entity Examples

After setup, you'll have entities like:
```
sensor.tesla_1_battery_level
sensor.tesla_1_estimated_range
sensor.tesla_1_charging_state
binary_sensor.tesla_1_locked
binary_sensor.tesla_1_plugged_in
device_tracker.tesla_1_location
```

Entity names use your car's display name from TeslaMate.

## 🎨 Dashboard Customization

The included dashboard shows:
- **Top**: Car picture with location
- **Row 1**: Status, Battery, Range
- **Card 1**: Battery & Charging details
- **Card 2**: Climate information
- **Card 3**: Security status
- **Card 4**: Location map
- **Card 5**: Location details
- **Card 6**: Vehicle information
- **Card 7**: Tire pressure gauges

Customize by editing in UI or YAML mode.

## 🚨 Troubleshooting

### No entities?
1. Check MQTT is working: Developer Tools → MQTT → Listen to `teslamate/#`
2. Verify car_id (usually `1`)
3. Check HA logs for errors

### Entities "Unavailable"?
1. Is TeslaMate running?
2. Is your Tesla online?
3. Is MQTT broker running?

### Car picture not showing?
1. Image at `config/www/tesla_car.png`?
2. Try PNG format
3. Restart HA

## 📚 Documentation

- **[README.md](README.md)** - Full documentation
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
- **[AUTOMATIONS.md](AUTOMATIONS.md)** - 12+ automation examples
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## 🌟 Features

- ✅ Real-time MQTT updates
- ✅ Multi-car support
- ✅ Proper device classes
- ✅ Statistics support
- ✅ Geofence integration
- ✅ Easy configuration
- ✅ HACS compatible
- ✅ Full HA entity registry
- ✅ Beautiful dashboard
- ✅ Comprehensive docs

## 🎯 Next Steps

1. ✅ Install integration
2. ✅ Add car picture
3. ✅ Import dashboard
4. 📋 Add automations (see AUTOMATIONS.md)
5. 🎨 Customize dashboard
6. 🔔 Set up notifications
7. 📊 Create energy tracking
8. 🚗 Enjoy!

## 💡 Pro Tips

### Energy Dashboard
Add charging sensors to HA Energy dashboard:
- Settings → Dashboards → Energy
- Add `sensor.tesla_1_charge_energy_added`

### Notifications
Install Home Assistant mobile app for push notifications in automations.

### Lovelace Cards
Try these custom cards (install via HACS):
- `mini-graph-card` - Beautiful graphs
- `battery-state-card` - Battery visualization
- `auto-entities` - Dynamic entity lists

### Templates
Create custom sensors in `configuration.yaml`:
```yaml
template:
  - sensor:
      - name: "Tesla Efficiency"
        unit_of_measurement: "Wh/km"
        state: "{{ states('sensor.tesla_1_power') | float / states('sensor.tesla_1_speed') | float }}"
```

## 🤝 Support

Need help?
- **GitHub Issues**: [Open an issue](https://github.com/your-username/teslamate-hacs/issues)
- **HA Community**: [Home Assistant Forum](https://community.home-assistant.io/)
- **TeslaMate Docs**: [TeslaMate Documentation](https://docs.teslamate.org/)

## ⭐ Enjoying This Integration?

- Star the repository on GitHub
- Share with other Tesla/HA users
- Contribute improvements
- Report bugs
- Suggest features

## 📜 License

MIT License - Free to use, modify, and distribute.

## ⚠️ Disclaimer

This integration is not affiliated with Tesla Inc. or TeslaMate.
Use at your own risk.

---

**Ready to get started? Follow the installation steps above!** 🚀

For detailed instructions, see [INSTALLATION.md](INSTALLATION.md)
