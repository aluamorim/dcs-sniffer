from __future__ import print_function
import socket
import sys
import time
from comm import *
from entity import *
from controller import *
from i2ccomm import *

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

class Server(object):
	
	i2c=0
	sckt=0
	host=0
	port=4545

	def __init__(self):
		self.i2c = I2CConnection)

		self.sckt = socket.socket()         # Create a socket object
		self.host = socket.gethostname() # Get local machine name
		self.port = REMOTE_PORT                	# Reserve a port for your service.
		self.sckt.bind(('', self.port))        # Bind to the port

	def startController(self):
		self.i2c.open()

	def server(self):

		self.startController()
		self.sckt.listen(5)                 # Now wait for client connection.

		while(True):
			connection, addr = self.sckt.accept()     # Establish connection with client.
			#try:
			while(True):

				print('Request from  ' + str(addr) + ' \r', end='')

				bytes = connection.recv(1024) ## read request

				if (bytes == None or len(bytes)==0):
					break

				# vl = [ord(t) for t in bytes]
				if (ord(bytes[0])==2): # write command
					size = ord(bytes[2])
					size = ((size<<8) | ord(bytes[1])) & 0x0000FFFF
					if (size < 1020):
						data = bytes[3:(3+size)]
						self.i2c.write(data)
				elif(ord(bytes[0])==3): # read command
					size = ord(bytes[2])
					size = ((size<<8) | ord(bytes[1])) & 0x0000FFFF
					data = self.i2c.read(size)
					connection.send(data)

		   	# except:
		   	# 	print ("> Connection Error ")
			print("")
			print ("Connection dropped down by the client. Wating for new requests... ")
			connection.close()# Close the connection

	def sendI2C(self, bytes):
		pass

	def readI2C(self, len):
		pass

class Client(object):

	def client(self):
		s = socket.socket()         # Create a socket object
		host = socket.gethostname() # Get local machine name
		port = REMOTE_PORT              # Reserve a port for your service.

		s.connect((host, port))
		print (s.recv(1024))
		s.close

# main should start the server class
if __name__=='__main__':


	# if (len(sys.argv) > 1):
	# 	print ("Client")
	# 	c = NetConnection)
		
	# 	controller = Controller(c)
	# 	controller.startController()
	# 	controller.sendEcho()
	# 	time.sleep(0.5)
	# 	print ("reading ptt package: ")
	# 	pckt = controller.getPTTPackage()
	# 	print(pckt)

	# 	print (">>>>>>>>>>> ")

	# else:
	print ("Starting I2C Bridge Server...")
	s = Server()
	s.startController()
	print ("Waiting for connections... ")
	s.server()