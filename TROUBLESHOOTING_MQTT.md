# TeslaMate MQTT Troubleshooting Guide

If your integration shows "Unknown" for all sensors or displays the wrong model, follow these steps to diagnose and fix the issue.

## Quick Diagnostics

### 1. Check if TeslaMate is Publishing to MQTT

**Using MQTT Explorer (Recommended):**
1. Download MQTT Explorer: http://mqtt-explorer.com/
2. Connect to your MQTT broker
3. Look for the topic structure: `teslamate/cars/1/`
4. You should see topics like:
   - `teslamate/cars/1/model` (should show "Y" for Model Y)
   - `teslamate/cars/1/display_name` (your car's name)
   - `teslamate/cars/1/battery_level`
   - `teslamate/cars/1/state`

**Using mosquitto_sub command:**
```bash
mosquitto_sub -h YOUR_MQTT_HOST -t "teslamate/cars/#" -v
```

**Expected Output:**
```
teslamate/cars/1/model Y
teslamate/cars/1/display_name Model Y Performance
teslamate/cars/1/battery_level 85
teslamate/cars/1/trim_badging Performance
```

### 2. Check Home Assistant MQTT Integration

1. Go to **Settings** → **Devices & Services**
2. Find **MQTT** integration
3. Click **Configure**
4. Click **Listen to a topic**
5. Enter topic: `teslamate/cars/1/#`
6. Click **Start Listening**
7. You should see messages appearing

### 3. Check Integration Logs

1. Go to **Settings** → **System** → **Logs**
2. Search for "teslamate" or "TeslaMate"
3. Look for messages like:
   - `Initializing TeslaMate coordinator for car 1, MQTT topic: teslamate/cars/1`
   - `Subscribed to X MQTT topics for car 1`
   - `Updated model = Y` (or 3, S, X)
   - `Updated battery_level = 85`

**Enable Debug Logging:**
Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.teslamate: debug
    homeassistant.components.mqtt: debug
```

Then restart Home Assistant and check logs again.

## Common Issues

### Issue 1: All Sensors Show "Unknown"

**Symptom:** Integration loads but all entities show "Unknown" state

**Causes:**
- MQTT broker not connected
- TeslaMate not publishing to MQTT
- Wrong MQTT prefix or car ID
- MQTT integration not configured in Home Assistant

**Solutions:**

**A) Verify MQTT Broker Connection:**
```yaml
# configuration.yaml
mqtt:
  broker: YOUR_MQTT_IP
  port: 1883
  username: YOUR_USERNAME  # if required
  password: YOUR_PASSWORD  # if required
```

**B) Check TeslaMate MQTT Settings:**
In TeslaMate configuration (environment variables):
```bash
MQTT_HOST=YOUR_MQTT_IP
MQTT_PORT=1883
MQTT_NAMESPACE=teslamate  # This is your MQTT prefix
```

**C) Verify Car ID:**
- TeslaMate assigns car IDs sequentially (1, 2, 3...)
- First car added = ID 1
- Check MQTT topics to confirm: `teslamate/cars/1/` or `teslamate/cars/2/`
- If your car is ID 2, reconfigure the integration with car ID "2"

**D) Check MQTT Prefix:**
- Default is `teslamate`
- If you changed it in TeslaMate, update the integration configuration
- Common alternatives: `tesla`, `tm`, `car`

### Issue 2: Wrong Model Displayed (e.g., Model 3 instead of Model Y)

**Symptom:** Device shows "Model 3" but you have a Model Y Performance

**Cause:** The `model` topic hasn't published data yet, or was cached incorrectly

**Solutions:**

**A) Check MQTT Model Topic:**
```bash
mosquitto_sub -h YOUR_MQTT_HOST -t "teslamate/cars/1/model" -v
```

Should output: `teslamate/cars/1/model Y`

**B) Force TeslaMate to Republish:**
1. In TeslaMate web interface, go to your car
2. Click "Wake Up" to wake the car
3. Wait 30 seconds for data to sync
4. Check MQTT topic again

**C) Clear Retained Messages:**
Sometimes MQTT retains old data. Clear it:
```bash
mosquitto_pub -h YOUR_MQTT_HOST -t "teslamate/cars/1/model" -r -n
```

Then restart TeslaMate to republish fresh data.

**D) Delete and Re-add Integration:**
1. **Settings** → **Devices & Services**
2. Find **TeslaMate** integration
3. Click three dots → **Delete**
4. Restart Home Assistant
5. Add integration again

### Issue 3: Integration Won't Load

**Symptom:** Integration fails to add or shows error during setup

**Causes:**
- MQTT integration not installed
- Syntax error in files
- Missing dependencies

**Solutions:**

**A) Install MQTT Integration First:**
1. **Settings** → **Devices & Services**
2. **+ Add Integration**
3. Search: **MQTT**
4. Configure with your broker details
5. Then add TeslaMate integration

**B) Check Home Assistant Logs:**
Look for Python errors or stack traces that mention `custom_components.teslamate`

**C) Verify Installation:**
Files should be at:
```
config/
  custom_components/
    teslamate/
      __init__.py
      manifest.json
      config_flow.py
      coordinator.py
      sensor.py
      binary_sensor.py
      device_tracker.py
      const.py
      strings.json
      icon.png
      logo.png
```

### Issue 4: Some Sensors Work, Others Don't

**Symptom:** Battery level works but temperature sensors show "Unknown"

**Cause:** Tesla only publishes certain data based on car state

**Solutions:**

**A) Wake the Car:**
- TeslaMate only gets data when the car is awake
- Wake it via the Tesla app or TeslaMate interface
- Some sensors only update while driving or charging

**B) Wait for Data:**
- Temperature sensors: Update when climate is on
- Tire pressure: Updates while driving
- Charging sensors: Only available when plugged in
- Speed/power: Only available when driving

**C) Check MQTT Topics:**
Verify which topics are actually publishing:
```bash
mosquitto_sub -h YOUR_MQTT_HOST -t "teslamate/cars/1/#" -v | grep -v "^$"
```

### Issue 5: Model Y Shows as "Model Unknown"

**Symptom:** Device info shows "Model Unknown by Tesla"

**Cause:** Model data hasn't been received from MQTT yet

**Solutions:**

**A) Check Model Mapping:**
The integration maps MQTT model values:
- `Y` → Model Y
- `3` → Model 3
- `S` → Model S
- `X` → Model X

**B) Verify MQTT Model Value:**
```bash
mosquitto_sub -h YOUR_MQTT_HOST -t "teslamate/cars/1/model" -C 1
```

Should return: `Y` (single character)

**C) Check for Case Sensitivity:**
Model should be uppercase `Y`, not lowercase `y`

**D) Reload Integration:**
1. Go to **Settings** → **Devices & Services**
2. Find **TeslaMate** integration
3. Click **TeslaMate** device
4. Click three dots → **Reload**

## Testing Checklist

Use this checklist to verify everything is working:

- [ ] MQTT broker is running and accessible
- [ ] Home Assistant MQTT integration is configured
- [ ] TeslaMate is connected to MQTT broker
- [ ] Can see `teslamate/cars/1/#` topics in MQTT Explorer
- [ ] `teslamate/cars/1/model` shows correct model letter
- [ ] `teslamate/cars/1/display_name` shows car name
- [ ] `teslamate/cars/1/battery_level` shows current percentage
- [ ] TeslaMate integration loads without errors
- [ ] Device shows correct model name
- [ ] At least battery_level and state sensors work
- [ ] Wake car and verify more sensors populate

## Still Having Issues?

### Get Support

1. **Enable debug logging** (see above)
2. **Collect diagnostics:**
   - Screenshot of MQTT Explorer showing your topics
   - Home Assistant log entries for `custom_components.teslamate`
   - Your TeslaMate MQTT configuration (hide passwords!)
   - Screenshot of integration device info page

3. **Open an issue on GitHub:**
   - Include all diagnostic information
   - Specify your Home Assistant version
   - Specify your TeslaMate version
   - Include relevant log entries

### Useful Commands

**Test MQTT Connection:**
```bash
# Publish test message
mosquitto_pub -h YOUR_MQTT_HOST -t "test/topic" -m "hello"

# Subscribe to test
mosquitto_sub -h YOUR_MQTT_HOST -t "test/topic"
```

**Check TeslaMate Database:**
If TeslaMate web interface works but MQTT doesn't, check TeslaMate logs for MQTT connection errors.

**Restart Everything:**
Sometimes a full restart helps:
1. Restart Home Assistant
2. Restart MQTT broker
3. Restart TeslaMate
4. Wake Tesla via app

## Advanced: Manual MQTT Testing

Create a test automation to see if MQTT works:

```yaml
automation:
  - alias: "Test TeslaMate MQTT"
    trigger:
      - platform: mqtt
        topic: "teslamate/cars/1/battery_level"
    action:
      - service: persistent_notification.create
        data:
          title: "TeslaMate MQTT Test"
          message: "Received battery level: {{ trigger.payload }}"
```

If you get notifications, MQTT is working and the issue is with the integration code.
