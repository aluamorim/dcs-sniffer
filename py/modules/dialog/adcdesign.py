# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './py/adcdialog.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ADCDialog(object):
    def setupUi(self, ADCDialog):
        ADCDialog.setObjectName(_fromUtf8("ADCDialog"))
        ADCDialog.resize(865, 658)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/adc.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ADCDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ADCDialog)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.mainWidget = QtGui.QWidget(ADCDialog)
        self.mainWidget.setMinimumSize(QtCore.QSize(0, 200))
        self.mainWidget.setObjectName(_fromUtf8("mainWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.mainWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chartContainer = QtGui.QWidget(self.mainWidget)
        self.chartContainer.setMinimumSize(QtCore.QSize(500, 300))
        self.chartContainer.setStyleSheet(_fromUtf8("border-color: rgb(6, 6, 6);"))
        self.chartContainer.setObjectName(_fromUtf8("chartContainer"))
        self.verticalLayout = QtGui.QVBoxLayout(self.chartContainer)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chartCanvasWidget = QtGui.QWidget(self.chartContainer)
        self.chartCanvasWidget.setStyleSheet(_fromUtf8("background-color: rgb(61, 61, 61);"))
        self.chartCanvasWidget.setObjectName(_fromUtf8("chartCanvasWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.chartCanvasWidget)
        self.verticalLayout_3.setContentsMargins(6, 0, 6, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout.addWidget(self.chartCanvasWidget)
        self.toolbarCanvasContainer = QtGui.QWidget(self.chartContainer)
        self.toolbarCanvasContainer.setAutoFillBackground(False)
        self.toolbarCanvasContainer.setStyleSheet(_fromUtf8(""))
        self.toolbarCanvasContainer.setObjectName(_fromUtf8("toolbarCanvasContainer"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.toolbarCanvasContainer)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.toolbarCanvasWidget = QtGui.QWidget(self.toolbarCanvasContainer)
        self.toolbarCanvasWidget.setMinimumSize(QtCore.QSize(450, 0))
        self.toolbarCanvasWidget.setObjectName(_fromUtf8("toolbarCanvasWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.toolbarCanvasWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout_4.addWidget(self.toolbarCanvasWidget)
        self.verticalLayout.addWidget(self.toolbarCanvasContainer)
        self.horizontalLayout_2.addWidget(self.chartContainer)
        self.verticalLayout_2.addWidget(self.mainWidget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.controlWidget = QtGui.QWidget(ADCDialog)
        self.controlWidget.setObjectName(_fromUtf8("controlWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.controlWidget)
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBar = QtGui.QProgressBar(self.controlWidget)
        self.progressBar.setEnabled(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.reloadButton = QtGui.QPushButton(self.controlWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("img/reload.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reloadButton.setIcon(icon1)
        self.reloadButton.setObjectName(_fromUtf8("reloadButton"))
        self.horizontalLayout.addWidget(self.reloadButton)
        self.exportButton = QtGui.QPushButton(self.controlWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("img/matlab.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportButton.setIcon(icon2)
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.horizontalLayout.addWidget(self.exportButton)
        self.okButton = QtGui.QPushButton(self.controlWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("img/check.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okButton.setIcon(icon3)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout_2.addWidget(self.controlWidget)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.retranslateUi(ADCDialog)
        QtCore.QMetaObject.connectSlotsByName(ADCDialog)

    def retranslateUi(self, ADCDialog):
        ADCDialog.setWindowTitle(_translate("ADCDialog", "ADC Sampler", None))
        self.reloadButton.setText(_translate("ADCDialog", "Reload", None))
        self.exportButton.setText(_translate("ADCDialog", "Export", None))
        self.okButton.setText(_translate("ADCDialog", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ADCDialog = QtGui.QDialog()
    ui = Ui_ADCDialog()
    ui.setupUi(ADCDialog)
    ADCDialog.show()
    sys.exit(app.exec_())

