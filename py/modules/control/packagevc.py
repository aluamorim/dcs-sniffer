import sys
import time
import random
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

if (sys.version_info.major>=3):
    import _thread as thread
else:
    import thread

from PyQt5 import QtCore, QtGui
from collections import deque
from modules.entity import *
from modules.entity.controller import *
from modules.connection.i2cnetcomm import *
from modules.connection.serialcomm import *
from modules.definitions import *
from modules.service.packageservice import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from .viewcontroller import *


           
class PackageViewController(ViewController):

    tableWidget=None
    treeWidget=None
    rawWidget=None
    row_count=0

    def __init__(self, table, tree, raw):
        self.tableWidget = table
        self.treeWidget= tree
        self.rawWidget = raw
        self.row_count= 0

    def clearTable(self):
        self.tableWidget.setRowCount(0)

    def removeRow(self, row):
        self.tableWidget.removeRow(row)
        
    def addRow(self, pckt=None, rowCnt=0, globalCnt=0):
        #prepare table data
        try:
            self.tableWidget.setRowCount(rowCnt)
            rowCnt -=1

            item = QtGui.QTableWidgetItem(str(globalCnt))
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowCnt, 0, item)
            item = QtGui.QTableWidgetItem(pckt.typeStr)
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowCnt, 1, item)
            item = QtGui.QTableWidgetItem(pckt.timeStamp())
            item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowCnt, 2, item)
            item = QtGui.QTableWidgetItem(" General Info About the Package Number: " + str(globalCnt))
            self.tableWidget.setItem(rowCnt, 3, item)
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc(file=sys.stdout)

    def loadTableFromList(self, packageList=None):

        row = 1
        self.tableWidget.setRowCount(0)
        for pckt in packageList:
            self.addRow(pckt, row, row)
            row+=1

    def fillRawPackageForm(self, pckt):

        try:
            vec = pckt.toArray()
            for i in range(0, len(vec), 16):
                row = int(i/16)
                self.rawWidget.setRowCount(row+1)
                item = QtGui.QTableWidgetItem(("%04X"%i))
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                self.rawWidget.setItem(row, 0, item)

                word = vec[i:(i+16)]
                val = '  '
                char = ''
                for w in word:
                    val += ' %02X'%w
                    if (w>=32 and w <=126): #check if is printable char
                        char += chr(w) + ' '
                    else:
                        char += '. '

                item = QtGui.QTableWidgetItem(val)
                #item.setTextAlignment(QtCore.Qt.AlignHLeft|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                self.rawWidget.setItem(row, 1, item)

                item = QtGui.QTableWidgetItem(char)
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                self.rawWidget.setItem(row, 2, item)
            self.rawWidget.resizeColumnsToContents()
            self.rawWidget.horizontalHeader().setStretchLastSection(True)
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc(file=sys.stdout)

    def fillHKDetailForm(self, pckt):

        try:
            root = self.treeWidget
            subItem = QtGui.QTreeWidgetItem(root)
            subItem.setText(0, "Package Type: ")
            subItem.setText(1, "Housekeeping Data Package ")
            #######################################################################################
            timeTagItem = self.addSubItem(root, "Time Tag: ", pckt.timeTag )
            timeTagItem.setText(1, pckt.timeStamp())
            timeTag = self.addChild(timeTagItem, "Hex: ", ''.join(("%02x "%(c) for c in pckt.timeTag)))
            
            year = self.addSubItem(timeTagItem, "Year: ", [pckt.timeTag[0]])
            self.addDecBinChildren(year, pckt.timeTag[0])
            month = self.addSubItem(timeTagItem, "Month: ", [(pckt.timeTag[1]%13)])
            self.addDecBinChildren(month, pckt.timeTag[1])
            day = self.addSubItem(timeTagItem, "Day: ", [pckt.timeTag[2]])
            self.addDecBinChildren(day, pckt.timeTag[2])
            hour = self.addSubItem(timeTagItem, "Hour: ", [pckt.timeTag[3]])
            self.addDecBinChildren(hour, pckt.timeTag[3])
            minute = self.addSubItem(timeTagItem, "Minute: ", [pckt.timeTag[4]])
            self.addDecBinChildren(minute, pckt.timeTag[4])
            sec = self.addSubItem(timeTagItem, "Second: ", [pckt.timeTag[5]])
            self.addDecBinChildren(sec, pckt.timeTag[5])

            #######################################################################################
            adcRmsItem = self.addSubItem(root, "ADC RMS: ", [pckt.adc_rms])
            self.addDecBinChildren(adcRmsItem, pckt.adc_rms)

            #######################################################################################
            cs1Item = self.addSubItem(root, "Current Sensor 1: ", [pckt.current_sensor1])
            self.addDecBinChildren(cs1Item, pckt.current_sensor1)

            #######################################################################################
            cs2Item = self.addSubItem(root, "Current Sensor 2: ", [pckt.current_sensor2])
            self.addDecBinChildren(cs2Item, pckt.current_sensor2)

            #######################################################################################
            pllSyncItem = self.addSubItem(root, "PLL Sync Bit: ", [pckt.pll_sync])
            self.addDecBinChildren(pllSyncItem, pckt.pll_sync)

            #######################################################################################
            ovcItem = self.addSubItem(root, "Over Current Fail: ", [pckt.over_current_fail])
            self.addDecBinChildren(ovcItem, pckt.over_current_fail)
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc(file=sys.stdout)



    def fillPTTDetailForm(self, pckt):

        try:
            root = self.treeWidget
            subItem = QtGui.QTreeWidgetItem(root)
            subItem.setText(0, "Package Type: ")
            subItem.setText(1, "PTT Data Package ")
            
            #######################################################################################
            pckgIdItem = self.addChild(root, "PTT IdNumber: ", '%d'%pckt.pttIdNumber )
            self.addHexBinChildren(pckgIdItem, pckt.pttIdNumber)


            #######################################################################################
            freqValue = pckt.freqMeasure;
            if (freqValue & 0x400):
                freqValue |= 0xfffffc00;
            freqValue = ctypes.c_short(freqValue).value
            freqValue = (freqValue*62)/1000;
            freqItem = self.addChild(root, "Frequency: ", '%.02f kHz'%(freqValue))
            self.addHexBinChildren(freqItem, pckt.freqMeasure)

            #######################################################################################
            ampRmsItem = self.addChild(root, "Amp RMS: ", '%d'%pckt.ampRms )
            self.addHexBinChildren(ampRmsItem, pckt.ampRms)

            #######################################################################################
            decNumItem = self.addChild(root, "Decoder Number: ", '%02x'%pckt.decoderNumber )
            self.addDecBinChildren(decNumItem, pckt.decoderNumber)

            #######################################################################################
            msgLenItem = self.addChild(root, "Message Length: ", '%02x'%pckt.msgLength )
            self.addDecBinChildren(msgLenItem, pckt.msgLength)
            
            #######################################################################################
            timeTagItem = self.addSubItem(root, "Time Tag: ", pckt.timeTag )
            timeTagItem.setText(1, pckt.timeStamp())
            timeTag = self.addChild(timeTagItem, "Hex: ", ''.join(("%02x "%(c) for c in pckt.timeTag)))
            
            year = self.addSubItem(timeTagItem, "Year: ", [pckt.timeTag[0]])
            self.addDecBinChildren(year, pckt.timeTag[0])
            month = self.addSubItem(timeTagItem, "Month: ", [(pckt.timeTag[1]%13)])
            self.addDecBinChildren(month, pckt.timeTag[1])
            day = self.addSubItem(timeTagItem, "Day: ", [pckt.timeTag[2]])
            self.addDecBinChildren(day, pckt.timeTag[2])
            hour = self.addSubItem(timeTagItem, "Hour: ", [pckt.timeTag[3]])
            self.addDecBinChildren(hour, pckt.timeTag[3])
            minute = self.addSubItem(timeTagItem, "Minute: ", [pckt.timeTag[4]])
            self.addDecBinChildren(minute, pckt.timeTag[4])
            sec = self.addSubItem(timeTagItem, "Second: ", [pckt.timeTag[5]])
            self.addDecBinChildren(sec, pckt.timeTag[5])
          
            #######################################################################################
            sensorDataItem = self.addSubItem(root, "User Data: ", pckt.sensorData )
            for i in range(0, len(pckt.sensorData), 4):
                w = pckt.sensorData[i:(i+4)]
                wordItem = self.addSubItem(sensorDataItem, ("Word[%d]: "%int(i/4)), w )


            crcItem = self.addChild(root, "Received CRC: ", '%04x'%pckt.crc )
            self.addDecBinChildren(crcItem, pckt.crc)

            calCRCItem = self.addChild(root, "Calculated CRC: ", '%04x'%pckt.localCRC )
            self.addDecBinChildren(calCRCItem, pckt.localCRC)
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc(file=sys.stdout)
        
        

    # Tree Widget Related Methods - Adds a new SubItem to a previous item
    def addSubItem(self, item, name, values):
        
        subItem = QtGui.QTreeWidgetItem(item)
        subItem.setFlags(subItem.flags() | QtCore.Qt.ItemIsEditable)
        subItem.setText(0, name)
        str = ''
        for v in values:
            str += (' %02x '%(v))
        subItem.setText(1, str)
        return subItem
    # Tree Widget Related Methods - Adds decimal and binary values subitens
    def addDecBinChildren(self, item, value):
        decValue = QtGui.QTreeWidgetItem(item)
        decValue.setFlags(decValue.flags() | QtCore.Qt.ItemIsEditable)
        decValue.setText(0, "Dec:")
        decValue.setText(1, str(value))

        binValue = QtGui.QTreeWidgetItem(item)
        binValue.setFlags(binValue.flags() | QtCore.Qt.ItemIsEditable)
        binValue.setText(0, "Bin:")
        binValue.setText(1, bin(int(value))) 

    def addHexBinChildren(self, item, value):
        decValue = QtGui.QTreeWidgetItem(item)
        decValue.setFlags(decValue.flags() | QtCore.Qt.ItemIsEditable)
        decValue.setText(0, "Hex:")
        decValue.setText(1, ("%04x"%value))

        binValue = QtGui.QTreeWidgetItem(item)
        binValue.setFlags(binValue.flags() | QtCore.Qt.ItemIsEditable)
        binValue.setText(0, "Bin:")
        binValue.setText(1, bin(int(value)))

    def addChild(self, item, name, value):
        child = QtGui.QTreeWidgetItem(item)
        child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
        child.setText(0, name)
        child.setText(1, value)
        return child 