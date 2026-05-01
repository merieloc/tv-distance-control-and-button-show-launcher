from roku import Roku
import time
import requests
from config import ROKU_IP, CHOSEN_SHOW

APP_ID = '291097' #Disney
SHOW = CHOSEN_SHOW

r = Roku(ROKU_IP)

def power_toggle():
    url = f"http://{ROKU_IP}:8060/keypress/PowerOn"
    requests.post(url, timeout=3)
    time.sleep(3)

def press(key, delay=0.4):
    getattr(r, key.lower())()
    time.sleep(delay)

def press_many(key, n):
    for _ in range(n):
        press(key)

def go_home(log):
    press_many('home', 3)
    log('Gone home')

def open_disney_app(log):
    go_home(log)
    r[APP_ID].launch()
    log('Disney loading')
    time.sleep(30)
    r.up()
    r.up()
    r.up()
    r.select()
    log('Click 1 (for User Profile 1)')
    time.sleep(10)
    r.up()
    r.up()
    r.up()
    r.select()
    log('Click 2 (for User Profile 1)')
    time.sleep(5)
    log('Disney launched')

def ensure_disney_open(log):
    while True:
        if r.active_app.id == "291097":
            log('Disney active')
            return
        else:
            log('Waiting for Disney')
            time.sleep(5)

def focus_disney_search(log):
    r.up()
    time.sleep(0.5)
    r.up()
    r.left()
    r.up()
    r.select()
    time.sleep(5)
    r.up()
    log('Disney search launched')
    time.sleep(5)

def enter_disney_text(log):
    r.literal(SHOW)
    time.sleep(2)
    r.up()
    r.select()
    log(f"{SHOW} typed")
    time.sleep(6)

def select_disney_show(log):
    r.select()
    log(f"{SHOW} selected")

def play_disney_show(log):
    power_toggle()
    open_disney_app(log)
    ensure_disney_open(log)
    focus_disney_search(log)
    enter_disney_text(log)
    select_disney_show(log)
    log(f"{SHOW} launched")

def run(log=print):
    #power_toggle()
    play_disney_show(log)
    #go_home()
    #open_disney_app()
    #r.select()
    log('Done')

if __name__ == "__main__":
    run()