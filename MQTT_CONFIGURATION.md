# Finding Your MQTT Configuration

If you're not sure what MQTT prefix or car ID to use, follow these steps:

## Step 1: Check Your TeslaMate Configuration

### Using Docker Compose
If you installed TeslaMate via Docker, check your `docker-compose.yml`:

```yaml
services:
  teslamate:
    environment:
      - MQTT_HOST=mosquitto
      - MQTT_NAMESPACE=teslamate    # <-- This is your MQTT prefix
```

The `MQTT_NAMESPACE` value is your **MQTT prefix** (default: `teslamate`)

### Using TeslaMate Environment Variables
Check your TeslaMate environment settings for:
- `MQTT_NAMESPACE` = Your MQTT prefix

## Step 2: Find Your Car ID

### Method 1: MQTT Explorer (Easiest)
1. Download [MQTT Explorer](http://mqtt-explorer.com/)
2. Connect to your MQTT broker
3. Expand the topic tree:
   ```
   teslamate/
     └── cars/
           ├── 1/          <-- Car ID 1
           │    ├── model
           │    ├── display_name
           │    └── battery_level
           └── 2/          <-- Car ID 2 (if you have multiple cars)
                ├── model
                └── ...
   ```
4. Note the number under `cars/` - that's your car ID

### Method 2: Home Assistant MQTT Tool
1. Go to **Settings** → **Devices & Services**
2. Find **MQTT** integration → Click **Configure**
3. Click **Listen to a topic**
4. Enter: `teslamate/cars/#`
5. Click **Start Listening**
6. You'll see messages like:
   ```
   teslamate/cars/1/model: Y
   teslamate/cars/1/display_name: Model Y Performance
   teslamate/cars/2/model: 3
   ```
7. The number after `cars/` is your car ID

### Method 3: TeslaMate Web Interface
1. Open your TeslaMate web interface (usually http://your-ip:4000)
2. Look at the URL when viewing your car:
   ```
   http://your-ip:4000/car/1      <-- Car ID is 1
   ```
3. If you have multiple cars, you'll see different IDs in the sidebar

### Method 4: Using mosquitto_sub Command
If you have access to the command line:

```bash
# Subscribe to all TeslaMate topics
mosquitto_sub -h YOUR_MQTT_IP -t "teslamate/cars/#" -v

# You'll see output like:
# teslamate/cars/1/model Y
# teslamate/cars/1/battery_level 85
# teslamate/cars/2/model 3
```

The number after `cars/` is the car ID.

## Common MQTT Configurations

### Default Configuration (Most Common)
- **MQTT Prefix:** `teslamate`
- **Car ID:** `1`
- **Topics:** `teslamate/cars/1/...`

### Custom Prefix
- **MQTT Prefix:** `tesla` (or whatever you set in MQTT_NAMESPACE)
- **Car ID:** `1`
- **Topics:** `tesla/cars/1/...`

### Multiple Cars
- **MQTT Prefix:** `teslamate`
- **Car IDs:** `1,2,3`
- **Topics:** 
  - `teslamate/cars/1/...`
  - `teslamate/cars/2/...`
  - `teslamate/cars/3/...`

## Integration Setup Examples

### Single Car (Default)
```
Name: TeslaMate
MQTT Prefix: teslamate
Car IDs: 1
```

### Single Car (Custom Prefix)
```
Name: TeslaMate
MQTT Prefix: tesla
Car IDs: 1
```

### Multiple Cars
```
Name: TeslaMate
MQTT Prefix: teslamate
Car IDs: 1,2,3
```

## Troubleshooting

### Not Sure Which Prefix?
Try these common values:
1. `teslamate` (default)
2. `tesla`
3. `tm`
4. Check your TeslaMate logs for "Publishing to MQTT..."

### Not Sure Which Car ID?
- First car added to TeslaMate = ID 1
- Second car added = ID 2
- And so on...
- Use MQTT Explorer to confirm

### MQTT Not Working?
See [TROUBLESHOOTING_MQTT.md](TROUBLESHOOTING_MQTT.md) for detailed diagnostics.

## What Happens During Setup

When you add the integration:

1. Integration checks if MQTT is configured in Home Assistant
2. Shows suggested MQTT prefix (defaults to `teslamate`)
3. Shows suggested car IDs (defaults to `1`)
4. You can modify these if needed
5. Integration subscribes to topics like:
   ```
   teslamate/cars/1/model
   teslamate/cars/1/battery_level
   teslamate/cars/1/charging_state
   ... (and 40+ more topics)
   ```
6. As TeslaMate publishes data, entities populate automatically

## Quick Test

After setup, check if it's working:

1. Go to **Developer Tools** → **States**
2. Search for `sensor.tesla` or `sensor.model_y`
3. You should see entities like:
   - `sensor.tesla_1_battery_level`
   - `sensor.tesla_1_charging_state`
   - `binary_sensor.tesla_1_locked`
   - `device_tracker.tesla_location`

If you see "Unknown" values, see the [troubleshooting guide](TROUBLESHOOTING_MQTT.md).
