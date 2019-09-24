
#!/usr/bin/env python

from papirus import PapirusTextPos
from datetime import datetime
import time
import socket


class papirus_cont(object):
    def __init__(self):

        self.papi = PapirusTextPos(False)
        self.papi.Clear()

        self.papi.AddText("DATE:", 0 ,0 ,Id="datetext")
        self.papi.AddText("00-00 00:00", 60 ,0 ,Id="date-time")

        self.papi.AddText("TEMP:", 0 ,20 ,Id="temptext")
        self.papi.AddText("00.000", 60 ,20 ,Id="temp")

        self.papi.AddText("HUME:",0,40,Id="humtext")
        self.papi.AddText("00.000",60,40,Id="hum")

        self.papi.AddText("PRES:",0,60,Id="presstxt")
        self.papi.AddText("0000",60,60,Id="press")

        self.papi.AddText("Initializing",0,80,Id="ip")

        self.papi.WriteAll()

    def set_new_datetime(self):
        self.now_time = datetime.now()
        self.papi.UpdateText("date-time",(self.now_time.strftime('%m-%d %H:%M')))

    def set_temp(self, temp):
        self.papi.UpdateText("temp","{0:.3f}".format(temp)+"[deg]")

    def set_hum(self, hum):
        self.papi.UpdateText("hum","{0:.3f}".format(hum)+"[%]")

    def set_press(self, press):
        self.papi.UpdateText("press","{0:.1f}".format(press)+"[hpa]")

    def set_ipaddress(self):
        self.ip = "0.0.0.0"

        try:
            #socket.AF_INET:IVv4のアドレス, socket.SOCK_DGRAM:UDPネットワークの
            #IPv6の場合はAF_INET→IF_INET6
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            #タイムアウトを１０秒
            self.s.settimeout(10)
            #ipアドレス8.8.8.8:80に接続します。
            # 8.8.8.8はgoogle Public DNSPCのIP。
            # 外のアドレスなら何でもいいです。
            self.s.connect(("8.8.8.8", 80))
            #今の接続のソケット名を取得します。
            self.ip=self.s.getsockname()[0]
            #IPアドレス表示
            #print(self.ip)

        except socket.error: #ネットワークがエラーだったり無かったら
            self.ip = 'No Internet'
            #print('No Internet')

        #print(type(self.ip))
        self.papi.UpdateText("ip", self.ip)

    def update(self):
        self.papi.WriteAll()



#papi.Add

#papi.UpdateText("Start", "New Text")
if __name__=='__main__':

    papi1 = papirus_cont()
    papi1.set_new_datetime()
    papi1.set_temp(12.345)
    papi1.set_hum(99.999)
    papi1.set_press(1234)
    papi1.set_ipaddress()
    papi1.update()
