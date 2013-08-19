#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtksurfacelabel.py,v $
## Language:  Python
## Date:      $Date: 2013/08/19 09:50:00 $
## Version:   $Revision: 1.0 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
##      PURPOSE.  See the above copyright notices for more information.


import sys
import vtk

import vtkvmtk
import pypes

vmtksurfacelabel = 'vmtkSurfacelabel'

class vmtkSurfacelabel(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)

        self.Surface = None
        self.CellEntityIdsArrayName = 'CellEntityIds'
        self.CellEntityIdValue = 1

        self.SetScriptName('vmtksurfacelabel')
        self.SetScriptDoc('assign an id to a surface for specification of boundary conditions before merging with other surface.')
        self.SetInputMembers([
            ['Surface','i','vtkPolyData',1,'','the input surface','vmtksurfacereader'],
            ['CellEntityIdsArrayName','entityidsarray','str',1,'','name of the array where the id of the caps have to be stored'],
            ['CellEntityIdValue','entityidvalue','int',1,'(0,)','value for entity ids'],
            ])
        self.SetOutputMembers([
            ['Surface','o','vtkPolyData',1,'','the output surface','vmtksurfacewriter'],
            ['CellEntityIdsArrayName','entityidsarray','str',1,'','name of the array where the id of the caps are stored']
            ])

    def Execute(self):

        if self.Surface == None:
            self.PrintError('Error: No input surface.')

        oldids = self.Surface.GetCellData().GetArray(self.CellEntityIdsArrayName)
        if oldids:
            self.PrintWarning("Warning: overwriting existing entity ids array.")

        ids = vtk.vtkIntArray()
        ids.SetName(self.CellEntityIdsArrayName)
        ids.SetNumberOfTuples(self.Surface.GetNumberOfCells())
        ids.FillComponent(0, self.CellEntityIdValue)
        self.Surface.GetCellData().AddArray(ids)

        if self.Surface.GetSource():
            self.Surface.GetSource().UnRegisterAllOutputs()


if __name__=='__main__':

    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()
