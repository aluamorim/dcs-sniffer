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
from modules.connection.i2cnetcomm import NetConnection
from modules.connection.arduinocomm import ArduinoConnection
from modules.connection.serialcomm import SerialConnection
from modules.definitions import *
from modules.service.packageservice import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar


class ViewController(object):
     """docstring for ClassName"""
     def __init__(self):
         super(ViewController, self).__init__()
          
class ChartController(ViewController):
	"""docstring for ChartController"""
	def __init__(self):
		super(ChartController, self).__init__()

	def updateChart(self):
		pass

	def barPlot(self, xvalues, yvalues, axis, title='', ylabel='', xlabel=''):
		axis.bar(xvalues, yvalues, align='center', alpha=0.6)
		axis.grid(linestyle='dotted')
		#plt.xticks(y_pos, x)
		self.plotDetails(axis, title, ylabel, xlabel)



	def linePlot2(self, axis, xvalues=[], y1values=[], label1='L1', y2values=[],  label2='L2', title='', ylabel='', xlabel=''):
		line1, = axis.plot(xvalues, y1values, 'y', label=label1 )
		line2, = axis.plot(xvalues, y2values, 'b', label=label2 )
		self.plotDetails(axis, title, ylabel, xlabel)
		axis.legend(loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=3, fancybox=True, fontsize=7)
		#axis.legend(loc='best', numpoints=1, fancybox=True)
		#axis.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0., fontsize=8)
		# plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
		#plt.xticks(y_pos, x)

	def linePlot(self, xvalues, yvalues, axis, color='y'):
		axis.plot(xvalues, yvalues, color)

	def linePlot(self, xvalues, yvalues, axis, title='', ylabel='', xlabel=''):
		axis.plot(xvalues, yvalues)
		#plt.xticks(y_pos, x)
		self.plotDetails(axis, title, ylabel, xlabel)

	def stemPlot(self, xvalues, yvalues, axis, title='', ylabel='', xlabel=''):
		axis.stem(xvalues, yvalues, '-.')
		#plt.xticks(y_pos, x)
		self.plotDetails(axis, title, ylabel, xlabel)

	def plotDetails(self, axis, title, ylabel, xlabel, color='white', yrotation=0, fontsize=10):

		if (ylabel != None):
			axis.set_ylabel(ylabel, fontsize=fontsize, rotation=yrotation, color=color)
		# axis.yaxis.set_label_coords(-0.05,1.08)
		if (xlabel!=None):
			axis.set_xlabel(xlabel, fontsize=fontsize, color=color)
		if (title!=None):
			axis.set_title(title, fontsize=fontsize, loc='left', y=1.05, color=color)

		axis.patch.set_facecolor('None')