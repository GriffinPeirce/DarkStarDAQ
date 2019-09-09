#!/usr/bin/env python


import sys
from PyQt4 import QtCore, QtGui
from pid import Ui_Dialog
from labjack import ljm

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.mainValveState = False
        self.ventValveState = False
        self.pressValveState = False
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.mainValveButton.clicked.connect(self.actuateMainValve)
        self.ui.ventValveButton.clicked.connect(self.actuateVentValve)
        self.ui.pressValveButton.clicked.connect(self.actuatePressValve)
        self.ui.eStopButton.clicked.connect(self.eStop)

        self.handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier

        info = ljm.getHandleInfo(self.handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
            "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
            (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))


    def actuateMainValve(self):
        print "Changing state of main valve"
        self.mainValveState = not self.mainValveState
        print self.mainValveState
        ljm.eWriteAddress(self.handle, 2012, ljm.constants.UINT16, self.mainValveState)

    def actuateVentValve(self):
        print "Changing state of vent valve"
        self.ventValveState = not self.ventValveState
        print self.ventValveState
        ljm.eWriteAddress(self.handle, 2013, ljm.constants.UINT16, self.ventValveState)

    def actuatePressValve(self):
        print "Changing state of press valve"
        self.pressValveState = not self.pressValveState
        print self.pressValveState
        ljm.eWriteAddress(self.handle, 2014, ljm.constants.UINT16, self.pressValveState)

    def eStop(self):
        print "Estop activated"
        self.mainValveState = False
        self.ventValveState = False
        self.pressValveState = False
        aAddresses = [2012, 2013, 2014]
        aDataTypes = [ljm.constants.UINT16, ljm.constants.UINT16, ljm.constants.UINT16]
        aValues = [self.mainValveState, self.ventValveState, self.pressValveState]
        print aValues
        numFrames = len(aAddresses)
        ljm.eWriteAddresses(self.handle, numFrames, aAddresses, aDataTypes, aValues)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyDialog()
    myapp.show()
    sys.exit(app.exec_())