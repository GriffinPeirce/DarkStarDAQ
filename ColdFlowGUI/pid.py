# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pid.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1140, 828)
        self.ventValveButton = QtGui.QPushButton(Dialog)
        self.ventValveButton.setGeometry(QtCore.QRect(740, 210, 31, 31))
        self.ventValveButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ventValveButton.setStyleSheet(_fromUtf8("border: none;"))
        self.ventValveButton.setText(_fromUtf8(""))
        self.ventValveButton.setCheckable(True)
        self.ventValveButton.setChecked(False)
        self.ventValveButton.setDefault(True)
        self.ventValveButton.setObjectName(_fromUtf8("ventValveButton"))
        self.mainValveButton = QtGui.QPushButton(Dialog)
        self.mainValveButton.setGeometry(QtCore.QRect(850, 400, 41, 27))
        self.mainValveButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mainValveButton.setStyleSheet(_fromUtf8("border: none;"))
        self.mainValveButton.setText(_fromUtf8(""))
        self.mainValveButton.setCheckable(True)
        self.mainValveButton.setChecked(False)
        self.mainValveButton.setDefault(False)
        self.mainValveButton.setObjectName(_fromUtf8("mainValveButton"))
        self.eStopButton = QtGui.QPushButton(Dialog)
        self.eStopButton.setGeometry(QtCore.QRect(630, 120, 41, 27))
        self.eStopButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.eStopButton.setStyleSheet(_fromUtf8("border: none;"))
        self.eStopButton.setText(_fromUtf8(""))
        self.eStopButton.setCheckable(False)
        self.eStopButton.setChecked(False)
        self.eStopButton.setObjectName(_fromUtf8("eStopButton"))
        self.outletPressureLCD = QtGui.QLCDNumber(Dialog)
        self.outletPressureLCD.setGeometry(QtCore.QRect(770, 280, 64, 23))
        self.outletPressureLCD.setObjectName(_fromUtf8("outletPressureLCD"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(760, 260, 111, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.flowMeterLCD = QtGui.QLCDNumber(Dialog)
        self.flowMeterLCD.setGeometry(QtCore.QRect(400, 290, 64, 23))
        self.flowMeterLCD.setObjectName(_fromUtf8("flowMeterLCD"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(400, 270, 111, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tankPressureLCD = QtGui.QLCDNumber(Dialog)
        self.tankPressureLCD.setGeometry(QtCore.QRect(620, 230, 64, 23))
        self.tankPressureLCD.setObjectName(_fromUtf8("tankPressureLCD"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(600, 210, 111, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(760, 120, 101, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.clock20HzLCD = QtGui.QLCDNumber(Dialog)
        self.clock20HzLCD.setGeometry(QtCore.QRect(850, 120, 64, 23))
        self.clock20HzLCD.setObjectName(_fromUtf8("clock20HzLCD"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(520, 130, 131, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(750, 410, 71, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(420, 130, 66, 17))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.logButton = QtGui.QPushButton(Dialog)
        self.logButton.setGeometry(QtCore.QRect(480, 130, 97, 27))
        self.logButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.logButton.setStyleSheet(_fromUtf8("border: none;"))
        self.logButton.setText(_fromUtf8(""))
        self.logButton.setCheckable(True)
        self.logButton.setDefault(True)
        self.logButton.setObjectName(_fromUtf8("logButton"))
        self.background = QtGui.QLabel(Dialog)
        self.background.setGeometry(QtCore.QRect(400, 110, 691, 391))
        self.background.setText(_fromUtf8(""))
        self.background.setPixmap(QtGui.QPixmap(_fromUtf8("P_ID.jpg")))
        self.background.setObjectName(_fromUtf8("background"))
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 90, 361, 551))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalPlots = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalPlots.setMargin(0)
        self.verticalPlots.setObjectName(_fromUtf8("verticalPlots"))
        self.background.raise_()
        self.ventValveButton.raise_()
        self.mainValveButton.raise_()
        self.eStopButton.raise_()
        self.outletPressureLCD.raise_()
        self.label.raise_()
        self.flowMeterLCD.raise_()
        self.label_2.raise_()
        self.tankPressureLCD.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.clock20HzLCD.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.logButton.raise_()
        self.verticalLayoutWidget.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Outlet Pressure", None))
        self.label_2.setText(_translate("Dialog", "Flow Rate", None))
        self.label_3.setText(_translate("Dialog", "Tank Pressure", None))
        self.label_4.setText(_translate("Dialog", "System Timer", None))
        self.label_5.setText(_translate("Dialog", "Emergency Stop", None))
        self.label_6.setText(_translate("Dialog", "Main Valve", None))
        self.label_7.setText(_translate("Dialog", "Log Data", None))

