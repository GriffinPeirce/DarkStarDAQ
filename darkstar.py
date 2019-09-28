# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'darkstar.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(2005, 1009)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(800, 100))
        self.label.setMaximumSize(QtCore.QSize(800, 100))
        self.label.setAutoFillBackground(False)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("UBCR White Border.png")))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.plotLayout = QtGui.QGridLayout()
        self.plotLayout.setObjectName(_fromUtf8("plotLayout"))
        self.loxTemperaturePlot = PlotWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loxTemperaturePlot.sizePolicy().hasHeightForWidth())
        self.loxTemperaturePlot.setSizePolicy(sizePolicy)
        self.loxTemperaturePlot.setMinimumSize(QtCore.QSize(800, 200))
        self.loxTemperaturePlot.setMaximumSize(QtCore.QSize(800, 250))
        self.loxTemperaturePlot.setObjectName(_fromUtf8("loxTemperaturePlot"))
        self.plotLayout.addWidget(self.loxTemperaturePlot, 1, 0, 1, 1)
        self.fuelTemperaturePlot = PlotWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fuelTemperaturePlot.sizePolicy().hasHeightForWidth())
        self.fuelTemperaturePlot.setSizePolicy(sizePolicy)
        self.fuelTemperaturePlot.setMinimumSize(QtCore.QSize(800, 200))
        self.fuelTemperaturePlot.setMaximumSize(QtCore.QSize(800, 250))
        self.fuelTemperaturePlot.setObjectName(_fromUtf8("fuelTemperaturePlot"))
        self.plotLayout.addWidget(self.fuelTemperaturePlot, 1, 1, 1, 1)
        self.engineTemperaturePlot = PlotWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.engineTemperaturePlot.sizePolicy().hasHeightForWidth())
        self.engineTemperaturePlot.setSizePolicy(sizePolicy)
        self.engineTemperaturePlot.setMinimumSize(QtCore.QSize(800, 200))
        self.engineTemperaturePlot.setMaximumSize(QtCore.QSize(800, 250))
        self.engineTemperaturePlot.setObjectName(_fromUtf8("engineTemperaturePlot"))
        self.plotLayout.addWidget(self.engineTemperaturePlot, 2, 0, 1, 1)
        self.loxPressurePlot = PlotWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loxPressurePlot.sizePolicy().hasHeightForWidth())
        self.loxPressurePlot.setSizePolicy(sizePolicy)
        self.loxPressurePlot.setMinimumSize(QtCore.QSize(800, 200))
        self.loxPressurePlot.setMaximumSize(QtCore.QSize(800, 250))
        self.loxPressurePlot.setObjectName(_fromUtf8("loxPressurePlot"))
        self.plotLayout.addWidget(self.loxPressurePlot, 0, 0, 1, 1)
        self.enginePerformancePlot = PlotWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enginePerformancePlot.sizePolicy().hasHeightForWidth())
        self.enginePerformancePlot.setSizePolicy(sizePolicy)
        self.enginePerformancePlot.setMinimumSize(QtCore.QSize(800, 200))
        self.enginePerformancePlot.setMaximumSize(QtCore.QSize(800, 250))
        self.enginePerformancePlot.setObjectName(_fromUtf8("enginePerformancePlot"))
        self.plotLayout.addWidget(self.enginePerformancePlot, 2, 1, 1, 1)
        self.fuelPressurePlot = PlotWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fuelPressurePlot.sizePolicy().hasHeightForWidth())
        self.fuelPressurePlot.setSizePolicy(sizePolicy)
        self.fuelPressurePlot.setMinimumSize(QtCore.QSize(800, 200))
        self.fuelPressurePlot.setMaximumSize(QtCore.QSize(800, 250))
        self.fuelPressurePlot.setObjectName(_fromUtf8("fuelPressurePlot"))
        self.plotLayout.addWidget(self.fuelPressurePlot, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.plotLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

from pyqtgraph import PlotWidget
