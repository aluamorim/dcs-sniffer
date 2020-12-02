"""
    rohdecontroller.py
    Author: Anderson Amorim
    Date: 26/05/2017
"""
import sys
import platform
import time
import datetime
import re
import matplotlib.pyplot as plt
import serialenum
import visa
import numpy as np

class RohdeController (object):

	viRM = 0;
	rohde = 0;
	connected = False

	def __init__ (self):
		self.viRM = visa.ResourceManager();

	def connect(self, address=None):
		if (address==None):
			return

		# address must be a vali ip addr at this point
		cmd = "TCPIP::"+address;
		self.rohde = self.viRM.open_resource (cmd)
		self.connected = True

	def disconnect(self):
		self.setLocal()
		self.connected = False

	def setLocal(self):
		self.rohde.write("&GTL")

	def setFreq(self, freq="401.635"):
		self.rohde.write("FREQ " + freq + " MHz");

	def setLevel(self, lvl="-98 dBm"):
		self.rohde.write("POW " + lvl);

	def enableRFO(self):
		self.rohde.write("OUTP ON")

	def disableRFO(self):
		self.rohde.write("OUTP OFF")

	def enableARB(self):
		self.rohde.write("SOUR:BB:ARB:STATE ON")

	def disableARB(self):
		self.rohde.write("SOUR:BB:ARB:STATE OFF")

	def setBBWaveform(self, waveform_file_data):
		if (waveform_file_data != None and len(waveform_file_data)> 0):
			# self.rohde.write("MMEM:DEL \'/var/user/sbcda.wv\'")
			data =  bytearray(waveform_file_data)
			# self.rohde.write_binary_values('BB:ARB:WAV:DATA \'/var/user/sbcda.wv\',', data, datatype='B')
			self.rohde.write_binary_values('MMEM:DATA \'/var/user/sbcda.wv\',', data, datatype='B')
			self.rohde.write("BB:ARB:WAV:SEL \'/var/user/sbcda.wv\'")
	
	def loadBBWaveformFile(self, name):
		if (name == None):
			return
		try:
			f = open(name, 'rb')
			data = f.read()
			# print (data)
			f.close()
			return data
		except Exception as e:
			print("Error: " + str(e))
			traceback.print_exc(file=sys.stdout)
			return None

	def sendWaveformFile(self, name):
		data = self.loadBBWaveformFile(name)
		self.setBBWaveform(data)

	def setSingleShotClockConfig(self):
		self.rohde.write("SOUR:BB:ARB:TRIG:SEQ SING")

	def setPeriodicClockConfig(self):
		self.rohde.write("SOUR:BB:ARB:TRIG:SEQ AUTO")

	def triggerSignal(self):
		self.rohde.write("SOUR:BB:ARB:TRIG:EXECUTE")


if __name__ == '__main__':
	
	name = "C:/Users/Anderson/Desktop/t.wv"

	r = RohdeController()
	r.connect("192.168.0.199")
	print("> Start ")
	r.sendWaveformFile(name)
	print("> End ")

	r.setLocal()