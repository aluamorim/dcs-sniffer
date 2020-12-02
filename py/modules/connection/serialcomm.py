
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


class SerialConnection(Connection):

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
			timeout=0.1
			)
		# self.device.open()

	def read(self, nbytes):
		if (self.device != None):
			return self.device.read(nbytes)
		else:
			return ''

	def write(self, strn):
		if (self.device != None):
			self.device.write(strn)
		else:
			print ("FAIL")
			
		
	def close(self):
		if (self.device != None):
			self.device.close()

	def setPort(self, port):
		self.COM_PORT = port


if __name__ == '__main__':

	vec = [0x02, 0x00, 0x04, 0xFA, 0xFB, 0xFC, 0xFD ]
	st = ''.join((map(chr, vec)))
	print ("Instanciating")
	comm  = SerialConnection("COM6", '57600')

	print ("Open connection")
	comm.open()
	print ('Write Echo')
	comm.write(st)
	# print ("Read 10 bytes")
	# t = comm.read(10)
	# print ("Read: ", end='')
	# print(t)
	# print ("Done")



