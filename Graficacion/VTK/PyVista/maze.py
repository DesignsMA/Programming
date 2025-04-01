import numpy as np
import pyvista as pv
import numpy as np
# Crear disco base (este será nuestro "bloque constructor")
disco_base = pv.Disc(inner=0, outer=10, c_res=100, r_res=1)

# Crear plotter 3D
plotter = pv.Plotter()

# Lista para almacenar todos los discos rotados
laberinto = []

# Aplicar las rotaciones y crear la estructura
for i in range(3):
    # Rotar el disco alrededor del eje Z
    disco_rotado = disco_base.copy()
    disco_rotado.rotate_z(10*i, inplace=True)
    # Visualizar cada disco con color diferente
    plotter.add_mesh(disco_rotado, color='red', 
                   show_edges=True, opacity=0.8)


# Configuración de visualización
plotter.add_axes()
plotter.show()