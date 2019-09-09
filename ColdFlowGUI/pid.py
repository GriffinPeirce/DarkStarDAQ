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
        Dialog.resize(678, 386)
        self.background = QtGui.QLabel(Dialog)
        self.background.setGeometry(QtCore.QRect(-5, 6, 691, 381))
        self.background.setText(_fromUtf8(""))
        self.background.setPixmap(QtGui.QPixmap(_fromUtf8("P_ID.jpg")))
        self.background.setObjectName(_fromUtf8("background"))
        self.pressValveButton = QtGui.QPushButton(Dialog)
        self.pressValveButton.setGeometry(QtCore.QRect(0, 180, 91, 27))
        self.pressValveButton.setObjectName(_fromUtf8("pressValveButton"))
        self.ventValveButton = QtGui.QPushButton(Dialog)
        self.ventValveButton.setGeometry(QtCore.QRect(310, 130, 91, 27))
        self.ventValveButton.setObjectName(_fromUtf8("ventValveButton"))
        self.mainValveButton = QtGui.QPushButton(Dialog)
        self.mainValveButton.setGeometry(QtCore.QRect(500, 340, 91, 27))
        self.mainValveButton.setObjectName(_fromUtf8("mainValveButton"))
        self.eStopButton = QtGui.QPushButton(Dialog)
        self.eStopButton.setGeometry(QtCore.QRect(50, 40, 97, 27))
        self.eStopButton.setObjectName(_fromUtf8("eStopButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pressValveButton.setText(_translate("Dialog", "Press Valve", None))
        self.ventValveButton.setText(_translate("Dialog", "Vent Valve", None))
        self.mainValveButton.setText(_translate("Dialog", "Main Valve", None))
        self.eStopButton.setText(_translate("Dialog", "EStop", None))

