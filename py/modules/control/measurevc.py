import sys
import time
import random
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
import math


class MeasuresViewController(ChartController):

    fig1=0
    fig2=0
    plotlyFigure = 0
    adcChartWidget=None
    currentChartWidget=None
    toolbarCanvasWidget=None
    adcCanvas=None
    currentCanvas=None
    chartToolbar=None

    adcAxis=0
    currentAxis=0

    def __init__(self, chartCanvas_0, chartCanvas_1, parentApp=None):
        self.adcChartWidget = chartCanvas_0
        self.currentChartWidget = chartCanvas_1

        # self.pltFigure = plt.figure(figsize=(3,5))
        # self.pltFigure.patch.set_facecolor('None')
        # self.pltFigure.patch.set_alpha(0.8)
        self.fig1 = plt.figure(figsize=(3,3))
        plt.style.use('dark_background')
        self.fig1.patch.set_facecolor('None')
        self.fig1.patch.set_alpha(0.8)
        
        self.fig2 = plt.figure(figsize=(3,3))
        plt.style.use('dark_background')
        self.fig2.patch.set_facecolor('None')
        self.fig2.patch.set_alpha(0.8)

        self.adcCanvas = FigureCanvas(self.fig1)
        self.currentCanvas = FigureCanvas(self.fig2)
        
        layout = self.adcChartWidget.layout()
        layout.addWidget(self.adcCanvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout = self.currentChartWidget.layout()
        layout.addWidget(self.currentCanvas)
        layout.setContentsMargins(0, 0, 0, 0)

        #layout.setContentsMargins(left, top, right, bottom)
        self.adcAxis = self.fig1.gca() #plt.subplot2grid((2,2), (0,0), colspan=2)
        self.currentAxis = self.fig2.gca()

        self.updateChart([], PackageReaderService.HK_PACKAGE_LIST_SIZE)


    def updateChart(self, pcktList, max_length):
        # print ("> Update ADC Chart < ")
        adc_values = [0]*max_length
        c1_values = [0]*max_length
        c2_values = [0]*max_length
        xvalues = np.arange(max_length)
        i = 0
        for p in pcktList:
            if (i<max_length):
                #adc_values[i] = p.adc_rms/32767.0
                # calc to present rms values in
                # dBm, related to the adc resolution
                # of 16 bits:
                # dBm = 20 * log10( rms/2^15)
                v = ((p.adc_rms*1.0)/(1<<15))
                if (v!=0):
                    adc_values[i] = 20*math.log(v, 10)
                else:
                    adc_values[i] = 0

                p.current_sensor1 = 0
                if (p.current_sensor1==0):
                    p.current_sensor1 = random.uniform(0.4, 0.6)
                c1_values[i] = p.current_sensor1
                p.current_sensor2 = 0
                if (p.current_sensor2==0):
                    p.current_sensor2 = random.uniform(0.4, 0.6)
                c2_values[i] = p.current_sensor2
            else:
                adc_values.append(p.adc_rms)
                c2_values.append(p.current_sensor2)
                c1_values.append(p.current_sensor1)
            i+=1
        
        # create an axis
        self.adcAxis.clear()
        self.adcAxis.set_xlim([0,max_length])
        self.adcAxis.set_ylim(-100, 0)
        self.barPlot(xvalues, adc_values, self.adcAxis, None, None, None)
        self.plotDetails(self.adcAxis, None, "dBFs", None, color='yellow', yrotation=90, fontsize=10)
        self.adcAxis.grid(True, linestyle='dotted')

        self.currentAxis.clear()
        self.currentAxis.set_xlim([0,max_length])
        self.currentAxis.set_ylim(0, 1)
        self.linePlot2(self.currentAxis, xvalues, c1_values, "Sensor A", c2_values, "Sensor B", None, None, None)
        self.plotDetails(self.currentAxis, None, "A", None, color='yellow', yrotation=90, fontsize=10)
        self.currentAxis.grid(True, linestyle='dotted')
        # refresh canvas
        #plt.style.use('fivethirtyeight')
        #plt.style.use('dark_background')
        #plt.style.use('seaborn')
        #plt.style.use('ggplot')

        self.fig1.tight_layout()
        self.fig2.tight_layout()
        self.adcCanvas.setContentsMargins(10, 10, 10, 10)
        self.adcCanvas.draw()

        self.currentCanvas.setContentsMargins(10, 10, 10, 10)
        self.currentCanvas.draw()
        self.fig1.tight_layout()
        self.fig2.tight_layout()
        

        
