from __future__ import annotations

import pyvista as pv
from math import fabs
from iceCream import IceCream
class Helmet:
    def __init__(self, headR:float=7, resolution:int=30, xCube:float=10, yCube:float=8, zCube:float=7 ):
        icecream2 = IceCream(coneH=10, coneR=3.8, resolution=resolution, creamR=headR)
        cube = pv.Cube(center=(0,-0.5,10), x_length=xCube, y_length=yCube, z_length=zCube).triangulate().subdivide(3)
        res = cube.boolean_difference(icecream2.polydata) # diferencia booleana
        self.polydata = res
 
    def boolean_difference(self, other: pv.PolyData):
        if not other.is_all_triangles:
            triangulatedMesh = other.triangulate().subdivide(3) 
        else:
            triangulatedMesh = other   
        return self.polydata.boolean_difference(triangulatedMesh) # return mesh
    
    def boolean_union(self, other: pv.PolyData):
        if not other.is_all_triangles:
            triangulatedMesh = other.triangulate().subdivide(3) 
        else:
            triangulatedMesh = other   
        return self.polydata.boolean_union(triangulatedMesh) # return mesh
    
    def boolean_intersection(self, other: pv.PolyData):
        if not other.is_all_triangles:
            triangulatedMesh = other.triangulate().subdivide(3) 
        else:
            triangulatedMesh = other   
        return self.polydata.boolean_intersection(triangulatedMesh) # return mesh

def helmFunc():
    icecream = IceCream(resolution=10, creamR=6.3)
    helm = Helmet(resolution=10)
    p = pv.Plotter()
    p.add_mesh(helm.polydata, show_edges=False)
    p.add_mesh(icecream.polydata, show_edges=False)
    p.camera_position = 'xz'
    p.show()



helmFunc()