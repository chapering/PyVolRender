# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testbed.ui'
#
# Created: Wed Nov  2 16:24:22 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TestbedWindow(object):
    def setupUi(self, TestbedWindow):
        TestbedWindow.setObjectName(_fromUtf8("TestbedWindow"))
        TestbedWindow.resize(789, 590)
        TestbedWindow.setWindowTitle(QtGui.QApplication.translate("TestbedWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(TestbedWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.renderView = QVTKRenderWindowInteractor(self.centralwidget)
        self.renderView.setGeometry(QtCore.QRect(0, 0, 781, 541))
        self.renderView.setObjectName(_fromUtf8("renderView"))

        TestbedWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TestbedWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuData = QtGui.QMenu(self.menubar)
        self.menuData.setTitle(QtGui.QApplication.translate("TestbedWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.menuData.setObjectName(_fromUtf8("menuData"))
        TestbedWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TestbedWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TestbedWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtGui.QAction(TestbedWindow)
        self.actionLoad.setCheckable(False)
        self.actionLoad.setText(QtGui.QApplication.translate("TestbedWindow", "Load...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setToolTip(QtGui.QApplication.translate("TestbedWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Load dataset</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setShortcut(QtGui.QApplication.translate("TestbedWindow", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.menuData.addAction(self.actionLoad)
        self.menubar.addAction(self.menuData.menuAction())

        self.retranslateUi(TestbedWindow)
        QtCore.QMetaObject.connectSlotsByName(TestbedWindow)

    def retranslateUi(self, TestbedWindow):
        pass

