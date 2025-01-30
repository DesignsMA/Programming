import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # Importar herramientas 3D
class Point():
    def __init__(self, x:float, y:float, z:float=0.0):
        self.y = y
        self.x = x
        self.z = z
        pass
    
    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    def __add__(self, otro):
        return Point(self.x + otro.x, self.y + otro.y, self.z +  otro.z)
    
    def __mul__(self, otro):
        if isinstance(otro, (float, int)):  # Multiplicar por un escalar
            return Point(self.x * otro, self.y * otro, self.z * otro)
        else:
            raise TypeError("Solo se puede multiplicar por un escalar (int o float)")

    def __rmul__(self, otro):
        # Manejar la multiplicación cuando el escalar está a la izquierda (por ejemplo, 2 * punto)
        return self.__mul__(otro)

    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, otro):
        # Comparar dos puntos para ver si son iguales
        return self.x == otro.x and self.y == otro.y and self.z == otro.z

class MallaBilineal():
    
    # Recibe los puntos que definen al cuadrilatero
    # Para generar la malla, dividimos u y v en n partes, i.e para una malla\
    # de 10X10 dividimos en 10 partes, u={0,0.1,0.2,…,1},v={0,0.1,0.2,…,1}
    def __init__(self, pt00:Point=Point(0,0), pt01:Point=Point(0,1)\
                     , pt10:Point=Point(1,0), pt11:Point=Point(1,1)\
                     , subdivisions: int=10):
        self.mesh = []
        self.pt00 = pt00
        self.pt01 = pt01
        self.pt10 = pt10
        self.pt11 = pt11
        self.subdivisions = subdivisions
    
        # Función de interpolación bilineal
        # Retorna el punto interpolado | un ejemplo:
        # En un cuadrilatero donde p00 = (0,0), p01 = (0,2)
        # p10 = (2,0), p11 = (2,2), la interpolacion  en (0.5, 0.5)
        # retorna  pt = (1,1), punto ubicado en el centro del cuadrilatero
    def bilinear_interpolation(self, u:float, v:float): #u y v oscilan entre 0 y 1 o los rangos del cuadrilatero
        return (1 - u) * (1 - v) * self.pt00 + u * (1 - v) * self.pt10 + (1 - u) * v * self.pt01 + u * v * self.pt11

    def generate_mesh(self):
        u=v=0
        for x in range(self.subdivisions + 1):  # Iterar sobre subdivisiones en u
            u = x * (1 / self.subdivisions)  # Calcular u
            for y in range(self.subdivisions + 1):  # Iterar sobre subdivisiones en v
                v = y * (1 / self.subdivisions)  # Calcular v
                self.mesh.append(self.bilinear_interpolation(u, v))  # Añadir punto a la malla
        return self.mesh

# MAIN
malla = MallaBilineal( Point(0,0), Point(0,3), Point(3,1), Point(3,4), 20)  # Ajustes por defecto
malla.generate_mesh()  # Generar malla

# Convertir a un array de numpy para facilitar la visualización
mesh_points = np.array([[point.x, point.y, point.z] for point in malla.mesh])

# Reorganizar los puntos en una cuadrícula para la visualización 3D
subdivisions = malla.subdivisions + 1
#El operador [:, 0] significa "todas las filas, columna 0".
#El método reshape de NumPy reorganiza un array 1D en un array 2D con la forma especificada.
#En este caso, mesh_points[:, 0].reshape(subdivisions, subdivisions)
# toma las coordenadas x (que están en un array 1D) y las reorganiza en
# una matriz 2D de tamaño subdivisions×subdivisions
# matplotlib espera una cuadricula  estructurada (matriz 2d) de tus valores
# matplotlib necesita que los datos estén en un formato de matriz 2D para 
# poder graficar superficies (plot_surface) y líneas (plot).
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
plt.title('Malla Bilineal en 3D')

# Mostrar el gráfico
plt.show()
