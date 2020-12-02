"""
	i2c.py

	This module implements the Comm API using I2C 
	interface.

	Obs: The write and read methods must receive and
	return (respectively) sstrings of ascii values,
	not integers. Internal convertion may be necessary
	according to the implementation. This was necessary
	because built-in library functions from fcntl work
	this way. Therefor, to avoid losing time with type
	convertion inside the commmunication functions we must
	impose this restriction

	Author: Anderson Amorim
	Date: 22/02/2017
"""
import sys
import io
import fcntl
from .connection import Connection
from time import sleep


class I2CComm (Connection):
	I2C_SLAVE_DEVICE=0x0703
	I2C_SLAVE_ADDR=0
	openned=False
	fw=0
	fr=0

	def __init__(self):
		Connection.__init__(self)
		self.I2C_SLAVE_ADDR = 0x10

	def setSlaveAddress(self, addr):
		self.I2C_SLAVE_ADDR = addr
		if (self.openned==True):
			fcntl.ioctl(self.fw, self.I2C_SLAVE_DEVICE, self.I2C_SLAVE_ADDR)
			fcntl.ioctl(self.fr, self.I2C_SLAVE_DEVICE, self.I2C_SLAVE_ADDR)
	
	def getSlaveAddress(self):
		return self.I2C_SLAVE_ADDR

	def open(self):
		self.fw = io.open("/dev/i2c-1", "wb", buffering=0)
		self.fr = io.open("/dev/i2c-1", "rb", buffering=0)
		fcntl.ioctl(self.fw, self.I2C_SLAVE_DEVICE, self.I2C_SLAVE_ADDR)
		fcntl.ioctl(self.fr, self.I2C_SLAVE_DEVICE, self.I2C_SLAVE_ADDR)
		self.openned = True

	def write(self, string):
		self.fw.write(string)

	def read(self, nbytes):
		return self.fr.read(nbytes)

	def close(self):
		self.fw.close()
		self.fr.close()
		self.openned = False

''' test '''
if __name__ == '__main__':

	i2c = I2Connection)
	i2c.open()
	print("---------------------------------------------------------")
	i2c.setSlaveAddress(0x10)
	bytes = [0xFA, 0x01, 0x02, 0x03, 0x04, 0x0A]
	string = ''.join((map(chr, bytes)))
	i2c.write(string)
	sleep(0.2)
	string = i2c.read(56)
	print("---------------------------------------------------------")
	bytes= [ord(c) for c in string]
	print (bytes)
	print("---------------------------------------------------------")
	i2c.close()