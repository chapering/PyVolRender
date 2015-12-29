#!/bin/env python

import numpy, sys, vtk, wx
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
  
try:
	from transfer_function import TransferFunctionWidget
except ImportError:
	print 'You need to get the TransferFunction from: "http://www.siafoo.net/snippet/122"'
	exit(1)

'''
try:
	from wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
except ImportError:
	print 'Warning: If you are getting flickering get wxVTKRenderWindowInteractor from: "http://www.siafoo.net/snippet/312"'
	from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
'''
 
try:       
	from imageImportFromArray import vtkImageImportFromArray
except ImportError:
	print 'You need to get the updated vtkImageImportFromArray from: "http://www.siafoo.net/snippet/313" '
	exit(1)
     
class TransferGraph(wx.Dialog):
	def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                  size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
 
		wx.Dialog.__init__(self, parent, id, title, pos, size, style)
		self.mainPanel = wx.Panel(self, -1, pos)
		self.mainPanel.SetAutoLayout(True)

		# Create some CustomCheckBoxes
		self.t_function = TransferFunctionWidget(self.mainPanel, -1, "TF Tunner", size=wx.Size(400, 250))

		# Layout the items with sizers
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(self.mainPanel, 1, wx.EXPAND)

		self.SetSizer(mainSizer)
		mainSizer.Layout()
         
	def get_function(self):
		return self.t_function
 
#class imgVolRender(wxVTKRenderWindowInteractor):
class imgVolRender:
	def __init__(self, parent):
		#wxVTKRenderWindowInteractor.__init__(self, parent, -1, size=parent.GetSize())
		self.parent = parent
		self.ren = vtk.vtkRenderer()

		self.app = wx.App()
		#self.frame = wx.Frame(None, -1, 'Volume Rendering with VTK', wx.DefaultPosition, wx.Size(600, 600))
		self.frame = wx.Frame(None, -1, 'Volume Rendering with VTK', wx.Point(0,0), wx.Size(600, 600))
		self.t_graph = TransferGraph(self.frame, -1, 'TF tunner', wx.Point(parent.pos().x()+parent.width(),parent.pos().y()))

		# So we know when new values are added / changed on the tgraph
		self.t_graph.Connect(-1, -1, wx.wxEVT_COMMAND_SLIDER_UPDATED, 
						 self.OnTGraphUpdate)

		style = vtk.vtkInteractorStyleTrackballCamera()
		self.parent.m_ui.renderView.SetInteractorStyle(style)

		self.volnum = 0

	def addVol(self, data, header=None):
		pix_diag = 5.0/10.0

		img = vtkImageImportFromArray()
		img.SetArray(data)
		img.ConvertIntToUnsignedShortOn()
		'''
		Origin and Data spacing setting are essential for a normalized volume rendering of
		the DWI image volumes
		------- dawdling for a long time for addressing the problem that the volume is too thin
		and even resorted to pre-resampling of the DWI volumes
		'''
		#img.GetImport().SetDataSpacing(0.9375, 0.9375, 4.5200)
		img.GetImport().SetDataSpacing(header['pixdim'][1:4])
		#img.GetImport().SetDataOrigin(128.0, 128.0, 68.50)
		img.GetImport().SetDataOrigin( 
				header['dim'][0]*header['pixdim'][0],
				header['dim'][1]*header['pixdim'][1],
				header['dim'][2]*header['pixdim'][2])
		print img.GetDataExtent()
 
		volMapper = vtk.vtkFixedPointVolumeRayCastMapper()
		#compositeFunction = vtk.vtkFixedPointVolumeRayCastCompositeHelper()
		#compositeFunction.SetCompositeMethodToInterpolateFirst()
		#compositeFunction.SetCompositeMethodToClassifyFirst()
		#volMapper.SetVolumeRayCastFunction(compositeFunction)

		volMapper.SetSampleDistance(pix_diag / 5.0)
		volMapper.SetImageSampleDistance( 1.0 )
		volMapper.SetInputConnection( img.GetOutputPort() )

		# The property describes how the data will look
		self.volProperty = volProperty = vtk.vtkVolumeProperty()
		volProperty.SetColor(self.color_tf)
		volProperty.SetScalarOpacity(self.opacity_tf)
		volProperty.SetGradientOpacity(self.opacity_tf)
		if self.parent.lighting:
			volProperty.ShadeOn()
		#volProperty.SetInterpolationTypeToLinear()
		volProperty.SetInterpolationTypeToNearest()
		volProperty.SetScalarOpacityUnitDistance(pix_diag/5.0)

		vol = vtk.vtkVolume()
		vol.SetMapper(volMapper)
		vol.SetProperty(volProperty)

		self.ren.AddVolume(vol)

		boxWidget = vtk.vtkBoxWidget()
		boxWidget.SetInteractor(self.parent.m_ui.renderView)
		boxWidget.SetPlaceFactor(1.0)

		planes = vtk.vtkPlanes()
		def ClipVolumeRender(obj, event):
			obj.GetPlanes(planes)
			volMapper.SetClippingPlanes(planes)
         
		boxWidget.SetInput(img.GetOutput())
		boxWidget.PlaceWidget(img.GetOutput().GetBounds())
		boxWidget.InsideOutOn()
		boxWidget.AddObserver("InteractionEvent", ClipVolumeRender)

		outlineProperty = boxWidget.GetOutlineProperty()
		outlineProperty.SetRepresentationToWireframe()
		outlineProperty.SetAmbient(1.0)
		outlineProperty.SetAmbientColor(1, 1, 1)
		outlineProperty.SetLineWidth(3)

		selectedOutlineProperty = boxWidget.GetSelectedOutlineProperty()
		selectedOutlineProperty.SetRepresentationToWireframe()
		selectedOutlineProperty.SetAmbient(1.0)
		selectedOutlineProperty.SetAmbientColor(1, 0, 0)
		selectedOutlineProperty.SetLineWidth(1)

		outline = vtk.vtkOutlineFilter()
		outline.SetInputConnection(img.GetOutputPort())
		outlineMapper = vtk.vtkPolyDataMapper()
		outlineMapper.SetInputConnection(outline.GetOutputPort())
		outlineActor = vtk.vtkActor()
		outlineActor.SetMapper(outlineMapper)

		self.ren.AddActor(outlineActor)
		self.volnum += 1

	def mount(self, data_set):
		if not data_set:
			return self.ren

		# Transfer Functions
		self.opacity_tf = vtk.vtkPiecewiseFunction()
		self.color_tf = vtk.vtkColorTransferFunction()

		self.LoadVolumeData(data_set)

		self.OnTGraphUpdate(None)

		# This is the transfer graph
		self.t_graph.Show()

		return self.ren

	def OnTGraphUpdate(self, event):
		self.color_tf.RemoveAllPoints()
		self.opacity_tf.RemoveAllPoints()

		for p in self.t_graph.t_function.points:
			rgba = p.get_rgba()
			self.color_tf.AddRGBPoint(p.value, rgba[0]/255.0, 
							 rgba[1]/255.0, rgba[2]/255.0)

			self.opacity_tf.AddPoint(p.value, rgba[3])

		#self.Refresh()
		if event:
			self.parent.m_ui.renderView.repaint()

	def LoadVolumeData(self, data_set):
		if data_set.endswith('nii') or data_set.endswith('nii.gz'):
			try:
				from nifti import NiftiImage
			except ImportError:
				print "Apparently you don't have PyNIfTI installed, see http://www.siafoo.net/snippet/310 for instructions"
				exit(1)
			nim = NiftiImage(data_set)

			img_data = nim.data
			img_header = nim.header
			print nim.data.shape

			if len(nim.data.shape) == 3: # single volume
				pass
			elif len(nim.data.shape) == 4: # multiple volume
				alldata = numpy.array(nim.data[0])
				print alldata.shape
				for i in range(1, len(nim.data)):
					#self.addVol( nim.data[i] )
					#alldata = numpy.append( alldata, nim.data[i], axis=0)
					alldata = numpy.add( alldata, nim.data[i])
				print alldata.shape
				img_data = alldata
			elif len(nim.data.shape) == 5: # tensor field volume
				alldata = numpy.array(nim.data[0][0])
				print alldata.shape
				for i in range(1, len(nim.data)):
					#self.addVol( nim.data[i] )
					#alldata = numpy.append( alldata, nim.data[i][0], axis=0)
					alldata = numpy.add( alldata, nim.data[i][0])
				print alldata.shape
				img_data = alldata

		elif data_set.endswith('hdr'):
			# Use the header to figure out the shape of the data
			# then load the raw data and reshape the array 
			shape = [int(x) for x in open(data_set).readline().split()]
			img_data = numpy.frombuffer(open(data_set.replace('.hdr', '.dat'), 'rb').read(),
									numpy.uint8)\
					.reshape((shape[2], shape[1], shape[0]))
                        
		self.addVol( img_data, img_header )
		return 0
