# Installation Guide

## Step-by-Step Installation

### 1. Prerequisites

Before installing this integration, ensure you have:

- ✅ Home Assistant installed and running
- ✅ TeslaMate installed and running
- ✅ MQTT broker (Mosquitto) configured
- ✅ Home Assistant MQTT integration configured

### 2. Verify TeslaMate MQTT

First, verify that TeslaMate is publishing to MQTT:

1. In Home Assistant, go to **Developer Tools** → **MQTT**
2. In the "Listen to a topic" field, enter: `teslamate/#`
3. Click **"Start Listening"**
4. You should see messages like:
   ```
   teslamate/cars/1/display_name: My Tesla
   teslamate/cars/1/battery_level: 85
   teslamate/cars/1/state: online
   ```

If you don't see messages, check your TeslaMate and MQTT broker configuration.

### 3. Install via HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Click on **"Integrations"**
3. Click the **three dots** (⋮) in the top right
4. Select **"Custom repositories"**
5. Enter:
   - Repository: `https://github.com/your-username/teslamate-hacs`
   - Category: **Integration**
6. Click **"Add"**
7. Find **"TeslaMate"** in the integrations list
8. Click **"Download"**
9. **Restart Home Assistant**

### 4. Manual Installation (Alternative)

If you prefer manual installation:

1. Download the latest release from GitHub
2. Extract the files
3. Copy the `custom_components/teslamate` folder to:
   ```
   config/custom_components/teslamate/
   ```
4. Your directory structure should look like:
   ```
   config/
   ├── custom_components/
   │   └── teslamate/
   │       ├── __init__.py
   │       ├── manifest.json
   │       ├── config_flow.py
   │       ├── const.py
   │       ├── coordinator.py
   │       ├── sensor.py
   │       ├── binary_sensor.py
   │       ├── device_tracker.py
   │       └── dashboard.py
   ```
5. **Restart Home Assistant**

### 5. Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"TeslaMate"**
4. Fill in the configuration:
   - **Name**: `My Tesla` (or any name you prefer)
   - **MQTT Prefix**: `teslamate` (default)
   - **Car IDs**: `1` (or comma-separated list for multiple cars)
5. Click **"Submit"**

The integration will now:
- ✅ Subscribe to all TeslaMate MQTT topics
- ✅ Create all sensor entities
- ✅ Create all binary sensor entities
- ✅ Create device tracker for location

### 6. Add Car Picture

For the best dashboard experience, add a picture of your Tesla:

1. Find or create an image of your Tesla model
   - Search online for "Tesla Model [3/S/X/Y] [color]"
   - Or take a photo of your own Tesla
2. Save the image as: `config/www/tesla_car.png`
3. Create the `www` folder if it doesn't exist
4. Recommended image size: 1920x1080 (16:9 aspect ratio)

### 7. Import Dashboard

#### Option A: YAML Dashboard

1. Go to **Settings** → **Dashboards**
2. Click **"+ Add Dashboard"**
3. Choose **"New dashboard from scratch"**
4. Name it: `Tesla`
5. Click the **three dots** (⋮) → **"Edit in YAML"**
6. Copy the content from `custom_components/teslamate/dashboard.py`
7. Paste into the YAML editor
8. Click **"Save"**

#### Option B: UI Dashboard

Create the dashboard manually using the UI editor with these cards:
- Picture entity card (with your car image)
- Entity cards for status
- Gauge cards for tire pressure
- Map card for location
- Entity rows for all sensors

### 8. Verify Installation

Check that everything is working:

1. Go to **Settings** → **Devices & Services**
2. Find the **TeslaMate** integration
3. Click on it to see:
   - ✅ 1 Device (your Tesla)
   - ✅ 40+ Sensors
   - ✅ 15+ Binary Sensors
   - ✅ 1 Device Tracker

4. Go to your new Tesla dashboard
5. Verify all data is showing correctly

## Multiple Cars

If you have multiple Teslas:

1. When configuring the integration, enter car IDs as: `1,2`
2. Each car will create a separate device
3. Entities will be named: `sensor.{car_name}_battery_level`

## Troubleshooting

### Issue: No entities created

**Solution:**
1. Check MQTT is working (Developer Tools → MQTT)
2. Verify TeslaMate is publishing: `teslamate/#`
3. Check correct car_id (default is `1`)
4. Check Home Assistant logs: Settings → System → Logs

### Issue: Entities show "Unavailable"

**Solution:**
1. Ensure TeslaMate is running
2. Check if your Tesla is awake/online
3. Verify MQTT broker is running
4. Restart Home Assistant

### Issue: Car picture not showing

**Solution:**
1. Verify image is at: `config/www/tesla_car.png`
2. Check file permissions (should be readable)
3. Try a different image format (PNG recommended)
4. Restart Home Assistant after adding image

### Issue: Wrong car_id

**Solution:**
1. Listen to MQTT topic: `teslamate/cars/#`
2. Look for your car ID in the topics
3. Update integration configuration with correct ID
4. Or remove and re-add the integration

## Uninstallation

To remove the integration:

1. Go to **Settings** → **Devices & Services**
2. Find **TeslaMate**
3. Click the **three dots** (⋮) → **"Delete"**
4. Confirm deletion
5. (Optional) Delete the `custom_components/teslamate` folder
6. Restart Home Assistant

## Next Steps

After installation:
- ✅ Create automations based on car status
- ✅ Set up notifications for charging completion
- ✅ Create climate control automations
- ✅ Monitor battery health over time
- ✅ Track charging costs
- ✅ Get alerts when car is unlocked

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Visit [Home Assistant Community Forum](https://community.home-assistant.io/)
- Open an issue on [GitHub](https://github.com/your-username/teslamate-hacs/issues)
