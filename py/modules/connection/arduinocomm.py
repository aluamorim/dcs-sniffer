
"""
    serialcomm.py


	This module implements a Serial UART connection
	interface
   
    Author: Anderson Amorim
    Date: 03/03/2017
"""

from __future__ import print_function
import sys
import time
import serial
from .connection import Connection


class ArduinoConnection(Connection):

	COM_PORT=None
	BAUDRATE = '115200'
	device=None

	def __init__(self, port=None, baudrate='115200'):
		Connection.__init__(self)
		self.COM_PORT = port
		self.BAUDRATE = baudrate

	def open(self):
		if (self.COM_PORT != None):
			self.device = serial.Serial(
			port=self.COM_PORT,
			baudrate=self.BAUDRATE,
			parity=serial.PARITY_NONE,
			timeout=2
			)
		# self.device.open()

	def read(self, nbytes):
		if (self.device != None):
			s0 = nbytes & 0x00FF
			s1 = (nbytes>>8) & 0x00FF
			pckt = '' +  chr(0x03) + chr(s1) + chr(s0)
			self.device.write(pckt)
			return self.device.read(nbytes)
		else:
			print ("ARDUINO READ FAIL")
			return ''

	def write(self, string):
		if (self.device != None):
			s0 = len(string) & 0x00FF
			s1 = (len(string)>>8) & 0x00FF
			pckt = '' +  chr(0x02) + chr(s1) + chr(s0) + string
			self.device.write(pckt)
		else:
			print ("ARDUINO WRITE FAIL")

	def flush(self):
		if (self.device != None):
			self.device.flush()
			
		
	def close(self):
		if (self.device != None):
			self.device.close()

	def setPort(self, port):
		self.COM_PORT = port


if __name__ == '__main__':

	vec = [0x00, 0x04, 0xFA, 0xFB, 0xFC, 0xFD ]
	st = ''.join((map(chr, vec)))
	print ("Instanciating")
	comm  = ArduinoConnection("COM6", '115200')

	print ("Open connection")
	comm.open()
	# print ('Write Echo')
	# comm.write(st)
	print ("Read 54 bytes")
	t = comm.read(54)
	print ("Read: ", end='')
	print(t)
	print ("Done")



