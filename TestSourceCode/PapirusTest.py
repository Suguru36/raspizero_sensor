#!/usr/bin/env python


from papirus import PapirusTextPos


papi = PapirusTextPos()

papi.AddText("00-00 00:00", 0 ,0 ,Id="date-time")
papi.AddText("00.000", 0 ,20 ,Id="temp")
#papi.Add

papi.UpdateText("Start", "New Text")