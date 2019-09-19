import smbus
from time import sleep



class Bme280Cnt(object):

	self._slave_addres = 0x76
	self.Temp = []
	self.Pres = []
	self.Humi = []
	self.tt = 0.0

	# Initialize Sensor
	def __init__(self):
		self.bus = smbus.SMBus(1)

		self.Tovs = 1     # Temperature oversampling x 1
		self.Povs = 1     # Pressure oversampling x 1
		self.Hovs = 1     # Humidity oversampling x 1
		self.mode   = 3   # Normal mode
		self.stby   = 5   # Tstandby 1000ms
		self.filter = 0   # Filter off
		self.spion = 0    # 3-wire SPI Disable

		self.ctrl_meas_reg = (self.Tovs << 5) | (self.Povs << 2) | self.mode
		self.config_reg    = (self.stby << 5) | (self.filter << 2) | self.spion
		self.ctrl_hum_reg  = self.Hovs

		self.writeSensor(0xF2, self.ctrl_hum_reg)
		self.writeSensor(0xF4, self.ctrl_meas_reg)
		self.writeSensor(0xF5, self.config_reg)

		self.getCalibration()
		self.readDataFromBme280()



	# Write Sensor I2C
	def writeSensor(self, reg_addr, data):
		self.bus.write_byte_data(_slave_addres, reg_addr, data)


	# Get Calibration Data
	def getCalibration(self):
		self.calib = []

		for i in range(0x88, 0x88+24):
			self.calib.append(bus.read_byte_data(0x76, i))
		self.calib.append(self.bus.read_byte_data(0x76, 0xA1))
		for i in range(0xE1, 0xE1+7):
			self.calib.append(self.bus.read_byte_data(0x76, i))

		self.Temp.append((self.calib[1] << 8) | self.calib[0])
		self.Temp.append((self.calib[3] << 8) | self.calib[2])
		self.Temp.append((self.calib[5] << 8) | self.calib[4])
		self.Pres.append((self.calib[7] << 8) | self.calib[6])
		self.Pres.append((self.calib[9] << 8) | self.calib[8])
		self.Pres.append((self.calib[11]<< 8) | self.calib[10])
		self.Pres.append((self.calib[13]<< 8) | self.calib[12])
		self.Pres.append((self.calib[15]<< 8) | self.calib[14])
		self.Pres.append((self.calib[17]<< 8) | self.calib[16])
		self.Pres.append((self.calib[19]<< 8) | self.calib[18])
		self.Pres.append((self.calib[21]<< 8) | self.calib[20])
		self.Pres.append((self.calib[23]<< 8) | self.calib[22])
		self.Humi.append( self.calib[24] )
		self.Humi.append((self.calib[26]<< 8) | self.calib[25])
		self.Humi.append( self.calib[27] )
		self.Humi.append((self.calib[28]<< 4) | (0x0F & self.calib[29]))
		self.Humi.append((self.calib[30]<< 4) | ((self.calib[29] >> 4) & 0x0F))
		self.Humi.append( self.calib[31] )

		for i in range(1,2):
			if self.Temp[i] & 0x8000:
				self.Temp[i] = (-self.Temp[i] ^ 0xFFFF) + 1

		for i in range(1,8):
			if self.Pres[i] & 0x8000:
				self.Pres[i] = (-self.Pres[i] ^ 0xFFFF) + 1

		for i in range(0,6):
			if self.Humi[i] & 0x8000:
				self.Humi[i] = (-self.Humi[i] ^ 0xFFFF) + 1


	# Read Now Temperature,Pressure,Humidity
	def readDataFromBme280(self):
		self.data = []
		for i in range(0xF7, 0xF7+8):
			self.data.append(bus.read_byte_data(0x76, i))
		self.pres = (self.data[0] << 12) | (self.data[1] << 4) | (self.data[2] >> 4)
		self.temp = (self.data[3] << 12) | (self.data[4] << 4) | (self.data[5] >> 4)
		self.humi = (self.data[6] << 8)  |  self.data[7]

		self.t2 = self.adjustTemp(self.temp)
		self.p2 = self.adjustPres(self.pres)
		self.h2 = self.adjustHumi(self.humi)

	# Adjust Pressure by Calibration
	def adjustPres(self, nowpres):
#		global  tt
		self.pressure = 0.0

		self.v1 = (self.tt / 2.0) - 64000.0
		self.v2 = (((self.v1 / 4.0) * (self.v1 / 4.0)) / 2048) * self.Pres[5]
		self.v2 = self.v2 + ((v1 * self.Pres[4]) * 2.0)
		self.v2 = (self.v2 / 4.0) + (self.Pres[3] * 65536.0)
		self.v1 = (((self.Pres[2] * (((self.v1 / 4.0) * (self.v1 / 4.0)) / 8192)) / 8) \
			+ ((self.Pres[1] * self.v1) / 2.0)) / 262144
		self.v1 = ((32768 + self.v1) * self.Pres[0]) / 32768

		if self.v1 == 0:
			return 0
		self.pressure = ((1048576 - self.nowpres) - (self.v2 / 4096)) * 3125
		if self.pressure < 0x80000000:
			self.pressure = (self.pressure * 2.0) / self.v1
		else:
			self.pressure = (self.pressure / self.v1) * 2
		self.v1 = (self.Pres[8] * (((self.pressure / 8.0) * (self.pressure / 8.0)) \
			/ 8192.0)) / 4096
		self.v2 = ((self.pressure / 4.0) * self.Pres[7]) / 8192.0
		self.pressure = self.pressure + ((self.v1 + self.v2 + self.Pres[6]) / 16.0)

		return self.pressure/100


	# Adjust Temperature by Calibration
	def adjustTemp(self, nowtemp):
#		global tt
		self.v1 = (self.nowtemp / 16384.0 - self.Temp[0] / 1024.0) * self.Temp[1]
		self.v2 = (self.nowtemp / 131072.0 - self.Temp[0] / 8192.0) \
			* (self.nowtemp / 131072.0 - self.Temp[0] / 8192.0) * self.Temp[2]
		self.tt = self.v1 + self.v2
		self.temperature = self.tt / 5120.0

		return self.temperature


	# Adjust Humidity by Calibration
	def adjustHumi(self, nowhumi):
#		global tt
		self.var_h = self.tt - 76800.0
		if self.var_h != 0:
			self.var_h = (self.nowhumi - (self.Humi[3] * 64.0 + self.Humi[4]/16384.0 \
					* self.var_h)) * (self.Humi[1] / 65536.0 * (1.0 \
					+ self.Humi[5] / 67108864.0 * self.var_h * (1.0 \
					+ self.Humi[2] / 67108864.0 * self.var_h)))
		else:
			return 0
		self.var_h = self.var_h * (1.0 - self.Humi[0] * self.var_h / 524288.0)
		if self.var_h > 100.0:
			self.var_h = 100.0
		elif self.var_h < 0.0:
			self.var_h = 0.0

		return self.var_h

#-----------------------------------------------
	def getTempData(self):
		return (self.t2)

	def getPresData(self):
		return (self.p2)

	def getHumData(self):
		return (self.h2)




#------------------------------------------------------

if name == '__main__':

	sens1 = Bme280()
	sens1.readDataFromBme280()
	print(sens1.getTempData)
	print(sens1.getPresData)
	print(sens1.getHumData)

