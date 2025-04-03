import numpy as np
import pyvista as pv
import time

# Crear disco base
disco_base = pv.Disc(inner=0, outer=10, c_res=100, r_res=1).triangulate()
disco_base.translate([0, 0, -15], inplace=True)  # Mover abajo para mejor visualización

# Ángulos de rotación en 3 etapas (en grados)
angulos_euler = [30, 60, 90]  # Tres rotaciones acumulativas

# Configurar plotter
plotter = pv.Plotter()
plotter.add_axes()

# Añadir disco original
plotter.add_mesh(disco_base, color='white', opacity=0.5, show_edges=True)

# Rotación acumulativa
disco_rotado = disco_base.copy()
for i, angulo in enumerate(angulos_euler, 1):
    # Aplicar rotación sobre el eje x (Euler x)
    disco_rotado.rotate_x(angulo, inplace=True)
    
    # Elevar el disco para visualización en 3D
    disco_rotado.translate([0, 0, 10*i], inplace=True)
    
    # Añadir al plotter
    color = np.random.rand(3)  # Color aleatorio para cada rotación
    plotter.add_mesh(disco_rotado.copy(), color=color, opacity=0.8, show_edges=True, label=f"Rotación {i}: {angulo}°")
    plotter.add_legend()
# Mostrar resultado final
plotter.show()