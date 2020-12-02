
from __future__ import print_function
import sys, traceback
import time

if (sys.version_info.major>=3):
    import _thread as thread
else:
    import thread

import threading
from PyQt5 import QtCore, QtGui
from collections import deque
from modules.entity import *
from modules.entity.controller import *
from modules.connection.i2cnetcomm import *
from modules.connection.serialcomm import *
from modules.definitions import *
from modules.service.service import *


class ConsoleService(Service):

    deviceController=None
    running=False
    pause=False

    newString=None
    pyqtSerialConsoleSignal=None

    def __init__(self):
        Service.__init__(self)
        self.deviceController = SerialConnection()

    def run(self):
        self.running = True
        try:
            self.startSerialController()
            try:
                self.serialMonitorThread()
            except Exception as e:
                print("Error: " + str(e))
                traceback.print_exc(file=sys.stdout)
            self.stopSerialController()
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc(file=sys.stdout)
        self.running = False

    def serialMonitorThread(self):
        # cnt = 0;
        # print("")
        while(self.running==True):

            #self.consoleTextEdit.append("Hello")
            if (self.newString == None):
                self.newString = self.deviceController.read(10)
                self.newString = self.newString.replace('\n', '')
                if (self.pyqtSerialConsoleSignal != None):
                    self.pyqtSerialConsoleSignal.emit()
            

            # print ('\r Serial console Thread is on (%d)'%cnt, end='')
            # cnt+=1
            time.sleep(0.001) # fastest I could get
            while(self.pause):
                 time.sleep(0.001)

    def readNewString(self):
        return self.newString
    def clearNewString(self):
        self.newString = None
    
    def setSerialConsoleSignal(self, signal):
        self.pyqtSerialConsoleSignal = signal

    def startSerialController(self):
        self.deviceController.open()

    def stopSerialController(self):
        if (self.deviceController != None):
            self.deviceController.close()


    def updatePort(self, port):
        if (self.running):
            self.pauseService()
            try:
                self.stopSerialController()
                self.deviceController.setPort(port)
                self.startSerialController()
            except Exception as e:
                print(str(e))
                self.deviceController.device = None
                return
            self.resumeService()
    
    def isRunning(self):
        return self.running==True

    def stopService(self):
        self.running = False

    def pauseService(self):
        self.pause = True
        time.sleep(0.01)

    def resumeService(self):
        self.pause = False
        time.sleep(0.01)

    def isPaused(self):
        return self.pause