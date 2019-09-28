#!/usr/bin/env python

from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QColor
import sys
import darkstar
import numpy as np
import pylab
import time
import pyqtgraph
import json
from labjack import ljm
import collections
from collections import OrderedDict
from analogsensor import AnalogLJSensor
from digitalsensor import DigitalLJSensor

class DarkStarDaqApp(QtGui.QMainWindow, darkstar.Ui_MainWindow):
    def __init__(self, parent=None):
        super(DarkStarDaqApp, self).__init__(parent)
        self.setupUi(self)
        self.red_pen = pyqtgraph.mkPen(color=QColor(255,0,0),width=4)
        self.orange_pen = pyqtgraph.mkPen(color=QColor(255,128,0),width=4)
        self.yellow_pen = pyqtgraph.mkPen(color=QColor(255,255,0),width=4)
        self.baby_blue_pen = pyqtgraph.mkPen(color=QColor(0,255,255),width=4)
        self.pink_pen = pyqtgraph.mkPen(color=QColor(255,51,255),width=4)
        self.green_pen = pyqtgraph.mkPen(color=QColor(0,255,0),width=4)
        self.blue_pen = pyqtgraph.mkPen(color=QColor(0,255,0),width=4)
        self.purple_pen = pyqtgraph.mkPen(color=QColor(127,255,0),width=4)
        self.white_pen = pyqtgraph.mkPen(color=QColor(255,255,255),width=4)
        self.gray_pen = pyqtgraph.mkPen(color=QColor(128,128,128),width=4)
        self.loxTemperaturePlot.addLegend()
        self.loxTemperaturePlot.setLabel(axis="left",text='temperature',units='C')
        self.loxTemperaturePlot.setTitle(title="LOX Thermocouple Temperatures")

        self.analog_sensors = collections.OrderedDict()
        self.digital_sensors = collections.OrderedDict()
        self.t7readListNames = []
        self.t4scanList = []
        self.t7channelNames = []
        self.configureT7()
        self.t7dataLogIntervalMs = 50

    def updatePlots(self):
        self.loxTemperaturePlot.plot(np.random.rand(100), pen=self.red_pen, name="lox injector")
        self.loxTemperaturePlot.plot(np.random.rand(100), pen=self.orange_pen, name="lox main valve")
        self.loxTemperaturePlot.plot(np.random.rand(100), pen=self.yellow_pen, name="lox tank port")
        self.loxTemperaturePlot.plot(np.random.rand(100), pen=self.baby_blue_pen, name="lox tank body")
        self.loxTemperaturePlot.plot(np.random.rand(100), pen=self.pink_pen, name="lox tank ullage")
        self.loxTemperaturePlot.plot(np.random.rand(100), pen=self.green_pen, name="lox ullage bottle")

    def captureT7Channels(self):
        try:
            ret = ljm.eReadAddresses(self.handle, len(self.sensorsAddresses), self.sensorsAddresses, self.sensorDataTypes)

            # scaled = np.copy(np.asarray(ret))
            # scaled = scaled * self.sensorMScaling
            # scaled = scaled + self.sensorBScaling

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
            if self.dataLog.shape[0]%10 == 0: # Only save/plot once per 100 readings
                self.fig_axes[0].plot()
                if(self.logData):
                    with open(self.csvFileName, mode='a') as data_file:
                        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        print self.dataLog.shape
                        data_writer.writerows(self.dataLog)
                self.dataLog = np.empty([0,4])
        finally:
            QtCore.QTimer.singleShot(self.t7dataLogIntervalMs, self.captureT7Channels)

    def closeConnections(self):
        ljm.close(self.t7handle)

    def readT7(self):
        results = ljm.eReadNames(self.t7handle, len(self.t7readListNames), self.t7readListNames)

        for i in range(len(self.t7readListNames)):
            print("    Name - %s, value : %f" % (self.t7channelNames[i], results[i]))
    def configureT7(self):

        with open('darkstar_t7.json', 'r') as f:
          config_data = f.read()
          config_dict = json.loads(config_data.decode('utf-8'), object_pairs_hook=OrderedDict)

        for sensor in config_dict['Analog Sensors']:
            self.analog_sensors[sensor['Name']]=AnalogLJSensor(sensor['Name'], sensor['PChannel'], sensor['NChannel'], sensor['range'], sensor['slope'], sensor['intercept'],sensor['ef_index'])    
        for sensor in config_dict['Digital Sensors']:
            self.digital_sensors[sensor['Name']]=DigitalLJSensor(sensor['Name'], sensor['Address'])

        self.t7handle = ljm.openS("T7", "ANY", "ANY")
        info = ljm.getHandleInfo(self.t7handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
              "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
              (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

        # Stream Configuration
        # for sensorName, sensor in self.analog_sensors.items():
        #     if sensor is not None:
        #        self.t7readList.append(int(sensor.getPositiveChannel()))
        #        self.channelNames.append(str(sensor.getName()))
        #        print(int(sensor.getPositiveChannel()))
        #        print(str(sensor.getName()))

        # print "T7 Read list" , self.t7readList


        aWriteNames = []
        aWriteValues = []
        # print(type(analog_sensors))
        # Stream Configuration
        for sensor in self.analog_sensors:
            pChannel = str(self.analog_sensors[sensor].getPositiveChannel())
            nChannel = int(self.analog_sensors[sensor].getNegativeChannel())
            if(nChannel > 0):
                print("configuring negative channel")
                aWriteNames.append("AIN"+pChannel+"_NEGATIVE_CH")
                aWriteValues.append(nChannel)
            if(int(self.analog_sensors[sensor].getExtendedFeatures())>0):
                aWriteNames.append("AIN"+pChannel+"_EF_INDEX")
                aWriteValues.append(int(self.analog_sensors[sensor].getExtendedFeatures()))

        print "Names written" , aWriteNames
        print "Values written" , aWriteValues

        ljm.eWriteNames(self.t7handle, len(aWriteNames), aWriteNames, aWriteValues)

        results = ljm.eReadNames(self.t7handle, len(aWriteNames), aWriteNames)


        print("\neReadNames results: ")
        for i in range(len(aWriteNames)):
            print("    Name - %s, value : %d" % (aWriteNames[i], results[i]))

        self.t7readListNames = []
        self.t7channelNames = []

        # Read Configuration
        for sensorName, sensor in self.analog_sensors.items():
            if sensor is not None:
                self.t7channelNames.append(str(sensor.getName()))
                if(int(sensor.getExtendedFeatures()) > 0):
                    self.t7readListNames.append("AIN"+str(sensor.getPositiveChannel())+"_EF_READ_A")
                else:
                    self.t7readListNames.append("AIN"+str(sensor.getPositiveChannel()))


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    darkstardaq = DarkStarDaqApp()
    darkstardaq.show()
    darkstardaq.updatePlots()
    app.exec_()
    darkstardaq.closeConnections()
    print("DONE")