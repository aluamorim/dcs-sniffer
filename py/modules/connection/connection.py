"""
	connection.py

	This Module defines the basic commmunication interface
	between the test program and the Decoder Module. It is
	interface independent, defining only the basic top
	level API.

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

class Connection (object):
	''' Template class '''

	def __init__(self):
		pass


	def open(self):
		pass

	def write(self, bytes):
		pass

	def read(self, nbytes):
		pass

	def close(self):
		pass
