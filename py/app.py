#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    app.py

    The SBCDAControllerApp class extends the design.Ui_MainWindow and 
    QtGui.QMainWindow classes and is the application's start point.
    UI Control bindings are made in this class. Each action, or button
    triggers a correspondete 'run' method. These methods are responsible
    for correct UI manipulation (i.e. enabling and disabling controls, 
    showing message boxes, printing error messages etc.)
    All UI bindings and new actions must be performed in this class

    Author: Anderson Amorim
    Date: 21/02/2017
"""

import sys
import platform
import time
import datetime
import re
import matplotlib.pyplot as plt
import serialenum

if (sys.version_info.major>=3):
    import _thread as thread
else:
    import thread
import maindesign

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTime, QDate, QObject
#from PyQt5.QtGui import QInputDialog, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from appcontroller import *
from modules import definitions
from modules.dialog.adcdialog import *
from modules.dialog.tonegenerator import *

'''
necessary to set the right window icon for windows
'''
if (platform.system()!="Linux"):
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
''''''

class SBCDAControllerApp(QMainWindow, maindesign.Ui_MainWindow):
    
    appController=0
    pauseReading=False

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
       Class constructor
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def __init__(self, parent=None):
        super(SBCDAControllerApp, self).__init__(parent)
        
        self.setupUi(self)
        self.appController = AppController(self) # when device is connected
        
        self.lastUIAdjusts()
        self.controlBindings()

        self.runFilterSelect()
        self.statusBar().showMessage("Ready")

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Last UI adjustments
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def lastUIAdjusts(self):
        
        self.mainTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.mainTableWidget.setColumnWidth(0, 50)
        self.mainTableWidget.setColumnWidth(1, 50)
        self.mainTableWidget.setColumnWidth(2, 160)

        self.rawDataTable.setSelectionMode(QAbstractItemView.SingleSelection)

        self.consoleTextEdit.setTextColor(QtGui.QColor(255, 255, 255 )) # white font

        #adjust current time
        now = datetime.datetime.now()
        time = QTime(now.hour, now.minute, now.second, 0)
        date = QDate(now.year, now.month, now.day)
        self.rtcTimeEdit.setTime(time)
        self.rtcDateEdit.setDate(date)

        # self.controlToolBox.setEnabled(False)
        self.deviceConfigWidget.setEnabled(False)
        self.connectionConfigWidget.setEnabled(True)
        self.actionADCSampler.setEnabled(False)

        #enumerate available serial ports
        ports = serialenum.enumerate()
        cnt=0
        for p in ports:
            self.serialConsoleComboBox.addItem("")
            self.comPortComboBox.addItem("")
            self.serialConsoleComboBox.setItemText(cnt, str(p))
            self.comPortComboBox.setItemText(cnt, str(p))
            cnt +=1


    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Control bindings
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def controlBindings(self):
        self.actionToneGenerator.triggered.connect(self.runToneGenDialog)
        self.actionADCSampler.triggered.connect(self.runActionADCSampler)
        self.actionClear.triggered.connect(self.runActionClear)
        self.actionQuit.triggered.connect(self.runActionQuit)
        self.actionPlay.triggered.connect(self.runActionPlay)
        self.actionPause.triggered.connect(self.runActionPause)
        self.actionStop.triggered.connect(self.runActionStop)
        self.actionEchoTest.triggered.connect(self.runEchoTest)
        self.actionConnect.triggered.connect(self.runConnect)
        self.actionDisconnect.triggered.connect(self.runDisconnect)
        self.actionSave.triggered.connect(self.runSaveFile)
        self.actionOpen.triggered.connect(self.runOpenFile)


        self.loadWaveformButton.clicked.connect(self.runLoadWaveformButton)
        self.connectVectorGenButton.clicked.connect(self.runConnectVectorGenButton)
        self.setRTCButton.clicked.connect(self.runSetRTCButton)
        self.mainTableWidget.selectionModel().selectionChanged.connect(self.runRowSelection)
        self.clearConsoleButton.clicked.connect(self.runClearSerialConsoleButton)
        self.refreshSerialButton.clicked.connect(self.runRefreshSerialButton);
        self.pauseRTCButton.clicked.connect(lambda: self.runControlRTC('Pause RTC', RTC_PAUSE))
        self.resumeRTCButton.clicked.connect(lambda: self.runControlRTC('Resume RTC', RTC_RESUME))
        self.resetRTCButton.clicked.connect(lambda: self.runControlRTC('Reset RTC', RTC_RESET))

        self.filterPTTCheckBox.stateChanged.connect(self.runFilterSelect)
        self.filterHKCheckBox.stateChanged.connect(self.runFilterSelect)
        self.serialConsoleComboBox.currentIndexChanged.connect(self.runSerialConsolePortSelection)
        self.comPortComboBox.currentIndexChanged.connect(self.runSerialConnectionPortSelection)
        self.enableRFCheckBox.stateChanged.connect(self.runEnableRFOutput)
        self.enableBasebandCheckBox.stateChanged.connect(self.runEnableBaseband)
        self.periodicCheckBox.stateChanged.connect(self.runClockConfiguration)

        self.enableConsoleCheckBox.clicked.connect(self.runEnableSerialConsole)
        self.updateHKButton.clicked.connect(self.runUpdateHK)
        self.runSignalButton.clicked.connect(self.runSendSignalButton)

        self.hkRequestSpinBox.valueChanged.connect(self.runUpdateHKRequestTime)
        self.frequencySpinBox.valueChanged.connect(self.runUpdateVectorGenFrequency)
        self.levelSpinBox.valueChanged.connect(self.runUpdateVectorGenLevel)


        # set assynchronous signal handler for internal subthreads (i.e PackageReaderThread)
        self.runFatalErrorSignalBinding(self.appController.pyqtErrorSignal)
        self.runUpdateADCMeasureSignalBinding(self.appController.pyqtADCMeasureSignal)
        self.runSerialConsoleSignalBinding(self.appController.pyqtSerialConsoleSignal)
        self.runEnableSerialConsole()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Override default method to proper handle exit action when
        user clicks on X button on main window
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def closeEvent(self, event):
        if (self.runActionQuit()==False):
            event.ignore()
        
            
    def askToSavePackageList(self):
        choice = QtGui.QMessageBox().question(self, "Confirm", 
        "Save current list?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if (choice == QtGui.QMessageBox.Yes):
            self.runSaveFile()
            return True
        else:
            return False

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger methods
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runClockConfiguration(self):
        if (self.periodicCheckBox.isChecked()):
            self.runSignalButton.setEnabled(True)
        else:
            self.runSignalButton.setEnabled(False)

        if (self.appController.rohdeController.connected):
            if (self.periodicCheckBox.isChecked()):
                self.appController.rohdeController.setSingleShotClockConfig()
            else:
                self.appController.rohdeController.setPeriodicClockConfig()


    def runSendSignalButton(self):
        if (self.appController.rohdeController.connected):
            self.appController.rohdeController.triggerSignal()

    def runToneGenDialog(self):
        self.pausePackageReaderThread()
        ui = ToneGenerator.getToneGenDialog()

    def runLoadWaveformButton(self):
        fDialog = QtGui.QFileDialog()
        name = fDialog.getOpenFileName(self, 'Open Waveform File')
        if(name=='' or name==None):
            return
        if (name.contains('.wv')):
            try:
                self.waveformFileLineEdit.setText(name)
            except Exception as e:
                QMessageBox.critical(self, "Invalid File", "Could not open Package List file!")
        else:
            QMessageBox.critical(self, "Invalid File", "Invalid file extension")

    def runUpdateVectorGenFrequency(self):
        if (self.appController.rohdeController.connected):
            freq = str(self.frequencySpinBox.value())
            self.appController.rohdeController.setFreq(freq)

    def runUpdateVectorGenLevel(self):
        if (self.appController.rohdeController.connected):
            lvl = str(self.levelSpinBox.value())
            self.appController.rohdeController.setLevel(lvl)

    def runEnableBaseband(self):
        self.runClockConfiguration()
        if (self.appController.rohdeController.connected):
            if (self.enableBasebandCheckBox.isChecked()):
                if (self.waveformFileLineEdit.text() != '' and self.waveformFileLineEdit.text()!=None):
                    self.appController.rohdeController.sendWaveformFile(self.waveformFileLineEdit.text())
                self.appController.rohdeController.enableARB()
            else:
                self.appController.rohdeController.disableARB()

    def runEnableRFOutput(self):
        self.runClockConfiguration()
        if (self.appController.rohdeController.connected):
            if (self.enableRFCheckBox.isChecked()):
                self.appController.rohdeController.enableRFO();
            else:
                self.appController.rohdeController.disableRFO();

    def runConnectVectorGenButton(self):
        host_addr = str(self.rohdeIPLineEdit.text())
        if (re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host_addr) == None):#check if it's a valid IPv4 address
            QMessageBox.critical(self, "Invalid IP Address", "Provide a valid Host IP Address")
            return
        try:
            iconpath = "img/disconnect.png"
            btnText = "Disconnect"
            if (self.appController.rohdeController.connected==False):
                self.appController.rohdeController.connect(host_addr)
                self.vecGenStatusLabel.setText("Vector Generator connected at " + host_addr)
                self.runEnableRFOutput()
            else:
                self.appController.rohdeController.disconnect()
                self.vecGenStatusLabel.setText("Vector Generator disconnected.")
                iconpath = "img/connect.png"
                btnText = "Connect"

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(iconpath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.connectVectorGenButton.setIcon(icon)
            self.connectVectorGenButton.setText(btnText)
            

        except Exception as e:
            print (str(e))
            traceback.print_exc(file=sys.stdout)
            QMessageBox.critical(self, "Fail", "Could not connect device! Please, check connection configuration.")


    def runActionADCSampler(self):
        self.pausePackageReaderThread()
        ui = ADCDialog.getADCDialog(self.appController.decoderController)

    def runRefreshSerialButton(self):
        ports = serialenum.enumerate()
        cnt=0
        self.serialConsoleComboBox.clear()
        self.comPortComboBox.clear()
        for p in ports:
            self.serialConsoleComboBox.addItem("")
            self.comPortComboBox.addItem("")
            self.serialConsoleComboBox.setItemText(cnt, str(p))
            self.comPortComboBox.setItemText(cnt, str(p))
            cnt +=1
    def runUpdateHKRequestTime(self):
        self.appController.packageReaderThread.setHKReadDelay(int(self.hkRequestSpinBox.value()))

    def runSerialConsolePortSelection(self):
        port = str(self.serialConsoleComboBox.currentText())
        print ("Selected serial port: " + port)

        self.appController.serialMonitorThread.updatePort(port)

    def runSerialConnectionPortSelection(self):
        port = str(self.comPortComboBox.currentText())

    def runClearSerialConsoleButton(self):
        self.consoleTextEdit.clear()

    def runEnableSerialConsole(self):

        # if (self.connSerialRadio.isChecked()):
        #      QMessageBox.critical(self, "Fail", "Serial console can not be used while serial connection is selected.")
        #      self.enableConsoleCheckBox.setChecked(False)
        #      return

        if(self.enableConsoleCheckBox.isChecked()):
            self.consoleTextEdit.setStyleSheet("background-color: rgb(31, 31, 31);")
            self.consoleTextEdit.setEnabled(True)
            self.serialConsoleComboBox.setEnabled(True)
            try:
                if (not self.appController.serialMonitorThread.isRunning()):
                    self.appController.serialMonitorThread = ConsoleService()
                    self.appController.serialMonitorThread.setSerialConsoleSignal(self.appController.pyqtSerialConsoleSignal)
                    self.appController.serialMonitorThread.updatePort(str(self.serialConsoleComboBox.currentText()))
                    self.appController.serialMonitorThread.start()
            except Exception as e:
                print("Error: " + str(e))
                traceback.print_exc(file=sys.stdout)
        else:
            self.consoleTextEdit.setStyleSheet("background-color: rgb(180, 180, 180);")
            self.consoleTextEdit.setEnabled(False)
            self.serialConsoleComboBox.setEnabled(False)
            self.stopSerialMonitorThread()
            

    def runSaveFile(self):
        self.pausePackageReaderThread() 
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save Package List')
        self.appController.actionSavePackageList(name)
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Open Action
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runOpenFile(self):
        self.pausePackageReaderThread()
        fDialog = QtGui.QFileDialog()
        name = fDialog.getOpenFileName(self, 'Open Package List')
        if (name!= None and name!=''):
            try:
                self.appController.actionOpenPackageList(name)
            except Exception as e:
                QMessageBox.critical(self, "Invalid File", "Could not open Package List file!")

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Update Housekeeping configuration
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runUpdateHK(self):
        self.pausePackageReaderThread()        
        if(self.appController.actionUpdateHK()):
            QMessageBox.information(self, "Success", "HouseKeeping configuration sent!")
        else:
            QMessageBox.critical(self, "Fail", "HouseKeeping Configuration Failed. Please check connection to the device")
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for filter selection.
        This method is called everytime a filter
        checkbox is changed
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runFilterSelect(self):

        filterList = self.appController.getPackageFilterList()
        filterList.clear()
        if (self.filterPTTCheckBox.isChecked()):
            filterList.append(Package.PCKG_TYPE_PTT) # PTT
        elif(Package.PCKG_TYPE_PTT in filterList):
            filterList.remove(Package.PCKG_TYPE_PTT) # PTT

        if (self.filterHKCheckBox.isChecked()):
            filterList.append(Package.PCKG_TYPE_HK) # HK
        elif(Package.PCKG_TYPE_HK in filterList):
            filterList.remove(Package.PCKG_TYPE_HK) # PTT

        self.appController.actionFilterSelect(filterList)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for disconnect button
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runDisconnect(self):
        
        try:
            self.runActionPause()
            if (self.runActionStop()==True):
                self.appController.actionDisconnect()
                self.appController.actionStopI2CServer()
                self.connectionConfigWidget.setEnabled(True)
                self.actionPause.setEnabled(False)
                self.actionPlay.setEnabled(False)
                self.actionStop.setEnabled(False) 
                self.actionEchoTest.setEnabled(False)
                self.actionClear.setEnabled(False)
                self.actionConnect.setEnabled(True)
                self.actionDisconnect.setEnabled(False)
                self.actionADCSampler.setEnabled(False)
                self.deviceConfigWidget.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Fail", "Somthing went wrong. Could not disconnect device.")
            print (str(e))
            traceback.print_exc(file=sys.stdout)
            return

        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Connect Button
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runConnect(self):
        connected = False
        if(self.connSerialRadio.isChecked()):
            port = str(self.comPortComboBox.currentText())
            try:
                self.appController.setDeviceControllerConnection(ArduinoConnection(port=port, baudrate='115200'))
                self.statusBar().showMessage("Connecting device... Arduino I2C-Bridge at " + port)
                self.appController.actionConnect()
                connected=True
            except Exception as e:
                connected = False;
                print (str(e))
                # traceback.print_exc(file=sys.stdout)
                QMessageBox.critical(self, "Fail", "Could not connect device! Please, check connection configuration.")
        else:
            connected=False
            if(self.connFtdiRadio.isChecked()):
                connType='FTDI'
                QMessageBox.information(self, "Connection", "Sorry! " + connType +" connection bridge is not functional yet. ")

        if (connected==True):
            self.connectionConfigWidget.setEnabled(False)
            self.actionPause.setEnabled(False)
            self.actionConnect.setEnabled(False)
            self.actionStop.setEnabled(False) 
            self.actionPlay.setEnabled(True)
            self.actionADCSampler.setEnabled(True)
            self.actionEchoTest.setEnabled(True)
            self.actionClear.setEnabled(True)
            self.actionDisconnect.setEnabled(True)
            self.deviceConfigWidget.setEnabled(True)




    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Echo Test
        This method issues the App Controller to send a simple Echo Command
        to the device board. It is intendedto check the communcation 
        channel between the tester and the FPGA. If the test succeeds 
        and echo message is printed on the serial console
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runEchoTest(self):
        self.pausePackageReaderThread()
        self.appController.actionEchoTest()
        # if (self.appController.actionEchoTest()==True):
        #     QMessageBox.information(self, "Success", "Echo command sent!")
        # else:
        #     QMessageBox.critical(self, "Fail", "Echo command failed! ")

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Control RTC action.
        This method issues de App Controller to send a RTC 
        Pause/Resume/Reset command to the FPGA board
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runControlRTC(self, name, cmdId):
        self.pausePackageReaderThread()
        if (self.appController.actionControlRTC(cmdId)==False):
            QMessageBox.critical(self, "Fail", name+" Failed! ")

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Set RTC action.
        This method issues de App Controller to send a RTC 
        Set command to the FPGA board
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runSetRTCButton(self):
        self.pausePackageReaderThread()
        if (self.appController.actionSetRTC()==True):
            QMessageBox.information(self, "Success", "RTC configuration sent!")
        else:
            QMessageBox.critical(self, "Fail", "RTC Configuration Failed. Please check connection to the device")

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Row Select
        This method issues de App Controller to display information
        about the package currently selected on the main package table
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runRowSelection(self):
        if (len(self.mainTableWidget.selectedIndexes ())>0):
            selectedItem = self.mainTableWidget.selectedIndexes ()[0]
            row_number = selectedItem.row()
            self.appController.actionRowSelected(row_number)
        else:
            self.appController.actionRowSelected(-1)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Quit action
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runActionQuit(self):
        
        
        # if (self.appController.isPackageListEmpty()==False):
        #     self.askToSavePackageList()
        # if (self.appController.isPackageReaderRunning()):
        #     if (self.runActionStop()==False):
        #         return False
        # else:
        #     choice = QtGui.QMessageBox().question(self, "Confirm", 
        #     "Exit Application?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        #     if (choice == QtGui.QMessageBox.No):
        #         return False
        
        self.stopAllIndependentThreads()
        self.appController.decoderController.stopController()
        self.appController.actionStopI2CServer()
        self.statusBar().showMessage("Closing...")
        time.sleep(0.25) # wait all threads go down
        QtGui.qApp.quit()
        return True
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Read Packages Action.
        This method issues de App Controller to start a new
        package reading thread. New Packages read from
        FPGA are placed into the application's main package table
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runActionPlay(self):
        
        if (self.appController.isPackageReaderRunning()==False and self.appController.isPackageListEmpty()==False):
            self.askToSavePackageList()
            self.appController.resetAppController()  #               
        
        self.statusBar().showMessage("Reading PTT packages...")
        self.appController.resumePackageReader()
        self.actionPause.setEnabled(True)
        self.actionPlay.setEnabled(False)
        self.actionStop.setEnabled(True)
        self.filterWidget.setEnabled(False)
        self.deviceConfigWidget.setEnabled(False)

        self.appController.actionPackageReader()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Pause Package Reading Action
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runActionPause(self):
        self.pausePackageReaderThread()
        self.deviceConfigWidget.setEnabled(True)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Stop Package Reading Action
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runActionStop(self):
        self.deviceConfigWidget.setEnabled(True)
        if (self.appController.isPackageReaderRunning()):
            choice = QtGui.QMessageBox().question(self, "Confirm", 
                "Stop reading packages?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if (choice == QtGui.QMessageBox.Yes):
                self.stopPackageReaderThread()
                return True
            else:
                return False
        else:
            return True

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Trigger method for Clear Main Package Table Action
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runActionClear(self):
        self.appController.resetAppController()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Internal control method for pausing all created threads like
        the Package Reader thread 
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def pausePackageReaderThread(self):
        # pause Package Reading if its running
        if (self.appController.isPackageReaderRunning() and self.appController.isPackageReaderPaused()==False):
            self.appController.pausePackageReader()
            self.actionPause.setEnabled(False)
            self.actionPlay.setEnabled(True)
            self.actionStop.setEnabled(True)
            self.filterWidget.setEnabled(True)  
            self.statusBar().showMessage("Paused")
            time.sleep(0.5)

    def stopAllIndependentThreads(self):
        self.stopPackageReaderThread()
        self.stopSerialMonitorThread()

    def stopSerialMonitorThread(self):
        self.appController.stopSerialMonitor()

    def stopPackageReaderThread(self):
        
        # pause Package Reading if its running
        # self.appController.stopThreads() 
        self.appController.stopPackageReader()  
        self.actionStop.setEnabled(False)
        self.actionPause.setEnabled(False)
        self.actionPlay.setEnabled(True)  
        self.actionStop.setEnabled(False)
        self.filterWidget.setEnabled(True)  
        self.statusBar().showMessage("Ready")
        return True

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Signal Handling for internal subthreads
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def runSerialConsoleSignalBinding(self, signal):
        signal.connect(self.runUpdateSerialConsoleHandling)
    
    def runFatalErrorSignalBinding(self, signal):
        signal.connect(self.runFatalErrorHandling)

    def runUpdateADCMeasureSignalBinding(self, signal):
        signal.connect(self.runUpdateADCMeasureHandling)

    def runUpdateSerialConsoleHandling(self):
        self.appController.actionUpdateSerialConsole()

    def runFatalErrorHandling(self):
        QMessageBox.critical(None, "Error", "An unexpected error had ocurred. Reset Connection")
        try:
            # self.stopPackageReaderThread()
            # self.appController.actionDisconnect()
            # self.appController.actionStopI2CServer()
            self.runDisconnect()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Somthing went wrong. Could not disconnect device.")
            print (str(e))

        # self.actionPause.setEnabled(False)
        # self.actionPlay.setEnabled(False)
        # self.actionStop.setEnabled(False) 
        # self.actionEchoTest.setEnabled(False)
        # self.actionClear.setEnabled(False)

        # self.actionConnect.setEnabled(True)
        # self.actionDisconnect.setEnabled(False)
        # self.controlToolBox.setEnabled(False)

    # updates the ADC RMS chart whenever a new HK package
    # is received
    def runUpdateADCMeasureHandling(self):
        self.appController.actionUpdateADCMeasures()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SBCDA Controller Apllicaton start point
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def main():

    app = QApplication(sys.argv)

    w = SBCDAControllerApp()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
