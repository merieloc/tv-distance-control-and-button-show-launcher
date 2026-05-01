from gpiozero import LED, Button
from signal import pause
import time
import threading
import signal
import sys

from ultrasound_module import run_ultrasound
import play_chosen_show
import tv_power_off
from config import LED_PIN, BUTTON_PIN
from OLED_module import OLEDDisplay 

# -----------------------
# GPIO SETUP
# -----------------------
led = LED(LED_PIN)
button = Button(BUTTON_PIN, hold_time=2)
oled = OLEDDisplay()

# -----------------------
# STATE
# -----------------------
ignore_release = False
last_press_time = 0
cooldown = 10

ultra_thread = None
ultra_stop = {"stop": False}

# -----------------------
# OLED LOGGER
# -----------------------
def log(msg):
    print(msg)
    oled.add_line(msg)

# -----------------------
# ULTRASOUND CONTROL
# -----------------------
def start_ultrasound():
    global ultra_thread, ultra_stop

    if ultra_thread is not None:
        log("Ultrasound already running")
        return

    log("Starting ultrasound")

    ultra_stop = {"stop": False}

    ultra_thread = threading.Thread(
        target=run_ultrasound,
        args=(ultra_stop,),
        daemon=True
    )
    ultra_thread.start()


def stop_ultrasound():
    global ultra_thread, ultra_stop

    if ultra_thread is None:
        return

    log("Stopping ultrasound")

    ultra_stop["stop"] = True
    ultra_thread.join()
    ultra_thread = None

# -----------------------
# BUTTON ACTIONS
# -----------------------
def run_tv(log=log):
    global last_press_time, ignore_release

    now = time.time()

    if ignore_release:
        ignore_release = False
        return

    if now - last_press_time < cooldown:
        log("Ignored press (cooldown)")
        return

    led.on()

    try:
        play_chosen_show.run(log=log)
        log("Launching TV and show")
        success = True
    except Exception as e:
        log(f"TV script failed: {e}")
        success = False

    led.off()
    
    if success:
        time.sleep(5)
        start_ultrasound()

    last_press_time = now


def power_off():
    global ignore_release

    log("Powering off TV")

    stop_ultrasound()

    tv_power_off.run()

    led.off()

    ignore_release = True

# -----------------------
# CLEANUP (CRITICAL)
# -----------------------
def cleanup(signum, frame):
    print("Cleaning up...")

    stop_ultrasound()

    led.close()
    button.close()
    oled.clear()

    time.sleep(0.3)

    sys.exit(0)

# -----------------------
# EVENT BINDINGS
# -----------------------
button.when_released = run_tv
button.when_held = power_off

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# -----------------------
# MAIN LOOP
# -----------------------
log("System ready. Waiting for button...")

pause()
