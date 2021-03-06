/*=========================================================================

Program:   VMTK
Module:    $RCSfile: vtkvmtkSmoothCapPolyData.h,v $
Language:  C++
Date:      $Date: 2006/07/17 09:53:14 $
Version:   $Revision: 1.5 $

  Copyright (c) Luca Antiga, David Steinman. All rights reserved.
  See LICENCE file for details.

  Portions of this code are covered under the VTK copyright.
  See VTKCopyright.txt or http://www.kitware.com/VTKCopyright.htm
  for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notices for more information.

=========================================================================*/
  // .NAME vtkvmtkSmoothCapPolyData - Add caps to boundaries.
  // .SECTION Description
  // This class closes the boundaries of a surface with a cap.

#ifndef __vtkvmtkSmoothCapPolyData_h
#define __vtkvmtkSmoothCapPolyData_h

#include "vtkPolyDataAlgorithm.h"
#include "vtkIdList.h"
#include "vtkvmtkWin32Header.h"

class VTK_VMTK_MISC_EXPORT vtkvmtkSmoothCapPolyData : public vtkPolyDataAlgorithm
{
  public:
  vtkTypeRevisionMacro(vtkvmtkSmoothCapPolyData,vtkPolyDataAlgorithm);
  void PrintSelf(ostream& os, vtkIndent indent);

  static vtkvmtkSmoothCapPolyData *New();

  vtkSetObjectMacro(BoundaryIds,vtkIdList);
  vtkGetObjectMacro(BoundaryIds,vtkIdList);

  vtkSetMacro(ConstraintFactor,double);
  vtkGetMacro(ConstraintFactor,double);

  vtkSetMacro(NumberOfRings,int);
  vtkGetMacro(NumberOfRings,int);

  vtkSetStringMacro(CellEntityIdsArrayName);
  vtkGetStringMacro(CellEntityIdsArrayName);

  vtkSetMacro(CellEntityIdOffset,int);
  vtkGetMacro(CellEntityIdOffset,int);

  protected:
  vtkvmtkSmoothCapPolyData();
  ~vtkvmtkSmoothCapPolyData();

  virtual int RequestData(vtkInformation *, vtkInformationVector **, vtkInformationVector *);

  vtkIdList* BoundaryIds;
  double ConstraintFactor;
  int NumberOfRings;

  char* CellEntityIdsArrayName;

  int CellEntityIdOffset;

  private:
  vtkvmtkSmoothCapPolyData(const vtkvmtkSmoothCapPolyData&);  // Not implemented.
  void operator=(const vtkvmtkSmoothCapPolyData&);  // Not implemented.
};

#endif
