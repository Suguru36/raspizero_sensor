import sys
sys.path.insert(0,"build/lib.linux-armv7l-2.7/")

import VL53L1X
import time
from datetime import datetime

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open() # Initialise the i2c bus and configure the sensor
tof.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
distance_in_mm = tof.get_distance() # Grab the range in mm

try:
    while True:
        distance_mm = tof.get_distance()
        print("Time: {} Distance: {}mm".format(datetime.utcnow().strftime("%S.%f"), distance_mm))
        time.sleep(0.001)
except KeyboardInterrupt:
    tof.stop_ranging()


tof.stop_ranging() # Stop ranging