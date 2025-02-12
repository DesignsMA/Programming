import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # Importar herramientas 3D
from mathObjects import *

class MallaBipoligonal():
    def __init__(self, pt0: Point, pt1: Point, pt2: Point, pt3: Point, pt4: Point, pt5: Point, pt6: Point, pt7: Point, subdivisions: int = 10):
        self.mesh = []
        self.pt0 = pt0
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
        self.pt4 = pt4
        self.pt5 = pt5
        self.pt6 = pt6
        self.pt7 = pt7
        self.subdivisions = subdivisions

    def bezier_quadratic(self, t: float, p0: Point, p1: Point, p2: Point):
        return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2

    def generate_mesh(self):
        for x in range(self.subdivisions + 1):
            u = x * (1 / self.subdivisions)  # Calcular u
            for y in range(self.subdivisions + 1):
                v = y * (1 / self.subdivisions)  # Calcular v

                # Calcular puntos en las curvas de Bézier
                q0 = self.bezier_quadratic(u, self.pt0, self.pt1, self.pt2)  # Lado inferior
                q1 = self.bezier_quadratic(v, self.pt2, self.pt3, self.pt4)  # Lado derecho
                q2 = self.bezier_quadratic(v, self.pt4, self.pt5, self.pt6)  # Lado superior
                q3 = self.bezier_quadratic(u, self.pt6, self.pt7, self.pt0)  # Lado izquierdo

                # Interpolación bipoligonal
                punto = (1 - u) * (1 - v) * q0 + u * (1 - v) * q1 + (1 - u) * v * q3 + u * v * q2    
                self.mesh.append(punto)

        return self.mesh

# MAIN
# Definir los puntos de control para las curvas de Bézier
pt0 = Point(0, 0)
pt1 = Point(0, 1.5)
pt2 = Point(0, 3)
pt3 = Point(1.5, 3)
pt4 = Point(3, 3)
pt5 = Point(3, 1.5)
pt6 = Point(3, 0)
pt7 = Point(1.5, 0)


malla = MallaBipoligonal(pt0, pt1, pt2, pt3, pt4, pt5, pt6, pt7, subdivisions=5)
malla.generate_mesh()  # Generar malla

# Convertir a un array de numpy para facilitar la visualización
mesh_points = np.array([[point.x, point.y, point.z] for point in malla.mesh])

# Reorganizar los puntos en una cuadrícula para la visualización 3D
subdivisions = malla.subdivisions + 1
X = mesh_points[:, 0].reshape(subdivisions, subdivisions)
Y = mesh_points[:, 1].reshape(subdivisions, subdivisions)
Z = mesh_points[:, 2].reshape(subdivisions, subdivisions)

# Visualizar la malla en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # Crear un gráfico 3D

# Graficar la superficie
ax.plot_surface(X, Y, Z, color='black', alpha=0.12)

# Graficar los puntos de la malla
ax.scatter(X, Y, Z, color='red')

# Conectar los puntos con líneas
for i in range(subdivisions):
    ax.plot(X[i, :], Y[i, :], Z[i, :], color='black')  # Líneas en dirección u
    ax.plot(X[:, i], Y[:, i], Z[:, i], color='black')  # Líneas en dirección v

# Etiquetar los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Agregar un título al gráfico
plt.title('Malla Bipoligonal en 3D')

# Mostrar el gráfico
plt.show()