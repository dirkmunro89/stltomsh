import vtk
import meshio
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
#
# read gmsh result
filename='tmp.msh'
mesh = meshio.read(filename,)
points=mesh.points
cells=mesh.cells
#
# write to vtk
meshio.write_points_cells("msh.vtk",points,cells)
#
# read vtk
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName("msh.vtk")
reader.Update()
tet=reader.GetOutput()
#
# seperate out element types
srf_pts=vtk.vtkPoints()
srf_elm=vtk.vtkCellArray()
srf_ply=vtk.vtkPolyData()
lne_pts=vtk.vtkPoints()
lne_elm=vtk.vtkCellArray()
lne_ply=vtk.vtkPolyData()
pts_pts=vtk.vtkPoints()
pts_elm=vtk.vtkCellArray()
pts_ply=vtk.vtkPolyData()
tet_pts=vtk.vtkPoints()
tet_ply=vtk.vtkUnstructuredGrid()
#
n=tet.GetCells().GetNumberOfCells()
pts=np.zeros((tet.GetNumberOfPoints(),5))
for i in range(n):
    idList = vtk.vtkIdList()
    tet.GetCellPoints(i,idList)
    m=idList.GetNumberOfIds()
    if m == 4:
        tet_ply.InsertNextCell(10,idList)
    if m == 3:
        srf_elm.InsertNextCell(idList)
    if m == 2:
        lne_elm.InsertNextCell(idList)
    if m == 1:
        pts_elm.InsertNextCell(idList)
    for j in range(m): pts[idList.GetId(j)][m]=1
#
p=vtk_to_numpy(tet.GetPoints().GetData())
for i in range(tet.GetNumberOfPoints()):
    if pts[i][4]: tet_pts.InsertPoint(i,p[i][0],p[i][1],p[i][2])
    if pts[i][3]: srf_pts.InsertPoint(i,p[i][0],p[i][1],p[i][2])
    if pts[i][2]: lne_pts.InsertPoint(i,p[i][0],p[i][1],p[i][2])
    if pts[i][1]: pts_pts.InsertPoint(i,p[i][0],p[i][1],p[i][2])
#
tet_ply.SetPoints(tet_pts)
writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName('./out/tet.vtu')
writer.SetInputData(tet_ply)
writer.Write()
#
srf_ply.SetPoints(srf_pts)
srf_ply.SetPolys(srf_elm)
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('./out/srf.vtp')
writer.SetInputData(srf_ply)
writer.Write()
#
lne_ply.SetPoints(lne_pts)
lne_ply.SetPolys(lne_elm)
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('./out/lne.vtp')
writer.SetInputData(lne_ply)
writer.Write()
#
pts_ply.SetPoints(pts_pts)
pts_ply.SetPolys(pts_elm)
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName('./out/pts.vtp')
writer.SetInputData(pts_ply)
writer.Write()
