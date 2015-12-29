#!/usr/bin/env python
  
import vtk
from vtk.util.colors import *
from tgdataReader import tgdataReader
import sys
  
stlineModel = tgdataReader( sys.argv[1] )

# The tube is wrapped around the generated streamline. By varying the
# radius by the inverse of vector magnitude, we are creating a tube
# whose radius is proportional to mass flux (in incompressible flow).
streamTube = vtk.vtkTubeFilter()
streamTube.SetInput( stlineModel )
streamTube.SetRadius(0.25)
streamTube.SetNumberOfSides(12)
#streamTube.SetVaryRadiusToVaryRadiusByVector()

mapStreamTube = vtk.vtkPolyDataMapper()
mapStreamTube.SetInputConnection(streamTube.GetOutputPort())
#mapStreamTube.SetScalarRange(reader.GetOutput().GetPointData().GetScalars().GetRange())
#mapStreamTube.SetScalarRange(reader.GetPolys().GetData().GetValueRange())
streamTubeActor = vtk.vtkActor()
streamTubeActor.SetMapper(mapStreamTube)
streamTubeActor.GetProperty().BackfaceCullingOn()
  
# Now create the usual graphics stuff.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
  
ren.AddActor(streamTubeActor)
ren.SetBackground(slate_grey)
  
# Here we specify a particular view.
'''
aCamera = vtk.vtkCamera()
aCamera.SetClippingRange(0.726079, 36.3039)
aCamera.SetFocalPoint(2.43584, 2.15046, 1.11104)
aCamera.SetPosition(-4.76183, -10.4426, 3.17203)
aCamera.SetViewUp(0.0511273, 0.132773, 0.989827)
aCamera.SetViewAngle(18.604)
aCamera.Zoom(1.2)
ren.SetActiveCamera(aCamera)
'''

renWin.SetSize(800, 600)
  
iren.Initialize()
renWin.Render()
iren.Start()

