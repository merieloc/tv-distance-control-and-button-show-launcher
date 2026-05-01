from roku import Roku
import time
import requests
from config import ROKU_IP

r = Roku(ROKU_IP)

def power_toggle():
    url = f"http://{ROKU_IP}:8060/keypress/PowerOff"
    requests.post(url, timeout=3)
    time.sleep(3)

def run():
    power_toggle()
    print('Power Off')

if __name__ == "__main__":
    run()
