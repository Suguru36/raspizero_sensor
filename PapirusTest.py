#!/usr/bin/env python


#from papirus import PapirusTextPos


#papi = PapirusTextPos()

#papi.AddText("00-00 00:00", 0 ,0 ,Id="date-time")
#papi.AddText("00.000", 0 ,20 ,Id="temp")
#papi.Add

#papi.UpdateText("Start", "New Text")
from papirus import Papirus

# The epaper screen object.
# Optional rotation argument: rot = 0, 90, 180 or 270 degrees
screen = Papirus([rotation = 90])

# Write a bitmap to the epaper screen
screen.display('./path/to/bmp/image')

# Perform a full update to the screen (slower)
screen.update()

# Update only the changed pixels (faster)
screen.partial_update()

# Update only the changed pixels with user defined update duration
screen.fast_update()

# Disable automatic use of LM75B temperature sensor
screen.use_lm75b = False