#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkboundarylayer.py,v $
## Language:  Python
## Date:      $Date: 2005/09/14 09:49:59 $
## Version:   $Revision: 1.6 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.

from __future__ import absolute_import #NEEDS TO STAY AS TOP LEVEL MODULE FOR Py2-3 COMPATIBILITY
import vtk
from vmtk import vtkvmtk
import sys

from vmtk import pypes


class vmtkBoundaryLayer(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)

        self.Mesh = None
        self.InnerSurfaceMesh = None
        
        self.WarpVectorsArrayName = ''
        self.ThicknessArrayName = ''
        self.CellEntityIdsArrayName = ''

        self.Thickness = 1.0
        self.ThicknessRatio = 0.1
        self.MaximumThickness = 1E10

        self.NumberOfSubLayers = 1
        self.SubLayerRatio = 1.0

        self.NumberOfSubsteps = 2000
        self.Relaxation = 0.01
        self.LocalCorrectionFactor = 0.45

        self.UseWarpVectorMagnitudeAsThickness = 0;
        self.ConstantThickness = 0
        self.IncludeSurfaceCells = 1
        self.IncludeSidewallCells = 1
        self.NegateWarpVectors = 0

        self.CellEntityIdsArrayName = 'CellEntityIds'
        self.InnerSurfaceCellEntityId = 0
        self.OuterSurfaceCellEntityId = 0
        self.SidewallCellEntityId = 0
        self.VolumeCellEntityId = 0

        self.SetScriptName('vmtkboundarylayer')
        self.SetScriptDoc('create a prismatic boundary layer from a surface mesh and a set of vectors defined on the nodes')
        self.SetInputMembers([
            ['Mesh','i','vtkUnstructuredGrid',1,'','the input mesh','vmtkmeshreader'],
            ['WarpVectorsArrayName','warpvectorsarray','str',1,'','name of the array where warp vectors are stored'],
            ['ThicknessArrayName','thicknessarray','str',1,'','name of the array where scalars defining boundary layer thickness are stored'],
            ['CellEntityIdsArrayName','entityidsarray','str',1],
            ['Thickness','thickness','float',1,'','value of constant boundary layer thickness'],
            ['ThicknessRatio','thicknessratio','float',1,'(0.0,)','multiplying factor for boundary layer thickness'],
            ['MaximumThickness','maximumthickness','float',1,'','maximum allowed value for boundary layer thickness'],
            ['NumberOfSubLayers','sublayers','int',1,'(0,)','number of sublayers which the boundary layer has to be made of'],
            ['NumberOfSubsteps','substeps','int',1,'(0,)','number of substeps for smoothly propagating the boundary layer'],
            ['Relaxation','relaxation','float',1,'(0.0,)','relaxation factor for the evolution of the inner surface'],
            ['LocalCorrectionFactor','localcorrection','float',1,'(0.0,)','amount of correction to apply to warp vectors during local untangling'],
            ['InnerSurfaceCellEntityId','innersurfaceentityid','int',1,'(0,)','cell entity id assigned to the inner warped surface'],
            ['OuterSurfaceCellEntityId','outersurfaceentityid','int',1,'(0,)','cell entity id assigned to the original outer surface'],
            ['SidewallCellEntityId','sidewallentityid','int',1,'(0,)','cell entity id assigned to the sidewall elements generated by sweeping'],
            ['VolumeCellEntityId','volumeentityid','int',1,'(0,)','cell entity id assigned to volume elements of the boundary layer'],
            ['SubLayerRatio','sublayerratio','float',1,'(0.0,)','ratio between the thickness of two successive boundary layers'],
            ['UseWarpVectorMagnitudeAsThickness','warpvectormagnitudeasthickness','bool',1,'','compute boundary layer thickness as the norm of warp vectors'],
            ['ConstantThickness','constantthickness','bool',1,'','toggle constant boundary layer thickness'],
            ['IncludeSurfaceCells','includesurfacecells','bool',1,'','include inner and outer surface cells in the output mesh'],
            ['IncludeSidewallCells','includesidewallcells','bool',1,'','include surface cells generated by sweeping the input surface boundaries in the output mesh'],
            ['NegateWarpVectors','negatewarpvectors','bool',1,'','flip the orientation of warp vectors']
            ])
        self.SetOutputMembers([
            ['Mesh','o','vtkUnstructuredGrid',1,'','the output mesh','vmtkmeshwriter'],
            ['InnerSurfaceMesh','oinner','vtkUnstructuredGrid',1,'','the output inner surface mesh','vmtkmeshwriter']
            ])

    def Execute(self):

        if self.Mesh == None:
            self.PrintError('Error: No input mesh.')

        boundaryLayerGenerator = vtkvmtk.vtkvmtkBoundaryLayerGenerator()
        boundaryLayerGenerator.SetInputData(self.Mesh)
        boundaryLayerGenerator.SetWarpVectorsArrayName(self.WarpVectorsArrayName)
        boundaryLayerGenerator.SetLayerThickness(self.Thickness)
        boundaryLayerGenerator.SetLayerThicknessArrayName(self.ThicknessArrayName)
        boundaryLayerGenerator.SetLayerThicknessRatio(self.ThicknessRatio)
        boundaryLayerGenerator.SetMaximumLayerThickness(self.MaximumThickness)
        boundaryLayerGenerator.SetNumberOfSubLayers(self.NumberOfSubLayers)
        boundaryLayerGenerator.SetNumberOfSubsteps(self.NumberOfSubsteps)
        boundaryLayerGenerator.SetRelaxation(self.Relaxation)
        boundaryLayerGenerator.SetLocalCorrectionFactor(self.LocalCorrectionFactor)
        boundaryLayerGenerator.SetSubLayerRatio(self.SubLayerRatio)
        boundaryLayerGenerator.SetConstantThickness(self.ConstantThickness)
        boundaryLayerGenerator.SetUseWarpVectorMagnitudeAsThickness(self.UseWarpVectorMagnitudeAsThickness)
        boundaryLayerGenerator.SetIncludeSurfaceCells(self.IncludeSurfaceCells)
        boundaryLayerGenerator.SetIncludeSidewallCells(self.IncludeSidewallCells)
        boundaryLayerGenerator.SetNegateWarpVectors(self.NegateWarpVectors)
        boundaryLayerGenerator.SetCellEntityIdsArrayName(self.CellEntityIdsArrayName)
        boundaryLayerGenerator.SetInnerSurfaceCellEntityId(self.InnerSurfaceCellEntityId)
        boundaryLayerGenerator.SetOuterSurfaceCellEntityId(self.OuterSurfaceCellEntityId)
        boundaryLayerGenerator.SetSidewallCellEntityId(self.SidewallCellEntityId)
        boundaryLayerGenerator.SetVolumeCellEntityId(self.VolumeCellEntityId)
        boundaryLayerGenerator.Update()
        
        self.Mesh = boundaryLayerGenerator.GetOutput()
        self.InnerSurfaceMesh = boundaryLayerGenerator.GetInnerSurface()



if __name__=='__main__':

    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()
