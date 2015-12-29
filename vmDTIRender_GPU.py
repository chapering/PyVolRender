#!/bin/env python

import vtk
import PyQt4

from PyQt4 import QtCore, QtGui
from vtk.util.colors import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from ui_testbed import Ui_TestbedWindow
from imgVolRender_GPU import imgVolRender

class MainWindow (QtGui.QMainWindow):
	def __init__(self, dataset=None, parent=None):
		super(MainWindow, self).__init__ (parent)
		self.setWindowTitle( "GUItestbed for LegiDTI v1.0" )

		self.m_ui = Ui_TestbedWindow()
		self.m_ui.setupUi( self )
		self.m_ui.statusbar.setStatusTip ( "ready to load" )
		self.m_ui.renderView.Initialize()
		self.m_ui.renderView.Start()

		self.oldsz = None
		self.imgVRender = imgVolRender(self)
		self.dataset = dataset
		self.render = None
		self.lighting = True

	def event(self, e):
		if e.type == QtCore.QEvent.KeyPress and e.text() == "l":
			self.lighting = not self.lighting
		else:
			return super(MainWindow, self).event(e)
		return True

	def resizeEvent(self, QResizeEvent):
		if not self.oldsz:
			self.oldsz = QResizeEvent.size()
		else:
			#sz = QResizeEvent.size() - QtCore.QSize(10, 3*self.m_ui.statusbar.size().height())
			sz = QResizeEvent.size()
			#osz = QResizeEvent.oldSize() 
			osz = self.oldsz

			wf = sz.width()*1.0/osz.width()
			hf = sz.height()*1.0/osz.height()

			orsz = self.m_ui.renderView.size()
			orsz.setWidth ( orsz.width() * wf )
			orsz.setHeight( orsz.height() * hf )
			self.m_ui.renderView.resize( orsz )
			'''
			orect = self.m_ui.renderView.geometry()
			rect = QtCore.QRect( orect.x() * wf, orect.y() * hf, orsz.width(), orsz.height() )
			self.m_ui.renderView.setGeometry( rect )
			'''

			self.oldsz = sz

	@QtCore.pyqtSlot()
	def on_actionLoad_triggered(self):
		#QtGui.QMessageBox.information(self, "Load...", "Load source dataset.")
		fndata = QtGui.QFileDialog.getOpenFileName(filter="All (*.*);; NIfTI (*.nii *.nii.gz)")
		print fndata
		self.dataset = str(fndata)
		self.draw()

	def draw(self):
		if self.render:
			self.m_ui.renderView.GetRenderWindow().RemoveRenderer(self.render)
		self.render = self.imgVRender.mount(self.dataset) 
		self.render.SetBackground(slate_grey)
		self.m_ui.renderView.GetRenderWindow().AddRenderer(self.render)
		print "Numer of Volumes in the render: %d" % (self.render.VisibleVolumeCount()/2)

	def show(self):
		super(MainWindow, self).show()
		self.draw()

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print >>sys.stderr, "No data provided, bailed out."
		sys.exit(1)

	app = QtGui.QApplication( sys.argv )

	win = MainWindow(sys.argv[1])
	win.show()

	ret = app.exec_()
	sys.exit( ret  )
	

#/* sts=8 ts=8 sw=80 tw=8 */
