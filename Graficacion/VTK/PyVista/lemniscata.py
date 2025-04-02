from __future__ import annotations

import pyvista as pv
import numpy as np
torus = pv.ParametricTorus(ringradius=3, crosssectionradius=6)
puntos_cercanos = torus.points[np.abs(torus.points[:,1]) < 0.15]

# Crear nube de puntos
nube_puntos = pv.PolyData(puntos_cercanos)

p = pv.Plotter()
p.add_mesh(nube_puntos, color='#ff5353', show_edges=True, label='Cono')
p.add_legend()
p.camera_position = 'xz'
p.show()