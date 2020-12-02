"""
    i2cnetcomm.py


	This module implements the Ethernet-I2C bridge client to run on
	the programmer PC. It is a temporary sollution while we don't 
	get a proper ftdi bridge
   
    Author: Anderson Amorim
    Date: 03/03/2017
"""

from __future__ import print_function
import socket
import sys
import time
from .connection import Connection

'''
	Server

	The server is intended to run on Rpi as a
	Ethernet-I2C bridge. It receives read/write
	requests over ethernet, forward then through
	I2C iface and (writes) and back to ethernet

	Package Format:
	
	The default package format must be 1024 bytes long
	It must be structure as follows:

	Write:

	Client --> Server
	[ 02 L0 L1 W0 W1 W2 ... W1020 ]
	02 			- Indicates it is a write operation
	L0L1 		- Two bytes indicating the size of the write (little endian)
	W0-W1020 	- Data to be written on I2C iface

	Obs: a write on I2C do not need to use the entire
	1020 W bytes. The L0L1 parameter spicifies the write length


	Read:

	Client --> Server
	[ 03 L0 L1 ... ]
	03 			- Indicates it is a read operation
	L0L1 		- Two bytes indicating the size of the be read from i2c (little endian)
	
	Server-->Client
	[00 01 02 ... ]
	The server returns only the amount of data requested

'''
# GLOBAL DEFINITIONS
REMOTE_PORT=12345

class NetConnection(Connection):


	I2C_SLAVE_DEVICE=0x0703
	I2C_SLAVE_ADDR=0
	sckt=0
	host='192.168.0.109' # remote hostname
	port = 0
	openned = False

	def __init__(self, remote_host='127.0.0.1'):
		Connection.__init__(self)
		self.I2C_SLAVE_ADDR = 0x10
		self.port = REMOTE_PORT
		self.host = remote_host

	def setSlaveAddress(self, addr):
		self.I2C_SLAVE_ADDR = addr
	
	def getSlaveAddress(self):
		return self.I2C_SLAVE_ADDR

	def open(self):
		self.sckt = socket.socket()         # Create a socket object
		self.sckt.connect((self.host, self.port))
		self.openned = True

	def write(self, string):
		s0 = len(string) & 0x00FF
		s1 = (len(string)>>8) & 0x00FF
		pckt = '' +  chr(0x02) + chr(s0) + chr(s1) + string
		self.sckt.send(pckt)

		# self.sckt.close()

	def read(self, nbytes):
		
		s0 = nbytes & 0x00FF
		s1 = (nbytes>>8) & 0x00FF
		pckt = '' +  chr(0x03) + chr(s0) + chr(s1)
		self.sckt.send(pckt)		
		
		# self.sckt.close()
		return self.sckt.recv(nbytes)


	def close(self):
		self.sckt.close()
		self.openned = False

