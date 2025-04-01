from __future__ import annotations

import pyvista as pv
from math import fabs
cone = pv.Cone(height=10, radius=3.8, resolution=20, direction=(0,0,-1)).triangulate().subdivide(3)
sphere = pv.Sphere(radius=4,center=(0,0,fabs(10-4*0.75)), phi_resolution=20, theta_resolution=20).triangulate().subdivide(3)
cream = sphere.boolean_difference(cone) # restarle a la esfera el cono
cone = cone.boolean_difference(sphere)
p = pv.Plotter()
p.add_mesh(cone, color='#ff5353', show_edges=False, label='Cono')
p.add_legend()
p.add_mesh(cream, color='pink', show_edges=False, label='Cream')
p.add_legend()
p.camera_position = 'xz'
p.show()