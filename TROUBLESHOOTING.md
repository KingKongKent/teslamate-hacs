# Troubleshooting Guide

Complete troubleshooting guide for the TeslaMate Home Assistant Integration.

## Quick Diagnostics Checklist

Before troubleshooting specific issues, verify these basics:

- [ ] Home Assistant is running
- [ ] MQTT integration is configured
- [ ] TeslaMate is running
- [ ] MQTT broker (Mosquitto) is running
- [ ] TeslaMate is publishing to MQTT
- [ ] Integration is installed correctly

## Common Issues

### Issue 1: No Entities Created

**Symptoms:**
- Integration shows 0 entities
- No sensors appear in Home Assistant
- Device shows but no entities

**Diagnosis:**
1. Check if MQTT integration is loaded:
   - Settings → Integrations → Look for "MQTT"
   
2. Verify MQTT messages are coming in:
   - Developer Tools → MQTT
   - Listen to topic: `teslamate/#`
   - You should see messages

**Solutions:**

**A. MQTT Not Configured**
```
Settings → Integrations → Add Integration → MQTT
Enter your MQTT broker details
Restart Home Assistant
```

**B. TeslaMate Not Publishing**
```
Check TeslaMate logs:
docker logs teslamate

Check MQTT_HOST in TeslaMate config
Verify MQTT broker is running:
docker ps | grep mosquitto
```

**C. Wrong Car ID**
```
Listen to MQTT: teslamate/cars/#
Look for your car ID in topics (usually 1)
Update integration with correct ID:
  Settings → Integrations → TeslaMate → Configure
```

**D. MQTT Prefix Mismatch**
```
Default is "teslamate"
If TeslaMate uses different prefix:
  Settings → Integrations → TeslaMate → Configure
  Update MQTT Prefix field
```

---

### Issue 2: Entities Show "Unavailable"

**Symptoms:**
- Entities exist but show "Unavailable"
- Previously working entities stop updating
- Some entities work, others don't

**Diagnosis:**
1. Check entity state in Developer Tools:
   - Developer Tools → States
   - Search for `sensor.tesla_1_battery_level`
   - Check last_updated timestamp

2. Check MQTT messages:
   - Developer Tools → MQTT
   - Listen to specific topic: `teslamate/cars/1/battery_level`

**Solutions:**

**A. Tesla is Asleep**
```
This is normal behavior!
Tesla goes to sleep to save battery
Entities will update when car wakes up

To wake the car:
- Open Tesla app
- Start the car
- TeslaMate will resume logging
```

**B. TeslaMate Stopped**
```
Check if TeslaMate is running:
docker ps | grep teslamate

Restart TeslaMate:
docker restart teslamate

Check logs:
docker logs teslamate
```

**C. MQTT Broker Down**
```
Check MQTT broker:
docker ps | grep mosquitto

Restart broker:
docker restart mosquitto

Test connection:
mosquitto_sub -h localhost -t teslamate/#
```

**D. Network Issues**
```
Check if HA can reach MQTT broker:
Settings → System → Logs
Look for MQTT connection errors

Verify broker IP/hostname
Check firewall rules
```

---

### Issue 3: Car Picture Not Showing

**Symptoms:**
- Dashboard loads but no car image
- Broken image icon
- "Image cannot be loaded" error

**Solutions:**

**A. Image Location Wrong**
```
Correct location: config/www/tesla_car.png

Check path:
ls config/www/tesla_car.png

Create www folder if missing:
mkdir config/www
```

**B. Image Format Issue**
```
Use PNG format (recommended)
JPG also works

Convert if needed:
- Online converter
- Image editor
- Save as PNG
```

**C. Permissions Issue**
```
Check file permissions:
ls -la config/www/tesla_car.png

Fix permissions:
chmod 644 config/www/tesla_car.png
chown homeassistant:homeassistant config/www/tesla_car.png
```

**D. Need HA Restart**
```
After adding image:
Settings → System → Restart

Or:
docker restart homeassistant
```

**E. Wrong Path in Dashboard**
```
Dashboard should reference:
/local/tesla_car.png

NOT:
config/www/tesla_car.png
/config/www/tesla_car.png
```

---

### Issue 4: Dashboard Not Showing Data

**Symptoms:**
- Dashboard cards are empty
- "Entity not available" errors
- Cards show but no data

**Solutions:**

**A. Entity Names Don't Match**
```
Check your actual entity names:
Settings → Devices & Services → TeslaMate → Click device

Update dashboard with correct names:
Replace tesla_1 with your car's name
Example: tesla_1 → blue_thunder
```

**B. Entities Not Created Yet**
```
Wait for MQTT messages to arrive
First data may take a few minutes
Check if TeslaMate is logging:
  Open TeslaMate web UI
  Verify data is shown there
```

**C. Dashboard YAML Errors**
```
Check for YAML syntax errors:
Settings → Dashboards → Edit → Check config

Common errors:
- Missing indentation
- Wrong entity names
- Typos in configuration
```

---

### Issue 5: Multiple Cars Not Working

**Symptoms:**
- Only one car shows up
- Wrong car data
- Duplicate entities

**Solutions:**

**A. Car IDs Not Configured**
```
During setup, enter all car IDs:
Car IDs: 1,2,3

Or reconfigure:
Settings → Integrations → TeslaMate → Configure
Update Car IDs field
```

**B. TeslaMate Has Different Car IDs**
```
Find your car IDs:
Developer Tools → MQTT
Listen to: teslamate/cars/#
Look at topic numbers

Update configuration with correct IDs
```

---

### Issue 6: Integration Won't Install

**Symptoms:**
- Can't find TeslaMate in integrations
- Installation fails
- "Unknown error" during setup

**Solutions:**

**A. Not Installed Correctly**
```
Via HACS:
1. HACS → Integrations
2. Three dots → Custom repositories
3. Add repo URL
4. Download
5. Restart HA

Manual:
1. Copy custom_components/teslamate folder
2. To config/custom_components/teslamate
3. Restart HA
```

**B. Home Assistant Restart Needed**
```
After installation:
Settings → System → Restart

Wait for full restart (2-3 minutes)
Then add integration
```

**C. MQTT Integration Not Found**
```
Install MQTT first:
Settings → Integrations → Add Integration → MQTT
Configure with broker details
Then install TeslaMate integration
```

---

### Issue 7: Real-time Updates Not Working

**Symptoms:**
- Data is stale
- Updates delayed
- Manual refresh needed

**Solutions:**

**A. MQTT QoS Settings**
```
Check MQTT broker QoS settings
Recommended: QoS 1

In MQTT integration:
Settings → Integrations → MQTT → Configure
```

**B. Coordinator Update Interval**
```
Default: 30 seconds
This is a fallback, MQTT should be real-time

If needed, can be changed in const.py:
DEFAULT_SCAN_INTERVAL = 30
```

**C. Too Many Entities**
```
If HA is slow:
- Check system resources
- Upgrade hardware
- Disable unused integrations
```

---

### Issue 8: Wrong Units (km vs miles, °C vs °F)

**Symptoms:**
- Range in wrong units
- Temperature in wrong units
- Speed in wrong units

**Solutions:**

**A. Home Assistant Unit Settings**
```
Settings → System → General
Change unit system:
- Metric (km, °C)
- Imperial (miles, °F)

Restart Home Assistant
```

**B. TeslaMate Configuration**
```
TeslaMate publishes in:
- km for distance
- °C for temperature

HA converts based on system settings
```

---

### Issue 9: Charging Data Not Updating

**Symptoms:**
- Charge level not increasing
- Charger power shows 0
- Time to full not updating

**Solutions:**

**A. Car Must Be Charging**
```
Check charging state:
sensor.tesla_1_charging_state

Should show: "Charging"
Not: "Stopped", "Complete", "Disconnected"
```

**B. TeslaMate Logging Delay**
```
TeslaMate updates every 1-5 seconds while charging
Check TeslaMate web UI to verify data there
If shown in TeslaMate but not HA:
  Check MQTT connection
  Restart integration
```

---

### Issue 10: Location/GPS Not Working

**Symptoms:**
- Device tracker shows "Unknown"
- Map doesn't show car
- Location coordinates wrong

**Solutions:**

**A. Car Must Be Awake**
```
Location only updates when car is online
Wake car via Tesla app
Drive to trigger updates
```

**B. GPS Data in MQTT**
```
Check if location data present:
Developer Tools → MQTT
Listen to: teslamate/cars/1/location

Should see JSON with latitude/longitude
```

**C. Device Tracker Entity**
```
Verify device tracker exists:
Developer Tools → States
Search: device_tracker.tesla_1_location

Check latitude/longitude attributes
```

---

## Advanced Troubleshooting

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.teslamate: debug
    homeassistant.components.mqtt: debug
```

Restart HA and check logs:
```
Settings → System → Logs
Look for "teslamate" entries
```

### Check MQTT Subscriptions

```bash
# Install mosquitto-clients
sudo apt-get install mosquitto-clients

# Subscribe to all TeslaMate topics
mosquitto_sub -h localhost -t "teslamate/#" -v

# Subscribe to specific car
mosquitto_sub -h localhost -t "teslamate/cars/1/#" -v

# Check connection
mosquitto_sub -h localhost -t "\$SYS/#" -v
```

### Verify MQTT Broker

```bash
# Check if broker is running
docker ps | grep mosquitto
netstat -tulpn | grep 1883

# Check broker logs
docker logs mosquitto

# Test publish
mosquitto_pub -h localhost -t "test/topic" -m "test message"
```

### Inspect Integration

```bash
# Check if integration installed
ls -la config/custom_components/teslamate/

# Check for Python errors
grep -r "teslamate" config/home-assistant.log

# Validate manifest
cat config/custom_components/teslamate/manifest.json
```

### Database Check (TeslaMate)

```bash
# Connect to TeslaMate database
docker exec -it teslamate-db psql -U teslamate

# Check cars
SELECT * FROM cars;

# Check latest positions
SELECT * FROM positions ORDER BY date DESC LIMIT 10;

# Check MQTT messages
SELECT * FROM mqtt_messages ORDER BY date DESC LIMIT 10;
```

---

## Getting Help

If you've tried everything and still have issues:

### 1. Gather Information
- Home Assistant version
- TeslaMate version
- MQTT broker type and version
- Error messages from logs
- Screenshots of issue

### 2. Check Existing Issues
- GitHub Issues: Search for similar problems
- HA Community: Search forum posts

### 3. Create Detailed Issue Report

**Title**: Clear, specific description
```
Example: "Entities show unavailable after HA restart"
```

**Description**: Include:
```
- What you expected
- What actually happened
- Steps to reproduce
- Environment details
- Relevant log entries
- Configuration (remove sensitive data)
```

### 4. Provide Logs

```yaml
# Enable debug logging
logger:
  logs:
    custom_components.teslamate: debug

# Copy relevant log entries
Settings → System → Logs
Download full log
```

### 5. Resources
- **GitHub**: https://github.com/your-repo/teslamate-hacs
- **HA Community**: https://community.home-assistant.io/
- **TeslaMate Docs**: https://docs.teslamate.org/
- **Discord**: Home Assistant Discord server

---

## Prevention Tips

### Regular Maintenance
- Keep HA updated
- Keep TeslaMate updated
- Monitor MQTT broker
- Check logs occasionally
- Backup configuration regularly

### Best Practices
- Use stable release versions
- Don't modify core files
- Document custom changes
- Test updates in dev environment
- Keep documentation handy

### Monitoring
Set up automations to alert on:
- Integration unavailable
- MQTT connection lost
- TeslaMate unhealthy
- Disk space low

---

## Still Need Help?

**Quick Links:**
- [Installation Guide](INSTALLATION.md)
- [README](README.md)
- [Automations Examples](AUTOMATIONS.md)
- [Dashboard Preview](DASHBOARD_PREVIEW.md)

**Community:**
- Post in Home Assistant Community Forum
- Open GitHub Issue
- Ask in Discord

**Please include:**
✅ Versions (HA, TeslaMate, integration)
✅ Error messages
✅ Steps you've tried
✅ Relevant logs

---

Most issues can be resolved by:
1. ✅ Verifying MQTT is working
2. ✅ Confirming TeslaMate is logging
3. ✅ Checking entity names match
4. ✅ Restarting Home Assistant
5. ✅ Reading the logs
