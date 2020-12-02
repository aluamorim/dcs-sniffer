import sys
import platform
import time
import re
import struct
import pickle
import ctypes

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from math import cos, sin, tan
import numpy as np

from .tonedesign import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTime, QDate, QObject
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import QInputDialog, QMessageBox
from PyQt5.QtGui import *
from modules.control.adcchart import *


class ToneGenerator(QDialog, Ui_ToneGenDialog):

	signal=0
	Fs = 128000
	clock = 0;
	precision = 16; # number of bits of I/Q values
	freqs = [0]*4;
	signal_length = 0;
	fileHeader = '{TYPE: SMU-WV, 0}\n{COMMENT: I/Q=sine/cosine}\n{VECTOR MAX:0.999969482421875}\n'#{LEVEL OFFS: 6.68, 0}'
	adcChart = None
	def __init__(self, parent=None):
		super(ToneGenerator, self).__init__(parent)
		self.setupUi(self)
		self.adcChart = ADCChart(self.chartWidget, self.toolbarWidget, plotx=8, ploty=10)
		self.signal = 0
		self.controlBindings()
		self.lastUiAdjustments()


	def lastUiAdjustments(self):
		self.runFreqChange()

	def controlBindings(self):
		self.tone1Slider.valueChanged.connect(self.runTone1SliderChange)
		self.tone2Slider.valueChanged.connect(self.runTone2SliderChange)
		self.tone3Slider.valueChanged.connect(self.runTone3SliderChange)
		self.tone4Slider.valueChanged.connect(self.runTone4SliderChange)
		self.freqSlider.valueChanged.connect(self.runFreqChange)
		self.closeButton.clicked.connect(self.close)
		self.generateButton.clicked.connect(self.runGenerateFile)
		self.plotButton.clicked.connect(self.runPlot)

	def runFreqChange(self):
		self.Fs = self.freqSlider.value()*1000;
		self.freqLabel.setText("%03d kHz"%(self.Fs/1000));
	

	def runPlot(self):
		self.runFreqChange()
		
		self.signal = self.generateWaveSamples(self.freqs);
		complex_signal = self.generateComplexSignal(self.signal)
		
		self.clockLabel.setText ("%d "%(len(self.signal)));
		self.signal_length = len(self.signal);
		Ts = (1.0/self.Fs);
		timeArray = np.arange(0, (len(self.signal)*Ts),Ts) # time vector
		
		self.adcChart.updateChart(complex_signal, timeArray*1000, self.Fs);

	def runGenerateFile(self):
		file_name = QtGui.QFileDialog.getSaveFileName(self, 'Export Waveform');
		if (file_name == None or file_name==''):
			return;


		self.runPlot()
		self.signal_length = len(self.signal);
		# pickle.dump(signal)
		text = self.fileHeader + '{SAMPLES: %d}'%(self.signal_length) + "\n"
		text += "{DATE: %s}\n"%(time.strftime("%d/%m/%Y %H:%M:%S"))
		# text += "{CLOCK:1e+07}\n"
		text += "{CLOCK:%d}\n"%(self.Fs)
		# text += "{CLOCK:%d}\n"%(self.clock)
		text += "{WAVEFORM-%d: #"%((self.signal_length*4)+1)
		file = open(file_name, 'wb');
		file.write(text)
		
		re = 0;
		im = 0;
		for k in self.signal:
			#file.write(struct.pack('=I', k))
			re = (k >> 16) & 0x0000FFFF;
			im = (k) & 0x0000FFFF;
			file.write(struct.pack('=H', re))
			file.write(struct.pack('=H', im))

		file.write("}")
		file.close()

	def runTone1SliderChange(self):
		self.tone1Label.setText(str(self.tone1Slider.value()))
		self.updateFreqs()
	def runTone2SliderChange(self):
		self.tone2Label.setText(str(self.tone2Slider.value()))
		self.updateFreqs()
	def runTone3SliderChange(self):
		self.tone3Label.setText(str(self.tone3Slider.value()))
		self.updateFreqs()
	def runTone4SliderChange(self):
		self.tone4Label.setText(str(self.tone4Slider.value()))
		self.updateFreqs()

	def updateFreqs(self):
		self.freqs[0] = self.tone1Slider.value()*1000
		self.freqs[1] = self.tone2Slider.value()*1000
		self.freqs[2] = self.tone3Slider.value()*1000
		self.freqs[3] = self.tone4Slider.value()*1000

	def generateComplexSignal(self, samples):
		signal = [0]*len(samples)
		for k in range(0, len(samples)):
			re = (samples[k] >> 16) & 0x0000FFFF;
			im = (samples[k]) & 0x0000FFFF;
			
			re = ctypes.c_short(re).value
			im = ctypes.c_short(im).value

			signal[k] = complex(re, im)
		signal = np.array(signal)
		return signal

	def generateWaveSamples(self, freqs):
		Ts = 1.0/self.Fs;
		max_amp = (1<<(self.precision-1))*1.0 -1.0

		period = 1;
		self.clock = 0;
		for m in range(0, len(freqs)):
			if (freqs[m] != 0):
				if (freqs[m] > self.clock):
					self.clock = freqs[m];
		period = self.durationSpinBox.value()*1.0;
		length = int(np.ceil(period/Ts)); 
		# length = int(np.ceil(period/Ts)); 
		signal = [0]*length;
		re = [0]*length;
		im = [0]*length;		 
		
		for m in range(0, len(freqs)):
			if (freqs[m] != 0):
				for k in range(0, length):
					#re[k] += (0.25) * np.sin(2*np.pi*freqs[m]*(k*Ts))
					re[k] += 0;
					im[k] += (0.25) * np.cos(2*np.pi*freqs[m]*(k*Ts))
			
		for k in range(0, length):
			re[k] = int((re[k]*max_amp))&0x0000FFFF
			im[k] = int((im[k]*max_amp))&0x0000FFFF
			# re[k] = ctypes.c_short(int(re[k]*max_amp)).value
			# im[k] = ctypes.c_short(int(im[k]*max_amp)).value

			signal[k] = (re[k]<<self.precision) | im[k];
		
		return signal

	@staticmethod
	def getToneGenDialog(parent = None):
		dialog = ToneGenerator(parent)
		result = dialog.exec_()
		return (result == QDialog.Accepted)

if __name__ == '__main__':
	print ("> Tone generator main")

	app = QtGui.QApplication(sys.argv)
	ToneGenerator.getToneGenDialog()