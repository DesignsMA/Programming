from __future__ import annotations

import pyvista as pv
from math import fabs
class IceCream:
    def __init__(self, coneH:int = 10, coneR:int=4, resolution:int=30, creamR:int=4 ):
        cone = pv.Cone(height=coneH, radius=coneR, resolution=resolution, direction=(0,0,-1)).triangulate().subdivide(3)
        sphere = pv.Sphere(radius=creamR,center=(0,0,fabs(coneH-creamR*0.75)), phi_resolution=resolution, theta_resolution=resolution).triangulate().subdivide(3)
        self.cream = sphere.boolean_difference(cone) # restarle a la esfera el cono
        self.cone = cone.boolean_difference(sphere)
        self.polydata = self.cone+self.cream
 
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

def iceCreamFunc():
    head = pv.Sphere(radius=4,center=(0,0,0), phi_resolution=20, theta_resolution=20).triangulate().subdivide(3)
    eyel = pv.Cylinder(radius=0.5, center = (2,4,2), direction=(0,1,0), height=5,resolution=20).triangulate().subdivide(3)
    eyer = pv.Cylinder(radius=0.5, center = (-2,4,2), direction=(0,1,0), height=5,resolution=20).triangulate().subdivide(3)
    helmet = head.boolean_difference(eyel+eyer)
    p = pv.Plotter()
    p.add_mesh(helmet, color='#ff5353', show_edges=False, label='Cono')
    p.add_legend()
    p.camera_position = 'xz'
    p.show()


iceCreamFunc()
