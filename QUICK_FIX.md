## Quick Diagnostic - Check These Now

### 1. Check Home Assistant Logs
```
Settings → System → Logs
Search for: "teslamate"
```

Look for lines like:
```
Car 1 - model = Y
Car 1 - display_name = Black Magic
```

**If you DON'T see these log lines**, MQTT data isn't arriving. Check:
- Is TeslaMate running?
- Is MQTT broker running?
- Can you see `teslamate/cars/1/model` in MQTT Explorer?

**If you DO see these log lines**, the data is arriving but entities are cached.

### 2. Force Entity Name Update

The entity names are cached in Home Assistant's entity registry. To fix:

**Option A: Delete Entities (Quick)**
1. Settings → Devices & Services → Integrations → TeslaMate
2. Click on device name "Unknown"
3. Go through each entity and click the entity name
4. Click gear icon → Delete (do this for ALL entities)
5. Restart Home Assistant
6. Integration will recreate all entities with correct names

**Option B: Delete Integration (Cleaner)**
1. Settings → Devices & Services → TeslaMate → Three dots → Delete
2. **Important:** Settings → System → Restart Home Assistant
3. Add integration again
4. All entities will be created fresh with correct names

**Option C: Manual Rename (Temporary Fix)**
1. Click each entity
2. Click gear icon
3. Change name from "Tesla 3 Battery Level" to "Black Magic Battery Level"
4. Repeat for all ~60 entities (tedious but works)

### 3. Verify MQTT Data

To confirm TeslaMate is publishing the model:

**Home Assistant MQTT Listener:**
```
Settings → Devices & Services → MQTT → Configure
Listen to topic: teslamate/cars/1/model
Start Listening
```

Should show: `Y` (single letter)

If it shows `3` or something else, that's your problem - TeslaMate is publishing the wrong model.

### 4. Check TeslaMate Directly

Open TeslaMate web interface and check:
- Is your car showing as Model Y?
- What does the URL show? (e.g., `/car/1` means car_id = 1)

---

## Expected Result After Fix

**Device Info:**
- Name: "Black Magic"
- Model: "Model Y"
- Manufacturer: "Tesla"

**Entity Names:**
- "Black Magic Battery Level"
- "Black Magic Charging State"
- "Black Magic Locked"
- etc.

Not "Tesla 3" or "Tesla 1"

---

Let me know what you find in the logs!
