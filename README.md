# Heatcontrol Generator

This project provides a set of Jinja2 templates and a Python script to automatically generate complex heating configurations for Home Assistant.

It interacts directly with the Home Assistant API to render templates based on your specific instance configuration (areas, devices, entities). The goal is to minimize manual configuration for heating plans, dashboards, and automations.

## Features

* **Automations**:
    * Generates heating automations for every area containing thermostats (TRVs).
    * Based on the blueprint `panhans/advanced_heating_control.yaml`.
    * Includes a "Reset" trigger that restarts all heating automations daily at 01:00 AM.
* **Intelligent Control (Binary Sensors)**:
    * Creates `binary_sensor` entities (`Heizen <Area>`).
    * **Logic**: Checks calendar entries (via labels) and determines if heating is required based on a dynamic lead time (Offset).
* **Configuration (Inputs)**:
    * **Temperatures**: Creates sliders (`input_number`) for *Eco* and *Comfort* temperatures per room.
        * Special temperature ranges for the area `kirche` (5-20°C).
        * Standard ranges for living areas (Eco: 15-20°C, Comfort: 20-25°C).
    * **Offset**: Sliders to adjust the pre-heating lead time in minutes (15-180 min).
* **Dashboard**:
    * Generates a complete Lovelace view configuration.
    * Displays warnings for devices with low battery (< 21%).
    * Visualizes current heating status.
    * Groups controls and graphs clearly by floors (e.g., Basement, Ground Floor, 1st Floor).

## Prerequisites

### Home Assistant
* **Blueprint**: The blueprint `panhans/advanced_heating_control.yaml` must be installed.
* **Frontend**: The `custom:auto-entities` card is required for the dashboard.
* **Calendars**: The logic expects calendar entities assigned to rooms via labels (matching `heatcontrol_...`).

### Python Environment
* Python 3
* `requests` library
    ```bash
    pip install requests
    ```

## Installation & Setup

### 1. Local Configuration
To allow the `generator.py` script to communicate with your Home Assistant instance, you must create two files in the project directory (these are ignored by git):

* **`hass_url.local`**: The URL of your Home Assistant instance.
    ```text
    [http://192.168.1.](http://192.168.1.)X:8123
    ```
* **`hass_token.local`**: A Long-Lived Access Token.
    * Create this in Home Assistant under *Profile -> Security -> Create Long-Lived Access Token*.
    * Paste only the token string into this file.

### 2. Generator Script
The script `generator.py` is designed to automatically find and process all template files.

## Usage

The script automatically searches for all `*.jinja` files in the current directory, renders them via the Home Assistant API, cleans up empty lines, and saves them as `.yaml` files.

Run the script using Python:

```bash
python generator.py
```

# TODO
- [ ] Dashboard - sortiere Areas nach 1. Menge der Geräte, 2. Höhe der KOmforttemperatur 