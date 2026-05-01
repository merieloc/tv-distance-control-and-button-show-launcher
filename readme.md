# Raspberry Pi TV Controller with OLED Feedback

## Overview

This project turns a Raspberry Pi into a physical “one-button TV controller” with proximity-based pause control and real-time feedback on an OLED display.

It integrates:

* GPIO button input
* LED status indication
* Ultrasonic distance sensors
* Roku TV control over network
* SSD1306 OLED display for system output

The system is designed to behave like an appliance: press a button to launch a show, and automatically pause playback if someone gets too close to the screen.

---

## Features

* **Single-button control**

  * Short press: turn on TV and launch a selected show
  * Long press: power off TV

* **Automatic proximity pause**

  * Uses three ultrasonic sensors
  * Pauses playback if viewer is too close
  * Resumes when distance is safe

* **OLED display output**

  * Shows system status and actions
  * Scrolls messages if too long

* **Threaded architecture**

  * Non-blocking ultrasound monitoring
  * Clean startup/shutdown handling

---

## Hardware Requirements

* Raspberry Pi (any model with GPIO + I2C)
* SSD1306 OLED display (128x32, I2C)
* 1x Push button
* 1x LED
* 3x Ultrasonic sensors (HC-SR04 or similar)
* Resistors / wiring as needed

---

## Pin Configuration

Defined in `config.py`:

```python
LED_PIN = 5
BUTTON_PIN = 6

ULTRASOUND_PINS = {
    "R": {"echo": 24, "trigger": 23},
    "M": {"echo": 27, "trigger": 17},
    "L": {"echo": 25, "trigger": 22},
}
```

---

## Software Requirements

Install dependencies:

```bash
pip install gpiozero adafruit-circuitpython-ssd1306 pillow requests roku
```

Enable I2C on the Pi:

```bash
sudo raspi-config
# Interface Options → I2C → Enable
```

---

## Configuration

### 1. Create a local config file

Create `config_local.py` (this file is ignored by Git):

```python
ROKU_IP = "192.168.x.x"
```

### 2. Base config (`config.py`)

Contains safe defaults and imports local overrides:

```python
try:
    from config_local import *
except ImportError:
    pass
```

---

## Usage

Run the system:

```bash
python3 combined_tv_controller.py
```

### Controls

* **Short press button**

  * Turns on TV
  * Launches configured show
  * Starts proximity monitoring

* **Long press (hold ~2s)**

  * Powers off TV
  * Stops sensors

---

## Project Structure

```text
.
├── combined_tv_controller.py   # Main entry point
├── OLED_module.py              # OLED display driver
├── ultrasound_module.py        # Distance sensing + pause logic
├── play_chosen_show.py         # Roku automation (launch show)
├── tv_power_off.py             # Roku power off
├── config.py                   # Shared configuration
├── config_local.py             # Local overrides (not tracked)
```

---

## Logging Design

The system uses a pluggable logging pattern:

```python
def run(log=print):
```

* Defaults to `print` when run standalone
* Accepts a custom logger from the controller
* Enables OLED + console output simultaneously

---

## Notes / Design Decisions

* **Single-process architecture**

  * Avoids GPIO locking issues (`GPIO busy`)
  * Ensures clean signal handling and shutdown

* **OLED as a component**

  * Not a wrapper process
  * Prevents orphaned subprocesses

* **Threaded ultrasound monitoring**

  * Runs independently of button/UI logic
  * Cleanly stopped via shared flag

---

## Troubleshooting

### GPIO busy error

* Ensure previous script is not still running:

  ```bash
  pkill -f combined_tv_controller.py
  ```

### OLED not displaying messages

* Ensure logging is routed through `log(...)`
* `print()` alone will not appear on OLED

### Roku not responding

* Verify IP in `config_local.py`
* Ensure Pi and Roku are on same network

---

## Future Improvements

* State machine for cleaner control flow
* Better OLED UI (icons, status indicators)
* Configurable shows via menu
* Async I/O instead of threads
* Debounce improvements for button handling

---

## Author

By [Meriel O'Conor](https://www.linkedin.com/in/merieloconor/)

Your Name
