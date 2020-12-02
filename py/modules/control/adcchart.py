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

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTime, QDate, QObject
#from PyQt5.QtGui import QInputDialog, QMessageBox
from PyQt5.QtGui import *
from modules.definitions import *
from modules.service.packageservice import *
from modules.control.measurevc import *

PI = 3.14159265359
ADC_FS = 128000.0 # 128ksp/s

class ADCChart(ChartController):

	pltFigure=0
	plotlyFigure = 0
	chartCanvasWidget=None
	toolbarCanvasWidget=None
	chartCanvas=None
	chartToolbar=None

	inPhaseAxis=0
	inQuadAxis = 0
	fftAxis=0
	fftdBAxis = 0
	currentADCPackage=None
	hanning = None;


	def __init__(self, chartCanvasWidget,  toolbarCanvasWidget=None, plotx=10, ploty=12):
		super(ADCChart, self).__init__()

		self.chartCanvasWidget=chartCanvasWidget
		self.toolbarCanvasWidget=toolbarCanvasWidget
		self.chartLayout(plotx, ploty)



	def chartLayout(self, plotx=10, ploty=12):
		try:
			#self.pltFigure = plt.figure(figsize=(5,7))
			self.pltFigure = plt.figure(figsize=(plotx, ploty))
			self.pltFigure.patch.set_facecolor('None')
			self.pltFigure.patch.set_alpha(0.8)

			self.chartCanvas = FigureCanvas(self.pltFigure)
			self.chartToolbar = NavigationToolbar(self.chartCanvas, None)

			layout = self.chartCanvasWidget.layout()
			layout.addWidget(self.chartCanvas)
			#layout.setContentsMargins(left, top, right, bottom)
			layout.setContentsMargins(0, 0, 0, 0)
			self.chartCanvasWidget.setLayout(layout)

			if (self.toolbarCanvasWidget != None):
				toolbarLayout = self.toolbarCanvasWidget.layout()
				toolbarLayout.addWidget(self.chartToolbar)
				#toolbarLayout.setContentsMargins(0, 0, 0, 0)
				self.toolbarCanvasWidget.setLayout(toolbarLayout)

			self.inPhaseAxis = plt.subplot2grid((3,2), (0,0), colspan=1)
			self.inQuadAxis = plt.subplot2grid((3,2), (0,1), colspan=1)
			self.fftdBAxis = plt.subplot2grid((3,2), (1,0), colspan=2)
			self.fftAxis = plt.subplot2grid((3,2), (2,0), colspan=2)

			# self.chartCanvas.draw()
			# self.chartCanvas.setContentsMargins(0, 0, 0, 0)
			y = [0]*ADC_PACKAGE_SAMPLES
			t = np.arange(ADC_PACKAGE_SAMPLES)
			[Y, frq] = self.calcFFT(y, ADC_SAMPLE_FREQ)
			self.updateChart(y, t, ADC_FS)
		except Exception as e:
			print (str(e))
			traceback.print_exc(file=sys.stdout)

	def updateChart(self, y, t, Fs):
		#[Y, frq] = self.calcFFT(y, Fs);
		[Y, frq] = self.calcFFT_Hanning(y, Fs);
		#self.updateChart(np.abs(y), t, np.abs(Y), frq)
		#self.updateChart(np.abs(y), t, np.abs(Y), frq)
		self.updateChartCanvas(np.real(y), np.imag(y), t, np.abs(Y), frq/1000)

	def updateChartCanvas(self, inPhase, inQuad, t, fft, k):

		#plt.style.use('fivethirtyeight')
		plt.style.use('dark_background')
		#plt.style.use('seaborn')
		#plt.style.use('ggplot')
		#plt.style.use('bmh')
		self.inPhaseAxis.clear()
		self.inQuadAxis.clear()
		self.fftAxis.clear()
		self.fftdBAxis.clear()

		#self.inPhaseAxis.set_ylim(-1, 1)
		self.linePlot(t, inPhase, self.inPhaseAxis)
		self.plotDetails(self.inPhaseAxis, None, "Inphase i(t)", "t(ms)", color='yellow', yrotation=90, fontsize=10)
		self.inPhaseAxis.grid(True, linestyle='dotted')

		#self.inQuadAxis.set_ylim(-1, 1)
		self.linePlot(t, inQuad, self.inQuadAxis)
		self.plotDetails(self.inQuadAxis, None, "Quad q(t)", "t(ms)", color='yellow', yrotation=90, fontsize=10)
		self.inQuadAxis.grid(True, linestyle='dotted')


		#self.fftAxis.set_xlim(0,len(k))
		#self.fftAxis.set_ylim(0, 1)
		self.linePlot(k, fft/(1<<15), self.fftAxis)
		self.plotDetails(self.fftAxis, None, "|Y(k)|", "Freq(kHz)", color='yellow', yrotation=90, fontsize=10)
		self.fftAxis.grid(True, linestyle='dotted')

		for i in range(0, len(k)):
			# fft[i] = np.abs(fft[i])*1.0
			if (fft[i]!=0):
			    fft[i] = 20.0*np.log10(fft[i]/(1<<15))

		# self.fftdBAxis.set_ylim(-200, 0)
		self.linePlot(k, fft, self.fftdBAxis)
		self.plotDetails(self.fftdBAxis, None, "dBFs", "Freq(kHz)", color='yellow', yrotation=90, fontsize=10)
		self.fftdBAxis.grid(True, linestyle='dotted')

		# refresh canvas
		plt.grid(True, linestyle='dotted')
		self.pltFigure.tight_layout()
		self.chartCanvas.setContentsMargins(0, 0, 0, 0)
		self.chartCanvas.draw()

	def calcFFT(self, y, Fs):
		n = len(y) # length of the signal
		Fs = Fs*1.0
		Ts = 1.0/Fs
		frq = np.fft.fftfreq(n, Ts)
		frq = np.fft.fftshift(frq)
		Y = np.fft.fft(y)/n # fft computing and normalization
		Y = np.fft.fftshift(Y)
		return [Y, frq]

	def calcFFT_Hanning(self, y, Fs):
		self.hanning = np.hanning(len(y));
		mean = np.mean(self.hanning)
		self.hanning = self.hanning/mean;
		y = np.multiply(y, self.hanning)
		y = np.lib.pad(y, (2048,0), 'constant', constant_values=(0, 0))

		n = len(y) # length of the signal
		Fs = Fs*1.0
		Ts = 1.0/Fs
		frq = np.fft.fftfreq(n, Ts)
		frq = np.fft.fftshift(frq)
		Y = np.fft.fft(y)/n # fft computing and normalization
		Y = np.fft.fftshift(Y)
		return [Y, frq] 
 

