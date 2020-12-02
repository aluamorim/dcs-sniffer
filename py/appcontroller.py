"""
    appcontroller.py

   
    Author: Anderson Amorim
    Date: 24/02/2017
"""
import sys, traceback
import time
import pickle # to save objects
import subprocess
if (sys.version_info.major>=3):
    import _thread as thread
else:
    import thread
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTime, QDate, QObject
from collections import deque
from modules.entity import *
from modules.entity.controller import *
from modules.connection.i2cnetcomm import NetConnection
from modules.connection.arduinocomm import ArduinoConnection
from modules.control.viewcontroller import *
from modules.control.measurevc import *
from modules.control.packagevc import *
from modules.control.rohdecontroller import *
from modules.definitions import *
from modules.service.consoleservice import *
from modules.service.packageservice import *


'''
ApplicationController

This class implements all services required for the controls
on the SBCDAControllerApp class (view layer) to work properly.
The applicationcontroller object handles action triggers binded
in view layer. It does not handle specific UI details like enabling
and disabling controls. This class is a middle way layer between
the UI view layer and the PackageReading services 
'''
class AppController(QObject):

    connected=False
    viewController=0
    chartViewController=0
    packageReaderThread =0
    serialMonitorThread=0
    packageFilterList = []
    decoderController = None
    rohdeController = None
    parentApp=0
    pyqtErrorSignal = QtCore.pyqtSignal()
    pyqtADCMeasureSignal= QtCore.pyqtSignal()
    pyqtSerialConsoleSignal = QtCore.pyqtSignal()


    # Use the 'connected' parameter when running the program
    # with a valid connection to the device board. For example,
    # when running on Raspberry Pi
    def __init__(self, app=None):
        QObject.__init__(self)
        self.parentApp = app
        self.decoderController = DeviceController(None)
        self.rohdeController = RohdeController();

        self.viewController = PackageViewController(self.parentApp.mainTableWidget, 
            self.parentApp.treeWidget, self.parentApp.rawDataTable)

        self.chartViewController = MeasuresViewController(self.parentApp.chartCanvasWidget_0, 
            self.parentApp.chartCanvasWidget_1, 
            self.parentApp)
        self.packageReaderThread = PackageReaderService(self.viewController, 
            self.decoderController)
        self.serialMonitorThread = ConsoleService()

        self.packageFilterList = deque()
        self.packageFilterList.append(Package.PCKG_TYPE_PTT)
        self.packageFilterList.append(Package.PCKG_TYPE_HK)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Independent Threads Control   
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def pausePackageReader(self):
        self.packageReaderThread.pauseService()

    def pauseSerialMonitor(self):
        self.serialMonitorThread.pauseService()

    def pauseAllThreads(self):
        self.packageReaderThread.pauseService()
        self.serialMonitorThread.pauseService()

    def resumePackageReader(self):
        self.packageReaderThread.resumeService()

    def resumeSerialMonitor(self):
        self.serialMonitorThread.resumeService()

    def resumeAllThreads(self):
        self.packageReaderThread.resumeService()
        self.serialMonitorThread.resumeService()

    def stopPackageReader(self):
        self.packageReaderThread.stopService()

    def stopSerialMonitor(self):
        self.serialMonitorThread.stopService()

    def stopAllThreads(self):
        self.packageReaderThread.resumeService();
        self.packageReaderThread.stopService()
        self.serialMonitorThread.resumeService()
        self.serialMonitorThread.stopService()

    def isPackageReaderRunning(self):
        return self.packageReaderThread.isRunning()

    def isSerialMonitorRunning(self):
        return self.serialMonitorThread.isRunning()

    def isPackageReaderPaused(self):
        return self.packageReaderThread.isPaused()

    def isSerialMonitorPaused(self):
        return self.serialMonitorThread.isPaused()

    def isPackageListEmpty(self):
        return self.packageReaderThread.getPackageListLength()==0

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Device Controller
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def setDeviceControllerConnection(self, conn):
        self.decoderController.setConnection(conn)

    def setNewServerAddress(self,server):
        if (type(self.decoderController.connection) is NetComm):
            self.decoderController.connection.host = server

    def getNewServerAddress(self):
        if (type(self.decoderController.connection) is NetComm):
            return self.decoderController.connection.host
        return '127.0.0.1'

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Application Controller
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def resetAppController(self):

        for i in reversed(range(self.parentApp.mainTableWidget.rowCount())):
            self.parentApp.mainTableWidget.removeRow(i)
        self.parentApp.mainTableWidget.setRowCount(0)
        self.parentApp.rawDataTable.setRowCount(0)
        self.packageReaderThread.resetReader()

    def filterList(self, types):
        
        i = 0
        length = self.packageReaderThread.getPackageListLength()
        while (i < length):
            pckt = self.packageReaderThread.getPackageByIndex(i)
            if (pckt!=None and pckt.typeStr not in types):
                self.packageReaderThread.removePackage(pckt)
                i = -1
            length = self.packageReaderThread.getPackageListLength()
            i+=1
    
    def actionUpdateSerialConsole(self):

        str = self.serialMonitorThread.readNewString()
        self.parentApp.consoleTextEdit.insertPlainText(str)
        self.serialMonitorThread.clearNewString()


    def actionUpdateADCMeasures(self):
        hkList = self.packageReaderThread.getHKPackageList()
        self.chartViewController.updateChart(hkList, self.packageReaderThread.HK_PACKAGE_LIST_SIZE)

    def actionSavePackageList(self, name=None):

        if (name==None):
            return
        extension =  '.sbcda_pckglist'
        if (extension not in name):
            name += extension
        
        file = open(name, 'wb')
        pickle.dump( self.packageReaderThread.getPackageList(), file)

    def actionOpenPackageList(self, name=None):

        if (name==None):
            return
        file = open(name, 'rb')

        self.packageReaderThread.setPackageList(pickle.load(file))
        self.viewController.loadTableFromList(self.packageReaderThread.getPackageList())

        
    def actionConnect(self):
        self.decoderController.startController()
        self.connected = True
    
    def actionDisconnect(self):
        self.stopPackageReader()
        self.decoderController.stopController()
        self.connected = False
    
    def actionEchoTest(self):
        try:
            self.decoderController.sendEcho()
            return True
        except:
            return False

    def actionControlRTC(self, cmdId):
        try:
            self.decoderController.simpleRun(cmdId)
            return True
        except:
            return False
        # self.decoderController.pauseRTC()
        # return True
    
    def actionSetRTC(self):

        date = self.parentApp.rtcDateEdit.date()
        vec = range(0,8)
        vec[0] = date.year()-1900
        vec[1] = date.month()
        vec[2] = date.day()

        time = self.parentApp.rtcTimeEdit.time()
        vec[3] = time.hour()
        vec[4] = time.minute()
        vec[5] = time.second()
        vec[6] = 1
        vec[7] = 1
        rtc = RTC()
        rtc.load(vec)
        ret = True
        if (self.connected==True):
            try:
                self.decoderController.setRTC(rtc)
            except:
                ret =  False
        
        return ret

    def actionFilterSelect(self, filterList):
        self.filterList(filterList)
        self.viewController.loadTableFromList(self.packageReaderThread.getPackageList())

    def actionUpdateHK(self):
        cfg_bytes = [0,0,0,0,0,0,0, 0] # config word is 8 bytes long
        cfg_bytes[2] = 0 # refresh time
        cfg_word = 0;
        if (self.parentApp.hkRTCCheck.isChecked()):
            cfg_word |= HK_CFG_RTC
        
        if (self.parentApp.hkCurrentSensorCheck.isChecked()):
            cfg_word |= HK_CFG_CURRENT_SENSORS
        
        if (self.parentApp.hkADCRmsCheck.isChecked()):
            cfg_word |= HK_CFG_ADC_RMS_SAMPLE
        
        if (self.parentApp.hkPLLSyncBitCheck.isChecked()):
            cfg_word |= HK_CFG_PLL_SYNC_BIT
        
        if (self.parentApp.hkOverCurrentErrorCheck.isChecked()):
            cfg_word |= HK_CFG_OVER_CURRENT

        cfg_bytes[0] = (cfg_word>>8)&0x00FF
        cfg_bytes[1] = (cfg_word)&0x00FF
        try:
            # wait for ptt task to stop
            self.decoderController.updateHKConfig(cfg_bytes)
            return True
        except:
            return False

    # gets selected package detail from the given selected row
    def actionRowSelected(self, rowNumber=-1):
        
        self.parentApp.treeWidget.clear() # clear previous msg details
        if (rowNumber == -1):
            return
        pckt = self.packageReaderThread.getPackageList()[rowNumber]
        type = self.parentApp.mainTableWidget.item(rowNumber, 1) ## type columm
        if (type.text()=='PTT'):
            self.viewController.fillPTTDetailForm(pckt)
        elif(type.text()=='HK'):
            self.viewController.fillHKDetailForm(pckt);
        else:
            return
        
        self.viewController.fillRawPackageForm(pckt)

    def actionStartI2CServer(self):
        if (type(self.decoderController.connection) is NetComm):
            cmd = ["ssh", "pi@" + self.getNewServerAddress(), REMOTE_SERVER_SCRIPT_PATH]
            # cmd = ["ssh", "-o TCPKeepAlive=yes", "pi@" + self.getNewServerAddress(), REMOTE_SERVER_SCRIPT_PATH]
            # print (cmd[0] + ' ' + cmd[1] + ' ' + cmd[2])
            try:
                p = subprocess.Popen(cmd)
                time.sleep(0.5)
                p.kill()
                return True
            except Exception as e:
                print(" Unable to start i2c sever! Error: " + str(e))
                traceback.print_exc(file=sys.stdout)
                return False
        else:
            return True

    def actionStopI2CServer(self):

        if (type(self.decoderController.connection) is NetComm):
            cmd = ["ssh" ,  "pi@" + self.getNewServerAddress(), "killall python"]
            try:
                p = subprocess.Popen(cmd)
                time.sleep(0.5)
                p.kill()
                return True
            except Exception as e:
                print(" Unable to stop i2c sever! Error: " + str(e))
                traceback.print_exc(file=sys.stdout)
                return False
        else:
            return True

    def actionPackageReader(self):
        try:
            self.parentApp.statusBar().showMessage("Reading Available Packages... ")
            self.packageReaderThread.setHKReadDelay(int(self.parentApp.hkRequestSpinBox.value()))
            self.packageReaderThread.setPackageTypes(self.packageFilterList)
            if (not self.packageReaderThread.isRunning()): # threads can only by started once
                self.packageReaderThread = PackageReaderService(self.viewController, self.decoderController, self.packageFilterList)
                self.packageReaderThread.setPyqtErrorSignal(self.pyqtErrorSignal) # to hanble threads fatal errors
                self.packageReaderThread.setPyqtADCMeasureSignal(self.pyqtADCMeasureSignal) # to hanble adc measures updates
                try:
                    self.packageReaderThread.start()
                except (KeyboardInterrupt, SystemExit):
                    self.stopPackageReader()
                    sys.exit()
            return True
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print(str(e))
            return False

    def getPackageFilterList(self):
        return self.packageFilterList

    def getPyqtSignal(self):
        return self.pyqtErrorSignal
