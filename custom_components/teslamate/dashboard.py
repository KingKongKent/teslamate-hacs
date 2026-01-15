"""Dashboard configuration for TeslaMate integration."""

# This is an example dashboard configuration
# To use: Copy this content and create a new dashboard in Home Assistant
# Or add this to your existing dashboard configuration

DASHBOARD_CONFIG = """
title: Tesla
views:
  - title: Tesla Dashboard
    path: tesla
    icon: mdi:car-electric
    badges: []
    cards:
      - type: vertical-stack
        cards:
          # Car Picture Card
          - type: picture-entity
            entity: device_tracker.tesla_1_location
            image: /local/tesla_car.png  # Add your car image to www/tesla_car.png
            name: My Tesla
            show_name: true
            show_state: true
            aspect_ratio: 16x9
            
          # Status Row
          - type: horizontal-stack
            cards:
              - type: entity
                entity: sensor.tesla_1_state
                name: Status
                icon: mdi:car-connected
              - type: entity
                entity: sensor.tesla_1_battery_level
                name: Battery
                icon: mdi:battery
              - type: entity
                entity: sensor.tesla_1_estimated_range
                name: Range
                icon: mdi:map-marker-distance
          
          # Battery & Charging Card
          - type: entities
            title: Battery & Charging
            show_header_toggle: false
            entities:
              - entity: sensor.tesla_1_battery_level
                name: Battery Level
              - entity: sensor.tesla_1_usable_battery_level
                name: Usable Battery Level
              - entity: sensor.tesla_1_charge_limit
                name: Charge Limit
              - entity: sensor.tesla_1_estimated_range
                name: Estimated Range
              - entity: sensor.tesla_1_rated_range
                name: Rated Range
              - entity: binary_sensor.tesla_1_plugged_in
                name: Plugged In
              - entity: sensor.tesla_1_charging_state
                name: Charging State
              - entity: sensor.tesla_1_charger_power
                name: Charger Power
              - entity: sensor.tesla_1_time_to_full_charge
                name: Time to Full
          
          # Climate Card
          - type: entities
            title: Climate
            show_header_toggle: false
            entities:
              - entity: binary_sensor.tesla_1_climate
                name: Climate On
              - entity: sensor.tesla_1_inside_temperature
                name: Inside Temperature
              - entity: sensor.tesla_1_outside_temperature
                name: Outside Temperature
              - entity: binary_sensor.tesla_1_preconditioning
                name: Preconditioning
          
          # Security Card
          - type: entities
            title: Security & Status
            show_header_toggle: false
            entities:
              - entity: binary_sensor.tesla_1_locked
                name: Locked
              - entity: binary_sensor.tesla_1_sentry_mode
                name: Sentry Mode
              - entity: binary_sensor.tesla_1_windows
                name: Windows
              - entity: binary_sensor.tesla_1_doors
                name: Doors
              - entity: binary_sensor.tesla_1_trunk
                name: Trunk
              - entity: binary_sensor.tesla_1_frunk
                name: Frunk
              - entity: binary_sensor.tesla_1_user_present
                name: User Present
          
          # Location Card
          - type: map
            entities:
              - entity: device_tracker.tesla_1_location
            hours_to_show: 24
            aspect_ratio: 16x9
          
          # Location Details Card
          - type: entities
            title: Location
            show_header_toggle: false
            entities:
              - entity: device_tracker.tesla_1_location
                name: Location
              - entity: sensor.tesla_1_geofence
                name: Geofence
              - entity: sensor.tesla_1_speed
                name: Speed
              - entity: sensor.tesla_1_heading
                name: Heading
              - entity: sensor.tesla_1_shift_state
                name: Shift State
          
          # Vehicle Info Card
          - type: entities
            title: Vehicle Information
            show_header_toggle: false
            entities:
              - entity: sensor.tesla_1_model
                name: Model
              - entity: sensor.tesla_1_trim_badging
                name: Trim
              - entity: sensor.tesla_1_exterior_color
                name: Color
              - entity: sensor.tesla_1_software_version
                name: Software Version
              - entity: binary_sensor.tesla_1_update_available
                name: Update Available
              - entity: sensor.tesla_1_odometer
                name: Odometer
          
          # Tire Pressure Card
          - type: horizontal-stack
            cards:
              - type: gauge
                entity: sensor.tesla_1_tire_pressure_front_left
                name: Front Left
                min: 2.0
                max: 3.5
                severity:
                  green: 2.5
                  yellow: 2.2
                  red: 0
              - type: gauge
                entity: sensor.tesla_1_tire_pressure_front_right
                name: Front Right
                min: 2.0
                max: 3.5
                severity:
                  green: 2.5
                  yellow: 2.2
                  red: 0
          
          - type: horizontal-stack
            cards:
              - type: gauge
                entity: sensor.tesla_1_tire_pressure_rear_left
                name: Rear Left
                min: 2.0
                max: 3.5
                severity:
                  green: 2.5
                  yellow: 2.2
                  red: 0
              - type: gauge
                entity: sensor.tesla_1_tire_pressure_rear_right
                name: Rear Right
                min: 2.0
                max: 3.5
                severity:
                  green: 2.5
                  yellow: 2.2
                  red: 0
"""


def get_dashboard_config():
    """Return the dashboard configuration."""
    return DASHBOARD_CONFIG
