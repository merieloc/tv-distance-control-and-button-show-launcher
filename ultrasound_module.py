from gpiozero import DistanceSensor
from time import sleep
from roku import Roku
from config import ROKU_IP, ULTRASOUND_PINS

def run_ultrasound(stop_flag):
    sleep(0.5)

    r = Roku(ROKU_IP)

    sensor_R = DistanceSensor(**ULTRASOUND_PINS["R"], max_distance=2)
    sensor_M = DistanceSensor(**ULTRASOUND_PINS["M"], max_distance=2)
    sensor_L = DistanceSensor(**ULTRASOUND_PINS["L"], max_distance=2)

    threshold_activity = 20 #cm
    delay = 0.05 #gap to prevent interference
    paused = False

    def read_distance(sensor):
        return sensor.distance * 100

    try:
        while not stop_flag["stop"]:
            d_R = read_distance(sensor_R)
            sleep(delay)
            d_M = read_distance(sensor_M)
            sleep(delay)
            d_L = read_distance(sensor_L)
            sleep(delay)
            
            d_min = min(d_R, d_M, d_L)
            d_min_dict = {'Right': d_R, 'Middle': d_M, 'Left': d_L}
            smallest_var_name = min(d_min_dict, key=d_min_dict.get)
            
            print(f"L:{d_L:.0f}cm, M:{d_M:.0f}cm, R:{d_R:.0f}cm, Closest sensor={smallest_var_name}")
            
            if d_min < threshold_activity and not paused:
                paused = True
                r.play()
                print(f"Too close. Distance: {d_min:.0f}cm. Paused:{paused}")
        #        sleep(3) #punishment
            elif d_min >= threshold_activity and paused:
                paused = False
                r.play()
                print(f"Good to go. Distance: {d_min:.0f}cm. Paused:{paused}")
            else:
                print('Paused status', paused)
    finally:     
        print("Closing sensors...")
        sensor_R.close()
        sensor_M.close()
        sensor_L.close()
        sleep(0.3)
