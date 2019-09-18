#!/usr/bin/env python


import sys
from PyQt4 import QtCore, QtGui
from pid import Ui_Dialog
from labjack import ljm
import numpy as np
from datetime import datetime
import csv

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.mainValveState = False
        self.ventValveState = False
        self.logData = False
        self.mainValveAddress = 2016 #CIO1
        self.ventValveAddress = 2017 #CIO0
        self.flowMeterAddress = 6 # AIN3
        self.tankPressureAddress = 2 # AIN1
        self.outletPressureAddress = 0 # AIN0
        self.clock20Hz = 61522
        self.actuatorsAddresses = [self.mainValveAddress, self.ventValveAddress]
        self.actuatorsDataTypes = [ljm.constants.UINT16, ljm.constants.UINT16]
        self.sensorsAddresses = [self.clock20Hz, self.flowMeterAddress, self.tankPressureAddress, self.outletPressureAddress]
        self.sensorDataTypes = [ljm.constants.UINT32, ljm.constants.FLOAT32, ljm.constants.FLOAT32, ljm.constants.FLOAT32]
        self.sensorMScaling = np.array([1,1/187.7,125,125])
        print self.sensorMScaling
        self.sensorBScaling = np.array([0,0,-62.5,-62.5])
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.openValveIcon = QtGui.QIcon("open.png")
        self.closedValveIcon = QtGui.QIcon("closed.png")
        self.ui.ventValveButton.setIcon(self.closedValveIcon)
        self.ui.mainValveButton.setIcon(self.closedValveIcon)
        self.ui.logButton.setIcon(self.closedValveIcon)
        self.ui.eStopButton.setIcon(self.openValveIcon)
        self.ui.mainValveButton.clicked.connect(self.actuateMainValve)
        self.ui.ventValveButton.clicked.connect(self.actuateVentValve)
        self.ui.eStopButton.clicked.connect(self.eStop)
        self.ui.logButton.clicked.connect(self.log)
        self.dataLog = np.empty([0,4])
        self.dataLogPacketSize = 100
        self.fig1, self.f1_axes = plt.subplots(ncols=1, nrows=3)
        self.f1_axes[0].plot(np.random.rand(100))
        self.f1_axes[1].plot(np.random.rand(100))
        self.f1_axes[2].plot(np.random.rand(100))
        self.addmpl(self.fig1)
        self.csvFile = None
        self.csvFileName = ""
        # self.ui.chartLayout.addWidget(self.toolbar)
        self.handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier

        info = ljm.getHandleInfo(self.handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
            "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
            (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.ui.verticalPlots.addWidget(self.canvas)
        self.canvas.draw()

    def log(self):
        self.logData = not self.logData
        if not self.logData:
            print "Disabled data logging"
        elif self.logData:
            print "Enabled data logging"
            self.csvFileName = 'coldflow_'+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.csv'
            with open(self.csvFileName, mode='w') as data_file:
                data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow(['20Hz Clock', 'Tank Pressure', 'Outlet Pressure', 'Flow Rate'])
        if self.ui.logButton.isChecked():
            self.ui.logButton.setIcon(self.openValveIcon)
        else:
            self.ui.logButton.setIcon(self.closedValveIcon)

    def captureChannels(self):
        try:
            ret = ljm.eReadAddresses(self.handle, len(self.sensorsAddresses), self.sensorsAddresses, self.sensorDataTypes)
            self.ui.clock20HzLCD.display(ret[0])
            self.ui.flowMeterLCD.display(ret[1])
            self.ui.tankPressureLCD.display(ret[2])
            self.ui.outletPressureLCD.display(ret[3])
            scaled = np.copy(np.asarray(ret))
            scaled = scaled * self.sensorMScaling
            scaled = scaled + self.sensorBScaling

            if self.dataLog.shape[0] == 0:
            	self.dataLog = np.copy(scaled)
            else:
            	self.dataLog = np.vstack((self.dataLog, scaled))
            if self.dataLog.shape[0]%10 == 0: # Only save/plot once per 100 readings
                if(self.logData):
                    with open(self.csvFileName, mode='a') as data_file:
                        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        print self.dataLog.shape
                        data_writer.writerows(self.dataLog)
                self.dataLog = np.empty([0,4])
        finally:
            QtCore.QTimer.singleShot(1000, self.captureChannels)

    def writeActuators(self):
    	try:
    		# ljm.eWriteAddress(self.handle, self.ventValveAddress, ljm.constants.UINT16, not self.ventValveState)
    		ljm.eWriteAddresses(self.handle, 
    							len(self.actuatorsAddresses), 
    							self.actuatorsAddresses, 
    							self.actuatorsDataTypes, 
    							[not self.mainValveState, not self.ventValveState])
    	finally:
    		QtCore.QTimer.singleShot(100, self.writeActuators)

    def actuateMainValve(self):
        print "Changing state of main valve"
        self.mainValveState = not self.mainValveState
        print self.mainValveState
        # ljm.eWriteAddress(self.handle, self.mainValveAddress, ljm.constants.UINT16, not self.mainValveState)
        if self.ui.mainValveButton.isChecked():
            self.ui.mainValveButton.setIcon(self.openValveIcon)
        else:
            self.ui.mainValveButton.setIcon(self.closedValveIcon)

    def actuateVentValve(self):
        print "Changing state of vent valve"
        self.ventValveState = not self.ventValveState
        print self.ventValveState
        # ljm.eWriteAddress(self.handle, self.ventValveAddress, ljm.constants.UINT16, not self.ventValveState)
        if self.ui.ventValveButton.isChecked():
            self.ui.ventValveButton.setIcon(self.openValveIcon)
        else:
            self.ui.ventValveButton.setIcon(self.closedValveIcon)

    def eStop(self):
        print "Estop activated"
        self.mainValveState = False
        self.ventValveState = False
        # aValues = [False, False]
        # ljm.eWriteAddresses(self.handle, len(aValues), self.actuatorsAddresses, self.actuatorsDataTypes, aValues)
        if self.ui.eStopButton.isChecked():
            self.ui.eStopButton.setIcon(self.closedValveIcon)
        else:
            self.ui.eStopButton.setIcon(self.openValveIcon)
            self.ui.ventValveButton.setIcon(self.closedValveIcon)
            self.ui.mainValveButton.setIcon(self.closedValveIcon)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyDialog()
    myapp.captureChannels()
    myapp.writeActuators()
    myapp.show()
    sys.exit(app.exec_())