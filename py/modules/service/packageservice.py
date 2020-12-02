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


class HousekeepingTimer(Service):
    
    delay=0
    timeout=False

    pause = False
    running = True

    def __init__(self):
        Service.__init__(self)

    def run(self):
        while (self.running):
            self.timeout = False
            time.sleep(self.delay)
            self.timeout = True
            while(self.pause or self.timeout):
                time.sleep(0.01)

    def setDelay(self, d):
        self.delay = d

    def pauseService(self):
        self.pause = True

    def resumeService(self):
        self.pause = False

    def stopService(self):
        self.running = False

    def isRunning(self):
        return self.running

    def isPaused(self):
        return self.pause

    def clearTimeout(self):
        self.timeout = False

    def isTimeout(self):
        return self.timeout

''''
PackageReader

This class implements the package reader thread. Its main job
is to read data packages from the DeviceController
and maintain a list of read packages.
'''
class PackageReaderService(Service):

    # data and operation
    keepReading=False
    readerPaused=False

    hkTimer = None

    packageList=0
    hkPackageList=0 # necessary to plot ADC rms values history
    packageTypes=0
    globalPackageCnt=0

    #configuration
    defaultDelay=0.01
    defaultHKDelay = 1
    MAX_PACKAGE_LIST_SIZE = 10
    HK_PACKAGE_LIST_SIZE = 10

    # dependencies
    deviceController=None
    packageViewController=None
    pyqtErrorSignal = None
    pyqtADCMeasureSignal=None

    def __init__(self, viewController, deviceController, packageTypes=[Package.PCKG_TYPE_PTT, Package.PCKG_TYPE_HK]):
        Service.__init__(self)
        self.deviceController = deviceController
        self.packageList = deque()
        self.hkPackageList = deque()
        self.globalPackageCnt=0
        self.packageViewController = viewController
        self.packageTypes = packageTypes
        self.hkTimer = HousekeepingTimer()

    def handleThreadFatalError(self, e):
        traceback.print_exc(file=sys.stdout)
        print(str(e))
        if (self.pyqtErrorSignal != None):
            self.pyqtErrorSignal.emit()


    def run(self):
        self.keepReading = True
        self.readerPaused = False
        try:
            self.packageReaderThread()
        except Exception as e:
            self.handleThreadFatalError(e)

        self.keepReading = False
        self.readerPaused = True
    '''
    This method reads PTT and HK packages from the device
    while readPackagesFlag is True. The mainTable from
    parent form is update at every new package
    '''
    def packageReaderThread(self):

        mult_factor= 30
        self.hkTimer.setDelay(self.defaultHKDelay)
        self.hkTimer.start()
        # cnt = 0;
        # print("")
        
        while (self.keepReading):
            # print ("\r Package reader Thread is (%d)"%cnt, end='')
            # cnt+=1
            if (self.readerPaused==False):
                time.sleep(self.defaultDelay)
                pckt=None
                if (self.hkTimer.isTimeout() and (Package.PCKG_TYPE_HK in self.packageTypes)):
                    self.hkTimer.clearTimeout()
                    self.deviceController.setHKMode()
                    time.sleep(0.1)
                    pckt = self.deviceController.getHKPackage()
                    self.deviceController.setPTTMode()
                elif (Package.PCKG_TYPE_PTT in self.packageTypes):
                    pckt = self.deviceController.getPTTPackage()
                    time.sleep(0.25)
                    self.deviceController.popPTT()
                    time.sleep(0.25)
    
                if (pckt == None):
                    self.deviceController.setPTTMode()
                    continue

                if (pckt.typeStr==Package.PCKG_TYPE_HK): # add to specific HK package list
                    if (len(self.hkPackageList) >= self.HK_PACKAGE_LIST_SIZE):
                        self.hkPackageList.popleft() # if list is full, remove oldest
                    self.hkPackageList.append(pckt)
                    if (self.pyqtADCMeasureSignal != None):
                        self.pyqtADCMeasureSignal.emit()

                if (len(self.packageList) > self.MAX_PACKAGE_LIST_SIZE):
                    # TODO update table removing the first line
                    self.packageList.popleft()
                    self.packageViewController.removeRow(0)

                self.packageList.append(pckt)
                self.globalPackageCnt +=1
                self.packageViewController.addRow(pckt, len(self.packageList), self.globalPackageCnt)
            # time.sleep(self.defaultDelay)


    # gets and sets
    def getHKPackageList(self):
        return self.hkPackageList
    
    def setHKPackageList(self, value):
        self.hkPackageList = value

    def getPackageByIndex(self, idx):
        if(idx < len(self.packageList)):
            return self.packageList[idx]
    
    def removePackage(self, pckt):
        if(pckt in self.packageList):
            self.packageList.remove(pckt)

    def getPackageList(self):
        return self.packageList
    
    def setPackageList(self, value):
        self.packageList = value

    def getPackageListLength(self):
        return len(self.packageList)

    def getGlobalPackageCnt(self):
        return self.globalPackageCnt

    def resetGlobalPackageCnt(self):
        self.globalPackageCnt = 0

    def getPackageTypes(self):
        return self.packageTypes
    
    def setPackageTypes(self, value):
        self.packageTypes = value

    def setHKReadDelay(self, value):
        self.defaultHKDelay = value
        self.hkTimer.setDelay(value)

    def pauseService(self):
        self.readerPaused = True
    
    def resumeService(self):
        self.readerPaused = False

    def stopService(self):
        self.keepReading=False
        self.hkTimer.clearTimeout()
        self.hkTimer.resumeService()
        self.hkTimer.stopService()

    def isRunning(self):
        return self.keepReading

    def isPaused(self):
        return self.readerPaused

    def resetReader(self):
        self.packageList.clear()
        self.hkPackageList.clear()

    def setPyqtErrorSignal(self, signal):
        self. pyqtErrorSignal = signal

    def setPyqtADCMeasureSignal(self, signal):
        self. pyqtADCMeasureSignal = signal
