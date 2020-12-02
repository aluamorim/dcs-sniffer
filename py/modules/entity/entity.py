
"""
	entity.py

	This Module defines all basic objects used in the
	system

	Author: Anderson Amorim
	Date: 23/02/2017
"""
import sys
import time
import datetime
import random
import ctypes
import numpy as np
from ..definitions import *
from math import pow, sqrt, exp, atan


####################################################################
class Entity(object):
	raw_data = []

	def load(self, byteArray):
		pass
	
	def toArray(self):
		return self.raw_data

	def toString(self):
		vec = self.toArray()
		return ''.join((map(chr, vec)))
	
	def timeStamp(self):
		pass

####################################################################
class Command(Entity):

	id=0
	resp_id=0
	result=0
	param=0

	def __init__(self, id=None):
		self.id = id
		self.resp_id = 0
		self.param = [0,0,0,0,0,0,0,0,0]

	def setId(self, newId):
		self.id = newId

	def getId(self):
		return self.id

	def setParam(self, bytes):
		self.param = bytes

	def getParam(self, newParam):
		return self.param

	def toArray(self):
		vec = [self.id, self.resp_id, self.result]
		return sum([self.param],vec)

	# builds a command instance using
	# the first 10 bytes of the array
	def load(self, byteArray):
		if (len(byteArray) >=12):
			self.id = byteArray[0]
			self.resp_id = byteArray[1]
			self.result = byteArray[2]
			self.param = byteArray[3:12] # 12 is exclusive
	
	def timeStamp(self):
		return ''

####################################################################
class RTC(Entity):
	YEAR = 0
	MONTH = 0
	DAY = 0
	HOUR = 0
	MINUTE = 0
	SECOND = 0 
	WEEK = 0
	WDAY = 0

	def __init__(self):
		now = datetime.datetime.now()
		self.YEAR = now.year-1900
		self.MONTH = now.month
		self.DAY = now.day
		self.HOUR = now.hour
		self.MINUTE = now.minute
		self.SECOND = now.second
		self.WEEK = 0
		self.WDAY = 0


	def load(self, byteArray):
		if (len(byteArray) > 4):
			self.YEAR = byteArray[0]
			self.MONTH = byteArray[1]
			self.DAY = byteArray[2]
			self.HOUR = byteArray[3]
			self.MINUTE = byteArray[4]
			self.SECOND = byteArray[5]
			if (len(byteArray)>6):
				self.WEEK = byteArray[6]
				self.WDAY = byteArray[7]
			else:
				self.WEEK = 1
				self.WDAY = 1
		
	def toArray(self):
		return [self.YEAR,self.MONTH,self.DAY,self.HOUR,self.MINUTE,self.SECOND,self.WEEK ,self.WDAY]

	def timeStamp (self):
		return "%02d/%02d/%04d %02d:%02d:%02d"%(self.DAY, self.MONTH, (self.YEAR+1900), self.HOUR, self.MINUTE, self.SECOND)

####################################################################
class Package(Entity):

	PCKG_TYPES = ['PTT', 'HK', 'ADC', 'ACK']
	PCKG_TYPE_HK = 'HK'
	PCKG_TYPE_PTT = 'PTT'
	PCKG_TYPE_ADC = 'ADC'
	PCKG_TYPE_ACK = 'ACK'
	typeStr=''

	pckgType=0 # 1 byte
	
	def __init__(self):
		super().__init__(self)


####################################################################
class HKPackage(Package):
	adc_rms = 0 # 2 byte
	current_sensor1 = 0 # 2 bytes
	current_sensor2 = 0 # 2 bytes
	pll_sync = 0	# 1 byte
	over_current_fail = 0 # 1 byte
	timeTag  = [] # 8 byte

	def __init__(self, dummy=False):
		
		self.typeStr = Package.PCKG_TYPES[1] # self.typeStr='HK'

		if (dummy==True):
			#b = range(0, 56)
			b = [random.randint(0,127) for p in range(0,HK_PACKAGE_SIZE)]
			self.load(b)
			rtc = RTC()
			self.timeTag = rtc.toArray()

	def load(self, byteArray):
		if (len(byteArray) < HK_PACKAGE_SIZE):
			return -1

		self.pckgType = byteArray[0]
		# skip byte 01
		self.adc_rms = (byteArray[2] & 0x00FF)
		self.adc_rms |= ((byteArray[3])<<8)

		self.current_sensor1 = (byteArray[4] & 0x00FF)
		self.current_sensor1 |= (byteArray[5]<<8)

		self.current_sensor2 = (byteArray[6] & 0x00FF)
		self.current_sensor2 |= (byteArray[7]<<8)


		self.pll_sync = byteArray[8]
		self.over_current_fail = byteArray[9]

		self.timeTag  = list(byteArray[HK_TIME_TAG_START:(HK_TIME_TAG_START+HK_TIME_TAG_LENGTH)])
		
		self.raw_data = byteArray

	def timeStamp(self):
		rtc = RTC()
		rtc.load(self.timeTag)
		return rtc.timeStamp()

####################################################################
class PTTPackage(Package):
	
	pttIdNumber = 0   # 2 bytes
	ampRms = 0 	 # 2 bytes
	freqMeasure = 0 # 4 bytes (24bits)
	decoderNumber = 0 # 1 byte
	msgLength = 0 # 1 byte
	timeTag = [] #lock time (8 bytes)
	sensorData = [] # 32 bytes
	crc = 0x0000 # 2 bytes

	localCRC=0x00  # locally calculated crc

	def __init__(self, dummy=False):
		self.typeStr = Package.PCKG_TYPES[0] # self.typeStr='PTT'
		if (dummy==True):
			#b = range(0, 56)
			b = [random.randint(0,127) for p in range(0,PTT_PACKAGE_SIZE)]
			self.load(b)
			rtc = RTC()
			self.timeTag = rtc.toArray()

	'''
		Loads package fields from an array
		of bytes. The length of the array must be of 
		PTT_PACKAGE_SIZE or less
	'''
	def load(self, byteArray):
		if (len(byteArray) < PTT_PACKAGE_SIZE):
			return -1
		
		# little endian
		self.pckgType = byteArray[0]
		self.decoderNumber = byteArray[1];

		self.ampRms = byteArray[2] & 0x00FF
		self.ampRms |= ((byteArray[3]<<8)&0xFF00)

		self.freqMeasure = 0
		# for i in range(4, 8):
		for i in range(7, 3, -1):
			self.freqMeasure |= ((byteArray[i] & 0x000000FF)<<((i-4)*8))

		# for i in range(8, 12):
		for i in range(11, 7, -1):
			self.pttIdNumber |= ((byteArray[i] & 0x000000FF)<<((i-8)*8))

		
		self.msgLength = byteArray[12];
		self.timeTag  = list(byteArray[PTT_TIME_TAG_START:(PTT_TIME_TAG_START+PTT_TIME_TAG_LENGTH)])
		self.sensorData = list(byteArray[PTT_SENSOR_DATA_START:(PTT_SENSOR_DATA_START+PTT_SENSOR_DATA_LENGTH)])

		self.crc = byteArray[PTT_PACKAGE_SIZE-2] & 0x00FF
		self.crc |= ((byteArray[PTT_PACKAGE_SIZE-1] << 8) & 0xFF00)

		self.raw_data = byteArray
		self.localCRC = calcCRC(self.sensorData) # doesn't include last 2 crc bytes

	def timeStamp(self):
		rtc = RTC()
		rtc.load(self.timeTag)
		return rtc.timeStamp()

####################################################################
class ADCPackage(Package):

	Fs = ADC_SAMPLE_FREQ;
	Ts = (1.0/ADC_SAMPLE_FREQ)*1000;
	limit = ((ADC_PACKAGE_SAMPLES / ADC_WINDOW_SIZE)*10) # in ms
	timeArray = 0
	adcSamples=[]
	pckgType = 0;

	def __init__(self, dummy=False):
		
		self.typeStr = Package.PCKG_TYPES[2] # self.typeStr='HK'
		self.adcSamples = [0]*ADC_PACKAGE_SAMPLES
		self.timeArray = np.arange(0,self.limit,self.Ts) # time vector

	def load(self, byteArray):
		if (len(byteArray) < ADC_PACKAGE_SIZE):
			return False

		self.pckgType = byteArray[0]
		cnt = 0
		tmp = 0
		for i in range(4, ADC_PACKAGE_SIZE, 4):
			tmp = tmp | ((byteArray[i+3] & 0x000000FF)<<24);
			tmp = tmp | ((byteArray[i+2] & 0x000000FF)<<16);
			tmp = tmp | ((byteArray[i+1] & 0x000000FF)<<8);
			tmp = tmp | ((byteArray[i] & 0x000000FF));
			self.adcSamples[cnt] = tmp
			tmp = 0;
			cnt +=1
		self.raw_data = byteArray
		return True

	def loadRandom(self):
		for i in range(0, ADC_PACKAGE_SAMPLES):
			self.adcSamples[i] = (random.randint(0,65535)&0x0000FFFF)<<16
			self.adcSamples[i] = self.adcSamples[i] | (random.randint(0,65535)&0x0000FFFF)

	def loadSinus(self):

		w1 = (2*np.pi*5000)#/ADC_SAMPLE_FREQ
		w2 = (2*np.pi*9000)#/ADC_SAMPLE_FREQ
		re = 0
		im = 0
		theta0 = 120*180/np.pi;
		for k in range(0, ADC_PACKAGE_SAMPLES):
			#t = np.exp(1j*theta0 + w1*self.timeArray[k])
			t = (np.sin(w1*self.timeArray[k]) * np.sin(w2*self.timeArray[k]))/2
			#t = (np.sin(w1*self.timeArray[k]))
			
			re = np.real(t)
			im = np.imag(t)
			
			re = int((re*32767))
			im = int((im*32767))

			# re = ctypes.c_ushort(re).value
			# im = ctypes.c_ushort(im).value

			self.adcSamples[k] = (re&0x0000FFFF)<<16
			self.adcSamples[k] = self.adcSamples[k] | (im&0x0000FFFF)

	def getComplexSignal(self):
		re = 0
		im = 0
		signal = [0]*len(self.adcSamples)
		t = np.arange(0,self.limit,self.Ts) # time vector
		for k in range(0, len(self.adcSamples)):
			re = (self.adcSamples[k] >> 16) & 0x0000FFFF;
			im = (self.adcSamples[k]) & 0x0000FFFF;
			
			re = ctypes.c_short(re).value
			im = ctypes.c_short(im).value

			#re = (re/32767.0)
			#im = (im/32767.0)

			signal[k] = complex(re, im)
			#signal[k] = (re + 1j*im)
		signal = np.array(signal)
		return signal

	def timeStamp(self):
		return None



####################################################################
if __name__=='__main__':
	
	print("Package Test")
	c = PTTPackage()
	b= range(0,PTT_PACKAGE_SIZE)

	c.load(b);

	print ("----------------------------------------------------")
	print (c.toArray())
	print ("----------------------------------------------------")
	print (c.toString())
	print ("----------------------------------------------------")

	print("Command Test")
	c= Command()
	c.setParam([32,33,34,35,36])
	c.setId(5)

	print ("----------------------------------------------------")
	print (c.toArray())
	print ("----------------------------------------------------")
	print (c.toString())
	print ("----------------------------------------------------")
