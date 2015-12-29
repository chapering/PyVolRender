#!/usr/bin/env python
'''
read a DTI streamline model 
Haipeng Cai @ Nov 5, 2011
'''

import os
import sys
import string
import re

import vtk

split=string.split

class tgdataReader(vtk.vtkPolyData):
	def __init__(self, fndata=None):
		#super(tgdataReader,self).__init__()

		self.allPoints = vtk.vtkPoints()
		self.allLines = vtk.vtkCellArray()

		self.fndata = fndata
		if self.fndata:
			self.load( self.fndata )

	def load(self, srcfn):
		sfh = file(srcfn, 'r')
		if None == sfh:
			raise Exception, "Failed to open file - %s." % (srcfn)

		try:
			curline = "#"
			LNo = 0
			while curline:
				curline = sfh.readline()
				LNo += 1
				curline = curline.lstrip().rstrip('\r\n')
				if len(split(curline)) == 1 and curline not in ["#","//","/*","%"]:
					break

			lnTotal = int(curline)
			lnCnt = 0
			ptCnt = 0

			while curline and lnCnt < lnTotal:
				# read line by line, in order to avoid the memory swelling by otherwise loading all lines once
				curline = sfh.readline()
				LNo += 1
				curline = curline.lstrip().rstrip('\r\n')
				if len(curline) < 1 or curline in ["#","//","/*","%"]:
					continue

				vtTotal = int(curline)
				vtCnt = 0
				startPtId = ptCnt

				while curline and vtCnt < vtTotal:
					curline = sfh.readline()
					LNo += 1
					curline = curline.lstrip().rstrip('\r\n')
					if len(curline) < 1 or curline in ["#","//","/*","%"]:
						continue

					# alway splitting a line with whitespace as the delimiter
					words = split(curline)
					if len(words) < 6: # not a vertex line
						continue

					self.allPoints.InsertNextPoint( float(words[0]), float(words[1]), float(words[2]) )
					ptCnt += 1

					vtCnt += 1

				if vtCnt < vtTotal :
					raise IOError, "Insufficient points on line No.%d, at file Line %d, aborted.\n" % (lnCnt, LNo)

				vtkln = vtk.vtkPolyLine()
				vtkln.GetPointIds().SetNumberOfIds(vtTotal)
				for id in range(0, vtTotal):
					vtkln.GetPointIds().SetId( id, id + startPtId )

				self.allLines.InsertNextCell( vtkln )
				lnCnt += 1

			if lnCnt < lnTotal:
				raise IOError, "Error encountered at file Line %d - Insufficient lines.\n" % (LNo)

			self.SetPoints( self.allPoints )
			self.SetLines ( self.allLines )

			self.fndata = srcfn 

		finally:
			sfh.close()
		
# set ts=4 tw=100 sts=4 sw=4
