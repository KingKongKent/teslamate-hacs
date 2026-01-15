# Example Automations for TeslaMate

This file contains example automations you can use with your TeslaMate integration.

## Installation

Copy the automation examples below and add them to your Home Assistant automations:
- Go to Settings → Automations & Scenes
- Click "+ Create Automation"
- Click the three dots → "Edit in YAML"
- Paste the automation code
- Modify entity names to match your car

---

## 1. Notify When Charging Complete

Get a notification when your Tesla finishes charging:

```yaml
alias: Tesla - Charging Complete Notification
description: Send notification when Tesla charging is complete
trigger:
  - platform: state
    entity_id: sensor.tesla_1_charging_state
    to: "Complete"
condition: []
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "🔋 Tesla Charging Complete"
      message: "Your Tesla is fully charged to {{ states('sensor.tesla_1_battery_level') }}%"
      data:
        notification_icon: mdi:battery-charging-100
mode: single
```

---

## 2. Climate Control Before Departure

Start climate control 10 minutes before you typically leave:

```yaml
alias: Tesla - Morning Climate Control
description: Pre-condition Tesla before morning departure
trigger:
  - platform: time
    at: "07:50:00"
condition:
  - condition: state
    entity_id: device_tracker.tesla_1_location
    state: "home"
  - condition: numeric_state
    entity_id: sensor.tesla_1_battery_level
    above: 20
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "🌡️ Tesla Climate Starting"
      message: "Pre-conditioning your Tesla for departure"
      data:
        actions:
          - action: "STOP_CLIMATE"
            title: "Stop Climate"
mode: single
```

---

## 3. Low Battery Alert

Get alerted when battery drops below 20%:

```yaml
alias: Tesla - Low Battery Alert
description: Alert when Tesla battery is low
trigger:
  - platform: numeric_state
    entity_id: sensor.tesla_1_battery_level
    below: 20
condition:
  - condition: state
    entity_id: binary_sensor.tesla_1_plugged_in
    state: "off"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "⚠️ Tesla Battery Low"
      message: "Your Tesla battery is at {{ states('sensor.tesla_1_battery_level') }}%. Consider charging soon."
      data:
        notification_icon: mdi:battery-alert
        tag: "tesla_low_battery"
        priority: high
mode: single
```

---

## 4. Unlocked Away From Home Alert

Get notified if your Tesla is unlocked while away from home:

```yaml
alias: Tesla - Unlocked Away from Home
description: Alert if Tesla is unlocked while not at home
trigger:
  - platform: state
    entity_id: binary_sensor.tesla_1_locked
    to: "on"  # Note: inverted in integration, "on" means unlocked
condition:
  - condition: not
    conditions:
      - condition: state
        entity_id: device_tracker.tesla_1_location
        state: "home"
  - condition: state
    entity_id: binary_sensor.tesla_1_user_present
    state: "off"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "🔓 Tesla Unlocked"
      message: "Your Tesla is unlocked at {{ states('sensor.tesla_1_geofence') }}"
      data:
        notification_icon: mdi:lock-open-alert
        tag: "tesla_unlocked"
        priority: high
        actions:
          - action: "VIEW_LOCATION"
            title: "View Location"
mode: single
```

---

## 5. Sentry Mode Auto-Enable Away From Home

Automatically enable sentry mode when leaving home:

```yaml
alias: Tesla - Auto Enable Sentry Mode
description: Enable sentry mode when leaving home
trigger:
  - platform: state
    entity_id: device_tracker.tesla_1_location
    from: "home"
condition:
  - condition: state
    entity_id: binary_sensor.tesla_1_sentry_mode
    state: "off"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "🛡️ Tesla Sentry Mode"
      message: "Your Tesla left home. Enable Sentry Mode?"
      data:
        notification_icon: mdi:shield-car
        actions:
          - action: "ENABLE_SENTRY"
            title: "Enable"
          - action: "DISMISS"
            title: "No Thanks"
mode: single
```

---

## 6. Track Charging Costs

Log charging costs based on your electricity rate:

```yaml
alias: Tesla - Log Charging Cost
description: Calculate and log charging session cost
trigger:
  - platform: state
    entity_id: sensor.tesla_1_charging_state
    to: "Complete"
variables:
  energy_added: "{{ states('sensor.tesla_1_charge_energy_added') | float }}"
  cost_per_kwh: 0.12  # Update with your electricity rate
  total_cost: "{{ (energy_added * cost_per_kwh) | round(2) }}"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "💰 Charging Cost"
      message: "Added {{ energy_added }} kWh. Cost: ${{ total_cost }}"
  - service: logbook.log
    data:
      name: "Tesla Charging"
      message: "Charging complete. Added {{ energy_added }} kWh for ${{ total_cost }}"
      entity_id: sensor.tesla_1_battery_level
mode: single
```

---

## 7. Windows or Doors Open Alert

Alert if windows or doors are left open:

```yaml
alias: Tesla - Windows or Doors Open
description: Alert if windows or doors are left open for 5 minutes
trigger:
  - platform: state
    entity_id:
      - binary_sensor.tesla_1_windows
      - binary_sensor.tesla_1_doors
    to: "on"
    for:
      minutes: 5
condition: []
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "⚠️ Tesla Open"
      message: >
        {% if is_state('binary_sensor.tesla_1_windows', 'on') %}
          Windows are open
        {% elif is_state('binary_sensor.tesla_1_doors', 'on') %}
          Doors are open
        {% endif %}
        at {{ states('sensor.tesla_1_geofence') }}
      data:
        notification_icon: mdi:car-door
        tag: "tesla_open"
mode: single
```

---

## 8. Start Charging During Off-Peak Hours

Automatically start charging during off-peak electricity hours:

```yaml
alias: Tesla - Off-Peak Charging
description: Start charging during off-peak hours if needed
trigger:
  - platform: time
    at: "23:00:00"  # Off-peak start time
condition:
  - condition: state
    entity_id: binary_sensor.tesla_1_plugged_in
    state: "on"
  - condition: numeric_state
    entity_id: sensor.tesla_1_battery_level
    below: 80
  - condition: state
    entity_id: sensor.tesla_1_charging_state
    state: "Stopped"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "⚡ Off-Peak Charging"
      message: "Starting off-peak charging to {{ states('sensor.tesla_1_charge_limit') }}%"
      data:
        notification_icon: mdi:ev-station
mode: single
```

---

## 9. Arrived Home Automation

Trigger actions when arriving home:

```yaml
alias: Tesla - Arrived Home
description: Actions when Tesla arrives home
trigger:
  - platform: state
    entity_id: device_tracker.tesla_1_location
    to: "home"
condition: []
action:
  - service: light.turn_on
    target:
      entity_id: light.garage
  - service: cover.open_cover
    target:
      entity_id: cover.garage_door
  - service: notify.mobile_app_your_phone
    data:
      title: "🏠 Welcome Home"
      message: "Tesla arrived. Garage door opening and lights on."
mode: single
```

---

## 10. Software Update Available Notification

Get notified when a Tesla software update is available:

```yaml
alias: Tesla - Software Update Available
description: Notify when Tesla software update is available
trigger:
  - platform: state
    entity_id: binary_sensor.tesla_1_update_available
    to: "on"
condition: []
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "🔄 Tesla Update Available"
      message: >
        Tesla software update available: {{ states('sensor.tesla_1_available_update_version') }}
        Current version: {{ states('sensor.tesla_1_software_version') }}
      data:
        notification_icon: mdi:update
        tag: "tesla_update"
        actions:
          - action: "VIEW_RELEASE_NOTES"
            title: "Release Notes"
mode: single
```

---

## 11. Tire Pressure Warning

Alert when tire pressure is low:

```yaml
alias: Tesla - Low Tire Pressure Alert
description: Alert when any tire pressure is low
trigger:
  - platform: numeric_state
    entity_id:
      - sensor.tesla_1_tire_pressure_front_left
      - sensor.tesla_1_tire_pressure_front_right
      - sensor.tesla_1_tire_pressure_rear_left
      - sensor.tesla_1_tire_pressure_rear_right
    below: 2.3  # BAR - adjust for your preference
condition: []
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "⚠️ Low Tire Pressure"
      message: >
        FL: {{ states('sensor.tesla_1_tire_pressure_front_left') }} BAR
        FR: {{ states('sensor.tesla_1_tire_pressure_front_right') }} BAR
        RL: {{ states('sensor.tesla_1_tire_pressure_rear_left') }} BAR
        RR: {{ states('sensor.tesla_1_tire_pressure_rear_right') }} BAR
      data:
        notification_icon: mdi:car-tire-alert
        tag: "tesla_tire_pressure"
        priority: high
mode: single
```

---

## 12. Charge Limit Reminder for Trip

Set reminder to increase charge limit before a trip:

```yaml
alias: Tesla - Weekend Trip Charge Reminder
description: Remind to increase charge limit on Friday evening
trigger:
  - platform: time
    at: "18:00:00"
condition:
  - condition: time
    weekday:
      - fri
  - condition: numeric_state
    entity_id: sensor.tesla_1_charge_limit
    below: 90
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "🚗 Weekend Trip Reminder"
      message: "Don't forget to increase charge limit to 90% for your weekend trip!"
      data:
        notification_icon: mdi:car-battery
        actions:
          - action: "OPEN_TESLA_APP"
            title: "Open Tesla App"
mode: single
```

---

## Tips for Customization

### Update Entity Names
Replace `tesla_1` with your actual car's entity prefix:
```yaml
sensor.tesla_1_battery_level
# becomes
sensor.blue_thunder_battery_level
```

### Adjust Thresholds
Modify numeric values based on your preferences:
- Battery levels
- Tire pressures
- Time delays
- Temperature thresholds

### Add Multiple Cars
For multiple Teslas, duplicate automations and update entity IDs:
```yaml
- sensor.tesla_1_battery_level
- sensor.tesla_2_battery_level
```

### Testing
Use the automation trace feature to debug:
1. Settings → Automations & Scenes
2. Click on automation
3. Click "Trace" to see execution history

---

## Advanced: Template Sensors

Create custom sensors for advanced tracking:

```yaml
# Add to configuration.yaml
template:
  - sensor:
      - name: "Tesla Efficiency"
        unit_of_measurement: "Wh/km"
        state: >
          {% set power = states('sensor.tesla_1_power') | float %}
          {% set speed = states('sensor.tesla_1_speed') | float %}
          {% if speed > 0 %}
            {{ (power / speed) | round(0) }}
          {% else %}
            0
          {% endif %}
        
      - name: "Tesla Range Anxiety"
        state: >
          {% set battery = states('sensor.tesla_1_battery_level') | int %}
          {% set plugged = is_state('binary_sensor.tesla_1_plugged_in', 'on') %}
          {% if plugged %}
            Charging
          {% elif battery < 15 %}
            Critical
          {% elif battery < 30 %}
            Low
          {% else %}
            Good
          {% endif %}
```

---

## Need More Ideas?

Check out the Home Assistant community forum for more automation ideas:
- [Home Assistant Community](https://community.home-assistant.io/)
- Search for "Tesla automations"
- Share your own creations!
