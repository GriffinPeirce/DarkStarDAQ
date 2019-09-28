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
        self.logData = False
        self.ventValveAddress = 2016 #CIO0
        self.mainValveAddress = 2017 #CIO1
        self.flowMeterAddress = 6 # AIN3
        self.tankPressureAddress = 2 # AIN1
        self.outletPressureAddress = 0 # AIN0
        self.clock40MHz = 61520
        self.clock20Hz = 61522
        self.actuatorsAddresses = [self.ventValveAddress, self.mainValveAddress]
        self.actuatorsDataTypes = [ljm.constants.UINT16, ljm.constants.UINT16]
        self.sensorsAddresses = [self.clock40MHz, self.tankPressureAddress, self.outletPressureAddress, self.flowMeterAddress]
        self.sensorDataTypes = [ljm.constants.UINT32, ljm.constants.FLOAT32, ljm.constants.FLOAT32, ljm.constants.FLOAT32]
        self.sensorMScaling = np.array([1, 125, 125, 1/273.5])
        self.sensorBScaling = np.array([0, -62.5, -62.5, 0])
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.openValveIcon = QtGui.QIcon("open.png")
        self.closedValveIcon = QtGui.QIcon("closed.png")
        self.ui.logButton.setIcon(self.closedValveIcon)
        self.ui.eStopButton.clicked.connect(self.eStop)
        self.ui.logButton.clicked.connect(self.log)
        self.dataLog = np.empty([0,4])
        self.tankPressure = 0
        self.outletPressure = 0
        self.flowRate = 0
        self.dataLogPacketSize = 1000
        self.actuatorsUpdateIntervalMs = 100
        self.lcdUpdateIntervalMs = 300
        self.dataLogIntervalMs = 1
        self.fig, self.fig_axes = plt.subplots(ncols=1, nrows=3)
        self.tankPressureRingBuffer = np.zeros(200)
        self.outletPressureRingBuffer = np.zeros(200)
        self.flowRateRingBuffer = np.zeros(200)
        self.addmpl(self.fig)
        self.csvFile = None
        self.csvFileName = ""
        # self.ui.chartLayout.addWidget(self.toolbar)
        self.handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier

        info = ljm.getHandleInfo(self.handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
            "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
            (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

        ret = ljm.eReadAddresses(self.handle, len(self.actuatorsAddresses), self.actuatorsAddresses, self.actuatorsDataTypes)
        self.ventValveState = bool(ret[0])
        self.mainValveState = bool(ret[1])

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
                data_writer.writerow(['40MHz Clock', 'Tank Pressure', 'Outlet Pressure', 'Flow Rate Current', 'Flow Rate Raw', 'Vent Valve' , 'Main Valve'])
        if self.ui.logButton.isChecked():
            self.ui.logButton.setIcon(self.openValveIcon)
        else:
            self.ui.logButton.setIcon(self.closedValveIcon)

    def captureChannels(self):
        try:
            ret = ljm.eReadAddresses(self.handle, len(self.sensorsAddresses), self.sensorsAddresses, self.sensorDataTypes)

            scaled = np.copy(np.asarray(ret))
            scaled = scaled * self.sensorMScaling
            scaled = scaled + self.sensorBScaling

            self.flowRate = scaled[3]
            self.flowRateRingBuffer = np.roll(self.flowRateRingBuffer,-1)
            self.flowRateRingBuffer[-1] = self.flowRate

            self.tankPressure = scaled[1]
            self.tankPressureRingBuffer = np.roll(self.tankPressureRingBuffer,-1)
            self.tankPressureRingBuffer[-1] = self.tankPressure

            self.outletPressure = scaled[2]
            self.outletPressureRingBuffer = np.roll(self.outletPressureRingBuffer,-1)
            self.outletPressureRingBuffer[-1] = self.outletPressure

            scaled = np.append(scaled, np.asarray([ret[3], self.ventValveState, self.mainValveState]))

            if self.dataLog.shape[0] == 0:
                self.dataLog = np.copy(scaled)
            else:
                self.dataLog = np.vstack((self.dataLog, scaled))
            if self.dataLog.shape[0]%self.dataLogPacketSize == 0: # Only save/plot once per 1000 readings
                self.fig_axes[0].plot()
                if(self.logData):
                    with open(self.csvFileName, mode='a') as data_file:
                        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        print self.dataLog.shape
                        data_writer.writerows(self.dataLog)
                self.dataLog = np.empty([0,4])
        finally:
            QtCore.QTimer.singleShot(self.dataLogIntervalMs, self.captureChannels)

    def writeActuators(self):
        try:
            if self.ui.mainValveButton.isChecked():
                self.ui.mainValveButton.setIcon(self.openValveIcon)
                self.mainValveState = True
            else:
                self.ui.mainValveButton.setIcon(self.closedValveIcon)
                self.mainValveState = False

            if self.ui.ventValveButton.isChecked():
                self.ui.ventValveButton.setIcon(self.openValveIcon)
                self.ventValveState = True
            else:
                self.ui.ventValveButton.setIcon(self.closedValveIcon)
                self.ventValveState = False

            # ljm.eWriteAddress(self.handle, self.ventValveAddress, ljm.constants.UINT16, not self.ventValveState)
            ljm.eWriteAddresses(self.handle, 
                                len(self.actuatorsAddresses), 
                                self.actuatorsAddresses, 
                                self.actuatorsDataTypes, 
                                [not self.ventValveState, not self.mainValveState])
        finally:
            QtCore.QTimer.singleShot(self.actuatorsUpdateIntervalMs, self.writeActuators)

    def renderReadings(self):
        try:
            self.ui.flowMeterLCD.display(self.flowRate)
            self.ui.tankPressureLCD.display(self.tankPressure)
            self.ui.outletPressureLCD.display(self.outletPressure)
            self.fig_axes[0].clear()
            self.fig_axes[0].plot(self.tankPressureRingBuffer)
            self.fig_axes[0].set_xticks([])
            self.fig_axes[0].set_ylim(0,np.amax(self.tankPressureRingBuffer))
            self.fig_axes[0].set_ylabel('PSI')
            self.fig_axes[0].set_title('Tank Pressure')

            self.fig_axes[1].clear()
            self.fig_axes[1].plot(self.outletPressureRingBuffer)
            self.fig_axes[1].set_xticks([])
            self.fig_axes[1].set_ylim(0,np.amax(self.outletPressureRingBuffer))
            self.fig_axes[1].set_ylabel('PSI')
            self.fig_axes[1].set_title('Outlet Pressure')
            
            self.fig_axes[2].clear()
            self.fig_axes[2].plot(self.flowRateRingBuffer)
            self.fig_axes[2].set_xticks([])
            self.fig_axes[2].set_ylim(0,np.amax(self.flowRateRingBuffer))
            self.fig_axes[2].set_ylabel('Kg s')
            self.fig_axes[2].set_title('Mass Flow Rate')
            self.canvas.draw()

        finally:
            QtCore.QTimer.singleShot(self.lcdUpdateIntervalMs, self.renderReadings)

    def actuateMainValve(self):
        print "Changing state of main valve"
        self.mainValveState = not self.mainValveState
        print self.mainValveState
        # ljm.eWriteAddress(self.handle, self.mainValveAddress, ljm.constants.UINT16, not self.mainValveState)

    def actuateVentValve(self):
        print "Changing state of vent valve"
        self.ventValveState = not self.ventValveState
        print self.ventValveState
        # ljm.eWriteAddress(self.handle, self.ventValveAddress, ljm.constants.UINT16, not self.ventValveState)

    def eStop(self):
        print "Estop activated"
        self.mainValveState = False
        self.ventValveState = False

        # self.ui.ventValveButton.setIcon(self.closedValveIcon)
        # self.ui.mainValveButton.setIcon(self.closedValveIcon)
        self.ui.ventValveButton.setChecked(False)
        self.ui.mainValveButton.setChecked(False)

        # aValues = [False, False]
        # ljm.eWriteAddresses(self.handle, len(aValues), self.actuatorsAddresses, self.actuatorsDataTypes, aValues)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyDialog()
    myapp.captureChannels()
    myapp.writeActuators()
    myapp.renderReadings()
    myapp.show()
    sys.exit(app.exec_())