# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './py/adcdialog.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
import platform
import time
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from math import cos, sin, tan
import numpy as np

if (sys.version_info.major>=3):
    import _thread as thread
else:
    import thread

from .adcdesign import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTime, QDate, QObject
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import QInputDialog, QMessageBox
from PyQt5.QtGui import *
from modules.definitions import *
from modules.service.packageservice import *
from modules.control.measurevc import *
from modules.control.adcchart import *


PI = 3.14159265359
ADC_FS = 128000.0; # 128ksp/s


class ADCDialog(QDialog, Ui_ADCDialog, ChartController):

    currentADCPackage=None
    adcChart = None
    deviceController=None
    """docstring for ADCDialog"""
    def __init__(self, deviceController, parent=None):
        super(ADCDialog, self).__init__(parent)
        self.setupUi(self)
        self.deviceController = deviceController
        self.adcChart = ADCChart(self.chartCanvasWidget, self.toolbarCanvasWidget)
        self.controlBindings()
        self.lastUiAdjustments()

    def lastUiAdjustments(self):
        pass

    def controlBindings(self):
        self.reloadButton.clicked.connect(self.runReloadButton)
        self.okButton.clicked.connect(self.close)
        self.exportButton.clicked.connect(self.runExportButton)

   
    def runReloadButton(self):
        try:
            pckg = self.requestADCPackage()
            if (pckg != None):
                self.currentADCPackage = pckg
                #pckg.loadSinus()
                # print ">>>>>>>>>>>>>>>>>>>>>> "
                # for i in range(0, len(pckg.adcSamples)):
                #     re = (pckg.adcSamples[i]>>16)&0x0000FFFF
                #     im = (pckg.adcSamples[i])&0x0000FFFF
                #     #print (" %04x %04x "%(re, im))
                
                # print "<<<<<<<<<<<<<<<<<<<<<<  "
                y = pckg.getComplexSignal()
                t = pckg.timeArray
                Fs = pckg.Fs
                self.adcChart.updateChart(y, t, Fs)
            else:
                QMessageBox.critical(self, "Transmission Error", "ADC Package could not be received. ")
        except Exception as e:
                print("Error: " + str(e))
                traceback.print_exc(file=sys.stdout)

    def requestADCPackage (self):
         
        self.progressBar.setEnabled(True)
        self.progressBar.setValue(0)
        # 1 - Set fw to config mode
        if (self.deviceController.setCMDMode()==False):
            print ("> Fail! Could not set CMD MODE.")
            self.progressBar.setValue(0)
            self.progressBar.setEnabled(False)
            return None

        self.progressBar.setValue(20)
        # 2 - Request fw to load a adc package
        self.deviceController.adcLoad()

        self.progressBar.setValue(30)

        # 3 - wait until package is loaded
        timeout = 10
        while (self.deviceController.adcState() != ADC_READY):
            time.sleep(0.01)
            timeout = timeout-1
            if (timeout == 0):
                print ("> Fail! Could not get ADC_READY state.")
                self.progressBar.setValue(0)
                self.progressBar.setEnabled(False)
                return None

        self.progressBar.setValue(50)
        # 4- set fw to adc mode
        self.deviceController.setADCMode()

        self.progressBar.setValue(60)

        # 5 - Read adc package
        pckg = None
        timeout = 2
        while (pckg == None):
            pckg = self.deviceController.getADCPackage()
            timeout = timeout - 1;
            if (pckg == None and timeout == 0):
                print ("> Fail! Could not get ADC_PACKAGE.")
                self.progressBar.setValue(0)
                break
        #pckg.loadSinus()
        if (pckg!=None):
            # print pckg.adcSamples
            self.progressBar.setValue(100)
        self.progressBar.setEnabled(False)
        return pckg

    def runExportButton(self):
        if (self.currentADCPackage == None):
            return

        name = QtGui.QFileDialog.getSaveFileName(self, 'Export Sample List')
        if (name==None):
            return
        extension =  '.m'
        if (extension not in name):
            name += extension

       
        adc_i  = "adc_i = ["
        adc_q = "adc_q = [ "
        adc_samples = "adc_samples = [ "
        t = "time = [ "
        for k in range(0, len(self.currentADCPackage.adcSamples)):
            re = (self.currentADCPackage.adcSamples[k] >> 16) & 0x0000FFFF;
            im = (self.currentADCPackage.adcSamples[k]) & 0x0000FFFF;
            re = ctypes.c_short(re).value
            im = ctypes.c_short(im).value

            adc_i += "%d, "%re
            adc_q += "%d, "%im

            adc_samples += "%d "%self.currentADCPackage.adcSamples[k]
            t += "%f, "%self.currentADCPackage.timeArray[k]
        adc_i  += "]; \n"
        adc_q += "]; \n"
        adc_samples += "]; \n"
        t += "]; \n"

        file = open(name, 'wb')
        file.write("FS = %lf ; \n"%(self.currentADCPackage.Fs))
        file.write(adc_samples)
        file.write(adc_i)
        file.write(adc_q)
        file.write(t)
        file.close()

    @staticmethod
    def getADCDialog(deviceController, parent = None):
        dialog = ADCDialog(deviceController, parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
        

def main():

    app = QtGui.QApplication(sys.argv)

    w = SBCDAControllerApp()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    main()