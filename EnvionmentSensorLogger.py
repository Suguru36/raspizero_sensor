#!/usr/bin/env python

from papirus_cont import papirus_cont
from Bme280Cnt import Bme280Cnt
from time import sleep
import ambient
#
# Ambient Livraryが必要です。
#　https://ambidata.io/refs/python/
#


class EnvionmentSensorLogger(object):

    def __init__(self):
        self.papi = papirus_cont()
        self.Bme280 = Bme280Cnt()
        self.ambi = ambient.Ambient(4779, "95a3ddcb3130ffe7")

    def get_bme280_data(self):
        self.Bme280.readDataFromBme280()
        self.humid = self.Bme280.getHumData()
        self.temp =  self.Bme280.getTempData()
        self.press = self.Bme280.getPresData()
    
    def disp_data(self):
        self.papi.set_new_datetime()
        self.papi.set_hum(self.humid)
        self.papi.set_temp(self.temp)
        self.papi.set_press(self.press)
        self.papi.set_ipaddress()
        self.papi.update()

    def sendDataToAmbient(self):
        self.r = self.ambi.send({"d1": self.temp, "d2": self.humid ,"d3": self.press})

    def network_state(self):
        if ((self.papi.get_network_state()) == 'No Internet'):
            return False
        else:
            return True


#------------------------------------------
if __name__ == "__main__":
    Sens = EnvionmentSensorLogger()

    while(True):
        Sens.get_bme280_data()
        Sens.disp_data()
        if (Sens.network_state()):
            Sens.sendDataToAmbient()
        else:
            pass

        sleep(10)

