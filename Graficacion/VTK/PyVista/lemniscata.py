from __future__ import annotations

import pyvista as pv
import numpy as np
torus = pv.ParametricTorus(ringradius=6, crosssectionradius=6, u_res = 20, v_res = 20, w_res = 20).triangulate().subdivide(3)
cube = pv.Cube(center=(0,0,0), x_length=25, y_length=0.5, z_length=12).triangulate().subdivide(3)
res = torus.boolean_intersection(cube)

p = pv.Plotter()
p.add_mesh(cube, color='#ff5353', show_edges=False, opacity=0.1)
p.add_mesh(torus, color='#53ff53', show_edges=False, opacity=0.2)
p.add_mesh(res, color='purple', show_edges=False)
p.camera_position = 'xz'
p.show_axes()
p.show()