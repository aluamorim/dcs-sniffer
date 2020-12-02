"""
	controller.py

	This Module defines the basic controll interface
	for the Decoder HW. Everything that is possible
	to do from the board computer side is offered
	by the methods of the controller module

	Author: Anderson Amorim
	Date: 23/02/2017
"""
import sys
import os
import time


from ..definitions import *
from ..connection import *
from ..entity.entity import *


class DeviceController(object):

	connection=None
	connected = False
	default_timeout = 5

	def __init__(self, conn=None):
		self.connection = conn
		self.connected = False

	def setConnection(self, conn):
		self.connection = conn

	def startController(self):
		if (self.connection != None):
			self.connection.open()
			self.connected = True

	
	def stopController(self):
		if (self.connection != None and self.connected):
			self.connection.close()
			self.connected = False

	''' Writes a single cmd through 
		the connection interface
		cmd object must be of type Command
	'''
	def wCmd(self, cmd):
		self.connection.write(cmd.toString())
	
	''' Reads a single cmd through 
		the connection interface
	'''
	def rCmd(self):
		str = self.connection.read(DEFAULT_CMD_SIZE)
		self.connection.flush()
		bytes = [ord(c) for c in str]
		cmd = Command()
		cmd.load(bytes)
		return cmd

	def simpleRun(self, cmdId):
		cmd = Command()
		cmd.setId(cmdId)
		self.wCmd(cmd)

	def setCMDMode(self):
		cmd = Command()
		cmd.setId(CMD_SET_CONFIG_MODE)
		self.wCmd(cmd)

		resp = self.rCmd()
		# blocks until the ack is received
		timeout = self.default_timeout
		while (resp.id != ACK_PCKG_ID or resp.resp_id != CMD_SET_CONFIG_MODE):
			resp = self.rCmd()
			time.sleep(0.1)
			# print("> SET CMD: ")
			# print (resp.toArray())
			timeout = timeout -1
			if(timeout == 0):
				return False
		return True
				
	
	def setADCMode(self):
		cmd = Command()
		cmd.setId(CMD_SET_ADC_MODE)
		self.wCmd(cmd)

	def setPTTMode(self):
		cmd = Command()
		cmd.setId(CMD_SET_PTT_MODE)
		self.wCmd(cmd)


	def setHKMode(self):
		cmd = Command()
		cmd.setId(CMD_SET_HK_MODE)
		self.wCmd(cmd)

	
	def setRTC(self, rtc):
		self.setCMDMode()
		cmd = Command()
		cmd.setId(RTC_SET)
		cmd.setParam(rtc.toArray())
		self.wCmd(cmd)

	def pauseRTC(self):
		self.setCMDMode()
		cmd = Command()
		cmd.setId(RTC_PAUSE)
		self.wCmd(cmd)

	def resumeRTC(self):
		self.setCMDMode()
		cmd = Command()
		cmd.setId(RTC_RESUME)
		self.wCmd(cmd)

	def resetRTC(self):
		self.setCMDMode()
		cmd = Command()
		cmd.setId(RTC_RESET)
		self.wCmd(cmd)

	def updateHKConfig(self, cfg):
		self.setCMDMode()
		cmd = Command()
		cmd.setId(HK_CONFIG)
		cmd.setParam(cfg)
		self.wCmd(cmd)

	def popPTT(self):
		cmd = Command()
		cmd.setId(PTT_POP)
		self.wCmd(cmd)

	def pausePTT(self):
		cmd = Command()
		cmd.setId(PTT_PAUSE)
		self.wCmd(cmd)

	def resumePTT(self):
		cmd = Command()
		cmd.setId(PTT_RESUME)
		self.wCmd(cmd)

	def adcLoad(self):
		cmd = Command()
		cmd.setId(ADC_LOAD)
		self.wCmd(cmd)
	
	def adcState(self):
		cmd = Command()
		cmd.setId(ADC_STATE)
		self.wCmd(cmd)
		resp = self.rCmd()

		timeout = self.default_timeout
		while(resp.id != ACK_PCKG_ID or resp.resp_id!=ADC_STATE):
			#self.wCmd(cmd)
			time.sleep(0.05)
			resp = self.rCmd()
			timeout = timeout -1
			if(timeout == 0):
				return 0

		n = resp.param[3] # last byte
		return n


	def adcReset(self):
		cmd = Command()
		cmd.setId(ADC_RESET)
		self.wCmd(cmd)


	def getNumOfAvailablePackages(self):
		self.setCMDMode()
		cmd = Command()
		cmd.setId(PTT_AVAILABLE) # request
		self.wCmd(cmd)
		resp = self.rCmd()

		timeout = self.default_timeout
		while(resp.id != ACK_PCKG_ID or resp.resp_id!=PTT_AVAILABLE):
			#self.wCmd(cmd)
			time.sleep(0.05)
			resp = self.rCmd()
			timeout = timeout -1
			if(timeout == 0):
				return 0

		n = resp.param[3]
		return n

	def isPTTServicePaused(self):
		cmd = Command()
		cmd.setId(PTT_ISPAUSED) # request
		self.wCmd(cmd)
		time.sleep(0.5)
		resp = self.rCmd()
		n = 0
		if(resp.id == ACK_PCKG_ID and resp.resp_id==PTT_ISPAUSED):
			n = resp.param[3]
		return n
	
	def getPTTPackage(self):
		str = self.connection.read(PTT_PACKAGE_SIZE)
		rcv_str = [ord(c) for c in str]
		if (len(rcv_str) >= PTT_PACKAGE_SIZE):
			pckt = PTTPackage()
			pckt.load(rcv_str)
			
			if (rcv_str[0]==PTT_PCKG_ID):
				return pckt
			else:
				print ("> Wrong package type error (PTT): " )
				print(pckt.toArray())
				return None
		else:
			print ("> No package received (PTT): " )
			return None

	def getHKPackage(self):
		rcv_str = self.connection.read(HK_PACKAGE_SIZE)
		pckt = None
		if (len(rcv_str) >= HK_PACKAGE_SIZE):
			bytes = [ord(c) for c in rcv_str]
			pckt = HKPackage()
			pckt.load(bytes)
			if (pckt.pckgType != HK_PCKG_ID):
				print ("> Wrong package type error (HK): " )
				print(pckt.toArray())
				return None # read an incorrect package
		else:
			print ("> No package received (HK): " )
		return pckt
	
	def getADCPackage(self):
		rcv_str = self.connection.read(ADC_PACKAGE_SIZE)
		pckt = None
		if (len(rcv_str) >= ADC_PACKAGE_SIZE):
			rcv_str = [ord(c) for c in rcv_str]
			# print(rcv_str)
			pckt = ADCPackage()
			if (pckt.load(rcv_str)==False):
				print ("> Could not load ADC Package " )
				return None
			if (pckt.pckgType != ADC_PCKG_ID):
				print ("> Wrong package type error (ADC): " )
				print(pckt.toArray())
				return None # read an incorrect package
		return pckt
		
	def sendEcho(self):
		self.setCMDMode()
		cmd = Command()
		cmd.setId(ECHO)
		self.wCmd(cmd)
		self.setPTTMode()


if __name__=='__main__':

	c = Controller(SerialConnection("COM6", '56700'))
	c.startController()

	c.sendEcho()