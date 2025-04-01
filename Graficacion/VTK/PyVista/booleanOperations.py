from __future__ import annotations

import pyvista as pv

cube = pv.Cube().triangulate().subdivide(3)
sphere = pv.Sphere(radius=0.6)
result = cube.boolean_difference(sphere)
p = pv.Plotter(shape=(2,2))
p.subplot(0,0)
p.add_mesh(result, color='#ff5353', show_edges=True, label='Normales de la esfera por defecto')
p.add_legend()

sphere.flip_normals()
result = cube.boolean_difference(sphere)
p.subplot(0,1)
p.add_mesh(result, color='#ff5353', show_edges=True, label='Normales de la esfera invertidas')
p.add_legend()

cube.flip_normals()
sphere.flip_normals()
result = cube.boolean_difference(sphere)
p.subplot(1,0)
p.add_mesh(result, color='#ff5353', show_edges=True, label='Normales del cubo invertidas')

p.add_legend()

sphere.flip_normals()
result = cube.boolean_difference(sphere)
p.subplot(1,1)
p.add_mesh(result, color='#ff5353', show_edges=True, label='Normales invertidas')

p.add_legend()

p.show()