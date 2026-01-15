# Diagnostic: Model Detection Issue

If your Tesla is showing as "Model Unknown" or the wrong model, follow these steps to diagnose.

## Step 1: Check MQTT Topic Value

Use one of these methods to see what TeslaMate is publishing:

### Method A: MQTT Explorer
1. Open MQTT Explorer
2. Navigate to: `teslamate/cars/1/model`
3. Check the value - should be a single letter: `Y`, `3`, `S`, or `X`

### Method B: Home Assistant MQTT Tool
1. Go to **Settings** → **Devices & Services** → **MQTT** → **Configure**
2. Click **Listen to a topic**
3. Enter: `teslamate/cars/1/model`
4. Click **Start Listening**
5. Check the value displayed

### Method C: Command Line
```bash
mosquitto_sub -h YOUR_MQTT_IP -t "teslamate/cars/1/model" -C 1
```

## Step 2: Check Home Assistant Logs

1. Go to **Settings** → **System** → **Logs**
2. Search for: `teslamate`
3. Look for lines like:
   ```
   Car 1 - model = Y
   Car 1 - display_name = Black Magic
   ```

If you see the log entry, the data is arriving. If the model shows correctly in logs but not in the UI, there may be a caching issue.

## Step 3: Expected Values

TeslaMate publishes these model values:
- **Model 3** → `3`
- **Model S** → `S`
- **Model X** → `X`
- **Model Y** → `Y`

The integration will map these to:
- `3` → "Model 3"
- `S` → "Model S"
- `X` → "Model X"
- `Y` → "Model Y"

## Common Issues

### Issue 1: Model Topic Not Publishing

**Symptom:** No data in `teslamate/cars/1/model` topic

**Causes:**
- TeslaMate hasn't fetched car data yet
- Car is asleep
- TeslaMate MQTT connection issue

**Solutions:**
1. Wake your car via Tesla app
2. Wait 30-60 seconds for TeslaMate to poll data
3. Check TeslaMate logs for MQTT connection errors
4. Restart TeslaMate service

### Issue 2: Wrong Model Showing

**Symptom:** Shows "Model 3" but you have Model Y

**Causes:**
- Old/cached data from previous setup
- Multiple car IDs configured
- Entity registry has stale data

**Solutions:**

**A) Clear Entity Registry:**
1. Stop Home Assistant
2. Edit `.storage/core.entity_registry` (backup first!)
3. Remove all `teslamate` entries
4. Start Home Assistant
5. Re-add integration

**B) Delete and Re-add Integration:**
1. **Settings** → **Devices & Services**
2. Find **TeslaMate** → Three dots → **Delete**
3. **Restart Home Assistant** (important!)
4. Add integration again
5. Check logs for `Car 1 - model = Y`

**C) Force Device Update:**
1. Go to device page
2. Click device name (e.g., "Black Magic")
3. Three dots → **Delete**
4. Wait 30 seconds
5. Restart Home Assistant
6. Device should be recreated with correct model

### Issue 3: Model Shows "Unknown"

**Symptom:** Device shows "Model Unknown by Tesla"

**Causes:**
- Model data hasn't arrived from MQTT yet
- MQTT subscription not working
- TeslaMate not publishing model data

**Solutions:**

**A) Check MQTT Subscription:**
Enable debug logging in `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.teslamate: debug
```

Restart HA and check logs for:
```
Subscribed to 46 MQTT topics for car 1
Car 1 - model = Y
```

**B) Verify MQTT Integration:**
1. Settings → Devices & Services → MQTT
2. Should show "Connected"
3. Click Configure → Listen to topic: `teslamate/cars/1/#`
4. Should see multiple messages

**C) Check TeslaMate Status:**
1. Open TeslaMate web interface
2. Verify car is shown
3. Check that data is updating
4. Look for MQTT connection status

### Issue 4: Model Sensor Shows "Y" but Device Shows "Model Unknown"

**Symptom:** 
- Entity `sensor.black_magic_model` shows state `Y`
- But device info shows "Model Unknown"

**Cause:** Device info is cached or not updating

**Solution:**
The device_info is now a property that should update dynamically. If it's not updating:

1. Delete the integration completely
2. **Restart Home Assistant**
3. Reinstall from HACS or manually
4. Re-add the integration
5. The device should now update properly

## Step 4: Verify Fix

After applying fixes:

1. **Check Home Assistant Logs:**
   ```
   Car 1 - model = Y
   Device info for car 1: model_raw='Y', model_name='Model Y', display_name='Black Magic'
   ```

2. **Check Device Page:**
   - Device name: "Black Magic" (your car's name)
   - Model: "Model Y" (not "Model Unknown")
   - Manufacturer: "Tesla"

3. **Check Entity Names:**
   - Should be: "Black Magic Battery Level"
   - Not: "Tesla 1 Battery Level" or "Tesla 3 Battery Level"

## Still Not Working?

### Enable Maximum Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.teslamate: debug
    custom_components.teslamate.coordinator: debug
    custom_components.teslamate.sensor: debug
    homeassistant.components.mqtt: debug
```

Restart HA and collect logs showing:
1. Integration startup
2. MQTT subscription confirmation
3. Model data arrival
4. Device info generation

Post these logs when asking for help.

### Check Integration Version

Make sure you have the latest version:
1. HACS → Integrations → TeslaMate
2. Click three dots → Redownload
3. Restart Home Assistant
4. Re-add integration

### Manual MQTT Test

Test if TeslaMate is publishing correctly:

```bash
# Terminal 1: Subscribe to all TeslaMate topics
mosquitto_sub -h YOUR_MQTT_IP -t "teslamate/cars/1/#" -v

# Terminal 2: Publish test model value
mosquitto_pub -h YOUR_MQTT_IP -t "teslamate/cars/1/model" -m "Y" -r

# Check Terminal 1 to see if message was received
```

If you can publish and receive test messages but TeslaMate's messages aren't arriving, the issue is with TeslaMate's MQTT configuration.
