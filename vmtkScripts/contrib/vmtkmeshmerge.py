#!/usr/bin/env python

import sys
import math
import numpy
import vtk
from vmtk import pypes
from vmtk import vmtkscripts
from vmtk import vtkvmtk

vmtkmeshmerge = 'vmtkMeshMerge'

class vmtkMeshMerge(pypes.pypeScript):
    def __init__(self):
        pypes.pypeScript.__init__(self)

        self.SetScriptName("vmtkmeshmerge")
        self.SetScriptDoc('Merge two or three meshes into one.')

        self.Mesh = None
        self.CellEntityIdsArrayName = "CellEntityIds"

        self.max_meshes = 7
        members = []
        for i in range(1, self.max_meshes+1):
            setattr(self, 'Mesh%d'%i, None)
            members.append(['Mesh%d'%i, 'mesh%d'%i, 'vtkUnstructuredGrid', 1, '',
                 'mesh number %d to merge'%i, 'vmtkmeshreader'])
        for i in range(1, self.max_meshes+1):
            setattr(self, 'CellEntityIdOffset%d'%i, None)
            members.append(['CellEntityIdOffset%d'%i, 'cellentityidoffset%d'%i, 'int', 1, '',
                 'offset added to cell entity ids from mesh%d'%i, ''])

        # Member info: name, cmdlinename, typename, num, default, desc[, defaultpipetoscript]
        self.SetInputMembers([
                ['CellEntityIdsArrayName', 'entityidsarray', 'str', 1, '',
                 'name of the array where entity ids have been stored'],
                ] + members)
        self.SetOutputMembers([
                ['Mesh', 'o', 'vtkUnstructuredGrid', 1, '',
                 'the output mesh', 'vmtkmeshwriter'],
                ['CellEntityIdsArrayName', 'entityidsarray', 'str', 1, '',
                 'name of the array where entity ids have been stored'],
                ])

    def Execute(self):
        data = []
        for i in range(1,self.max_meshes+1):
            mesh = getattr(self, 'Mesh%d' % i)
            if mesh is not None:
                offset = getattr(self, 'CellEntityIdOffset%d' % i)
                data.append((i,mesh,offset))
        if len(data) < 2:
            self.PrintError('Error: Need at least 2 meshes to merge.')

        merger = vtkvmtk.vtkvmtkAppendFilter()
        for i, mesh, offset in data:
            cellids = mesh.GetCellData().GetScalars(self.CellEntityIdsArrayName)
            numIds = cellids.GetNumberOfTuples()
            self.PrintLog("Merging mesh %s with %d entityids offset by %d." % (i, numIds, offset))
            if offset != 0:
                for i in range(numIds):
                    cellids.SetValue(i, cellids.GetValue(i) + offset)
            merger.AddInput(mesh)
        merger.SetMergeDuplicatePoints(1)
        merger.Update()

        self.Mesh = merger.GetOutput()
        cellids = self.Mesh.GetCellData().GetScalars(self.CellEntityIdsArrayName)
        numIds = cellids.GetNumberOfTuples()
        self.PrintLog("Merged mesh has %d entityids." % (numIds,))

if __name__ == '__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()
