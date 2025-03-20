import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from disc import *
from mathObjects import *

# Función implícita para obtener z en función de x e y
def implicitFunc(disc: DiscMesh, pointInDisc: Point):
    x0, y0, z0 = disc.center.x, disc.center.y, disc.center.z
    r1 = disc.radio
    
    x1, y1 = pointInDisc.x, pointInDisc.y 
    
    try:
        # Calcular z1 utilizando la fórmula del disco
        z1_positive =  (x1 - x0)**2 + (y1 - y0)**2 -r1**2
        return z1_positive
    except ValueError:
        # Si hay un error en la raíz cuadrada (cuando el punto está fuera del disco)
        return None

# Función para graficar los puntos en 3D
def graph(ax, color, mesh, size: int=1, alpha: float=1):
    ptx = np.array([point.x for point in mesh])
    pty = np.array([point.y for point in mesh])
    ptz = np.array([point.z for point in mesh])
    
    ax.scatter(ptx, pty, ptz, c=color, s=size, depthshade=False, alpha=alpha )  # Graficar puntos

# Crear la figura y los ejes 3D
fig = plt.figure() 
ax = fig.add_subplot(projection='3d')
ax.set_box_aspect([1, 0.8, 1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Crear los discos
disc1 = DiscMesh(subdivisions=100, radio=10)
disc1.generateMesh()

disc2 = DiscMesh(center=Point(5, 0, 0), subdivisions=100, radio=10)
disc2.generateMesh()

graph1 = []
graph2 = []

# Calcular las alturas z1 y z2 para cada punto de los discos
for p1, p2 in zip(disc1.mesh, disc2.mesh):
    z1 = implicitFunc(disc1, p1)
    z2 = implicitFunc(disc2, p2)
    
    if z1 is not None:
        graph1.append(Point(p1.x, p1.y, z1))  # Asignar la altura calculada a z1
    
    if z2 is not None:
        graph2.append(Point(p2.x, p2.y, z2))  # Asignar la altura calculada a z2

# Graficar los puntos de los discos
graph(ax, '#ff5353', graph1)  # Graficar el disco 1
graph(ax, '#5353ff', graph2)  # Graficar el disco 2

plt.show()
