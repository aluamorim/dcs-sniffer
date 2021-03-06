# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './py/waveformgen.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ToneGenDialog(object):
    def setupUi(self, ToneGenDialog):
        ToneGenDialog.setObjectName("ToneGenDialog")
        ToneGenDialog.resize(744, 479)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/sine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ToneGenDialog.setWindowIcon(icon)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ToneGenDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.line_3 = QtWidgets.QFrame(ToneGenDialog)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.mainWidget = QtWidgets.QWidget(ToneGenDialog)
        self.mainWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.mainWidget.setObjectName("mainWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.mainWidget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_10 = QtWidgets.QWidget(self.mainWidget)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.tabWidget = QtWidgets.QTabWidget(self.widget_10)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.configWidget = QtWidgets.QWidget(self.tab)
        self.configWidget.setStyleSheet("border-color: rgb(61, 61, 61);")
        self.configWidget.setObjectName("configWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.configWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_9 = QtWidgets.QWidget(self.configWidget)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_8 = QtWidgets.QWidget(self.widget_9)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_10 = QtWidgets.QLabel(self.widget_8)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        self.freqSlider = QtWidgets.QSpinBox(self.widget_8)
        self.freqSlider.setMinimum(1)
        self.freqSlider.setMaximum(256)
        self.freqSlider.setProperty("value", 128)
        self.freqSlider.setObjectName("freqSlider")
        self.horizontalLayout_8.addWidget(self.freqSlider)
        self.freqLabel = QtWidgets.QLabel(self.widget_8)
        self.freqLabel.setObjectName("freqLabel")
        self.horizontalLayout_8.addWidget(self.freqLabel)
        self.label_9 = QtWidgets.QLabel(self.widget_8)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.durationSpinBox = QtWidgets.QDoubleSpinBox(self.widget_8)
        self.durationSpinBox.setDecimals(3)
        self.durationSpinBox.setMinimum(0.001)
        self.durationSpinBox.setSingleStep(0.1)
        self.durationSpinBox.setProperty("value", 1.0)
        self.durationSpinBox.setObjectName("durationSpinBox")
        self.horizontalLayout_8.addWidget(self.durationSpinBox)
        self.label_12 = QtWidgets.QLabel(self.widget_8)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_6.addWidget(self.widget_8)
        self.widget_6 = QtWidgets.QWidget(self.widget_9)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_6.addWidget(self.widget_6)
        self.verticalLayout.addWidget(self.widget_9)
        self.label_13 = QtWidgets.QLabel(self.configWidget)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.widget_2 = QtWidgets.QWidget(self.configWidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.tone1Slider = QtWidgets.QSlider(self.widget_2)
        self.tone1Slider.setMaximum(32)
        self.tone1Slider.setOrientation(QtCore.Qt.Horizontal)
        self.tone1Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.tone1Slider.setObjectName("tone1Slider")
        self.horizontalLayout.addWidget(self.tone1Slider)
        self.tone1Label = QtWidgets.QLabel(self.widget_2)
        self.tone1Label.setObjectName("tone1Label")
        self.horizontalLayout.addWidget(self.tone1Label)
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.configWidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.tone2Slider = QtWidgets.QSlider(self.widget_3)
        self.tone2Slider.setMaximum(32)
        self.tone2Slider.setOrientation(QtCore.Qt.Horizontal)
        self.tone2Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.tone2Slider.setObjectName("tone2Slider")
        self.horizontalLayout_2.addWidget(self.tone2Slider)
        self.tone2Label = QtWidgets.QLabel(self.widget_3)
        self.tone2Label.setObjectName("tone2Label")
        self.horizontalLayout_2.addWidget(self.tone2Label)
        self.label_4 = QtWidgets.QLabel(self.widget_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.configWidget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.widget_4)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.tone3Slider = QtWidgets.QSlider(self.widget_4)
        self.tone3Slider.setMaximum(32)
        self.tone3Slider.setOrientation(QtCore.Qt.Horizontal)
        self.tone3Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.tone3Slider.setObjectName("tone3Slider")
        self.horizontalLayout_3.addWidget(self.tone3Slider)
        self.tone3Label = QtWidgets.QLabel(self.widget_4)
        self.tone3Label.setObjectName("tone3Label")
        self.horizontalLayout_3.addWidget(self.tone3Label)
        self.label_6 = QtWidgets.QLabel(self.widget_4)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self.configWidget)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.widget_5)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.tone4Slider = QtWidgets.QSlider(self.widget_5)
        self.tone4Slider.setMaximum(32)
        self.tone4Slider.setOrientation(QtCore.Qt.Horizontal)
        self.tone4Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.tone4Slider.setObjectName("tone4Slider")
        self.horizontalLayout_4.addWidget(self.tone4Slider)
        self.tone4Label = QtWidgets.QLabel(self.widget_5)
        self.tone4Label.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tone4Label.setObjectName("tone4Label")
        self.horizontalLayout_4.addWidget(self.tone4Label)
        self.label_8 = QtWidgets.QLabel(self.widget_5)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.verticalLayout.addWidget(self.widget_5)
        self.plotButton = QtWidgets.QPushButton(self.configWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/chart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.plotButton.setIcon(icon1)
        self.plotButton.setObjectName("plotButton")
        self.verticalLayout.addWidget(self.plotButton)
        self.widget = QtWidgets.QWidget(self.configWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_7 = QtWidgets.QWidget(self.widget)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.generateButton = QtWidgets.QPushButton(self.widget_7)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.generateButton.setIcon(icon2)
        self.generateButton.setObjectName("generateButton")
        self.horizontalLayout_6.addWidget(self.generateButton)
        self.closeButton = QtWidgets.QPushButton(self.widget_7)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon3)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_6.addWidget(self.closeButton)
        self.verticalLayout_2.addWidget(self.widget_7)
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout_8.addWidget(self.configWidget)
        self.widget_11 = QtWidgets.QWidget(self.tab)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_11 = QtWidgets.QLabel(self.widget_11)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_9.addWidget(self.label_11)
        self.clockLabel = QtWidgets.QLabel(self.widget_11)
        self.clockLabel.setObjectName("clockLabel")
        self.horizontalLayout_9.addWidget(self.clockLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.verticalLayout_8.addWidget(self.widget_11)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_9.addWidget(self.tabWidget)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.horizontalLayout_5.addWidget(self.widget_10)
        self.line = QtWidgets.QFrame(self.mainWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        self.plotWidget = QtWidgets.QWidget(self.mainWidget)
        self.plotWidget.setMinimumSize(QtCore.QSize(400, 400))
        self.plotWidget.setObjectName("plotWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.plotWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.chartWidget = QtWidgets.QWidget(self.plotWidget)
        self.chartWidget.setMinimumSize(QtCore.QSize(0, 350))
        self.chartWidget.setStyleSheet("background-color: rgb(61, 61, 61);")
        self.chartWidget.setObjectName("chartWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.chartWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4.addWidget(self.chartWidget)
        self.toolbarWidget = QtWidgets.QWidget(self.plotWidget)
        self.toolbarWidget.setObjectName("toolbarWidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.toolbarWidget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_4.addWidget(self.toolbarWidget)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_5.addWidget(self.plotWidget)
        self.verticalLayout_3.addWidget(self.mainWidget)
        self.line_4 = QtWidgets.QFrame(ToneGenDialog)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_3.addWidget(self.line_4)

        self.retranslateUi(ToneGenDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ToneGenDialog)

    def retranslateUi(self, ToneGenDialog):
        _translate = QtCore.QCoreApplication.translate
        ToneGenDialog.setWindowTitle(_translate("ToneGenDialog", "Simple Waveform Generator"))
        self.label_10.setText(_translate("ToneGenDialog", "Sample Rate:"))
        self.freqLabel.setText(_translate("ToneGenDialog", "KHz"))
        self.label_9.setText(_translate("ToneGenDialog", "Duraton:"))
        self.label_12.setText(_translate("ToneGenDialog", "s"))
        self.label_13.setText(_translate("ToneGenDialog", "SIGNAL FREQUENCIES:"))
        self.label.setText(_translate("ToneGenDialog", "Tone 1:"))
        self.tone1Label.setText(_translate("ToneGenDialog", "0"))
        self.label_2.setText(_translate("ToneGenDialog", "KHz"))
        self.label_3.setText(_translate("ToneGenDialog", "Tone 2:"))
        self.tone2Label.setText(_translate("ToneGenDialog", "0"))
        self.label_4.setText(_translate("ToneGenDialog", "KHz"))
        self.label_5.setText(_translate("ToneGenDialog", "Tone 3:"))
        self.tone3Label.setText(_translate("ToneGenDialog", "0"))
        self.label_6.setText(_translate("ToneGenDialog", "KHz"))
        self.label_7.setText(_translate("ToneGenDialog", "Tone 4:"))
        self.tone4Label.setText(_translate("ToneGenDialog", "0"))
        self.label_8.setText(_translate("ToneGenDialog", "KHz"))
        self.plotButton.setText(_translate("ToneGenDialog", "Plot"))
        self.generateButton.setText(_translate("ToneGenDialog", "Save Waveform"))
        self.closeButton.setText(_translate("ToneGenDialog", "Close"))
        self.label_11.setText(_translate("ToneGenDialog", "Number of Samples:"))
        self.clockLabel.setText(_translate("ToneGenDialog", "0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ToneGenDialog", "CONFIG:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ToneGenDialog = QtWidgets.QDialog()
    ui = Ui_ToneGenDialog()
    ui.setupUi(ToneGenDialog)
    ToneGenDialog.show()
    sys.exit(app.exec_())

