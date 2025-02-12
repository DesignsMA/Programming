import matplotlib.pyplot as plt
import numpy as np
import pprint as pp
from mpl_toolkits.mplot3d import Axes3D  # Importar herramientas 3D
from mathObjects import *
# surfacePoints es una matriz de 4X4 que describe una superficie bicubica para metrica
# sin necesidad de guardar cada punto interpolado, una superficie de bezier es una
# generalizacion de una curva de bezier donde cada de una de las cuatro filas de puntos
# de control pueden ser pensadas como una curva de bezier en dos dimensiones.

# lo
class BezierSurface():
    def __init__(self, surfacePoints: np.ndarray = None, subdivisions: int = 10):
        self.mesh = []
        self.surfacePoints = surfacePoints
        self.subdivisions = subdivisions
        self.n = None
        
    def calculate_n(self):
        """
        Calcula el grado de la superficie (n) basado en el tamaño de surfacePoints.
        """
        if self.surfacePoints is not None:
            # El grado es el número de puntos de control en una dirección menos 1
            self.n = self.surfacePoints.shape[0]
        else:
            raise ValueError("surfacePoints no está inicializado")
        
    def create_bezier_patch(self):
        self.surfacePoints = np.array([
            [Point(0, 0, 0), Point(1, 0, 2), Point(2, 0, 1), Point(3, 0, 3)],
            [Point(0, 1, 1), Point(1, 1, 3), Point(2, 1, 2), Point(3, 1, 4)],
            [Point(0, 2, 2), Point(1, 2, 4), Point(2, 2, 3), Point(3, 2, 5)],
            [Point(0, 3, 3), Point(1, 3, 5), Point(2, 3, 4), Point(3, 3, 6)] ])

    def bernstein_basis_polynomial(self, v: int, n: int, x: int): # ( n | v)
        return binomial(n,v)*x**v*(1-x)**(n-v)
    
    def generateCoordinate( self, u: float, v:float, attr: str):
        coord = 0
        for i in range(self.n):
            for j in range(self.n):
                coord += getattr(self.surfacePoints[i,j], attr)*self.bernstein_basis_polynomial(i, self.n-1, u)\
                         *self.bernstein_basis_polynomial(j, self.n-1, v)
        return coord
                
    def generate_mesh(self):
        if self.surfacePoints is None:
            self.create_bezier_patch()
        
        self.calculate_n()

        for u_index in range(self.subdivisions + 1):
            u = u_index * (1.0 / self.subdivisions)  # Calculate u
            for v_index in range(self.subdivisions + 1):
                v = v_index * (1.0 / self.subdivisions)  # Calculate v
                x = self.generateCoordinate(u, v, 'x')
                y = self.generateCoordinate(u, v, 'y')
                z = self.generateCoordinate(u, v, 'z')
                self.mesh.append(Point(x, y, z))  # Append as a Point object           
                     
    
    def interactiveGraph(self):
        for point in self.mesh:
            print(f"{point}", end=' | ')
        # Convertir a un array de numpy para facilitar la visualización
        mesh_points = np.array([[point.x, point.y, point.z] for point in self.mesh])

        pp.pp(mesh_points)
        # Reorganizar los puntos en una cuadrícula para la visualización 3D
        # mesh_points[:, 0] DE TODAS LAS FILAS, EXTRAE EL ELEMENTO CERO
        # .reshape(subdivisions, subdivisions)  MODIFCA EL ARREGLO 1D A 2D,, es decir si el arreglo 1d tiene 3 elementos y realizas un reshape(1,3)
        # obtienes un arreglo 2d con 3 filas donde sea [1,2,3] -> [ [1], [2], [3] ]
        subdivisions = self.subdivisions + 1
        X = mesh_points[:, 0].reshape(subdivisions, subdivisions)
        Y = mesh_points[:, 1].reshape(subdivisions, subdivisions)
        Z = mesh_points[:, 2].reshape(subdivisions, subdivisions)
        
        pp.pp(X)
        pp.pp(Y)
        pp.pp(Z)
        # Visualizar la malla en 3D
        fig = plt.figure() #nueva ventana
        #ax = fig.add_subplot(111, projection='3d'): Añade un subplot (gráfico) en la figura con proyección 3D. El argumento 111 indica que es el primer (y único) gráfico en una cuadrícula de 1x1.
        ax = fig.add_subplot(111, projection='3d')  # Crear un gráfico 3D

        # Graficar la superficie | la  superficie compuesta por los puntos
        ax.plot_surface(X, Y, Z, color='black', alpha=0.12)

        # Graficar los puntos de la malla
        ax.scatter(X, Y, Z, color='red')
        #extrae todos los elementos de la primera fila x[i,j] i = filas, j = columnas
        pp.pp(X[0,:])
        pp.pp(Y[0,:])
        pp.pp(Z[0,:])
        #extrae todos los elementos de la primera columna x[i,j] i = filas, j = columnas
        pp.pp(X[:,0])
        pp.pp(Y[:,0])
        pp.pp(Z[:,0])
        # Conectar los puntos con líneas
        for i in range(subdivisions):
            ax.plot(X[i, :], Y[i, :], Z[i, :], color='black')  # Líneas en dirección u
            ax.plot(X[:, i], Y[:, i], Z[:, i], color='black')  # Líneas en dirección v

        # Etiquetar los ejes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Agregar un título al gráfico
        plt.title('Superficie de bézier')

        # Mostrar el gráfico
        plt.show()
        
        
# MAIN
# Definir los puntos de control para las curvas de Bézier
mesh2 = np.array([
            [Point(-1, 0, 0), Point(0, 0, 1), Point(1, 0, 0)],
            [Point(-1, -1.5, 0), Point(0, -1.5, 1), Point(1, -1.5, 0)],
            [Point(-1, -3, 0), Point(0, -3, 1), Point(1, -3, 0)],
            ])

malla = BezierSurface(surfacePoints=mesh2, subdivisions=20)
malla.generate_mesh()  # Generar malla
malla.interactiveGraph() # Mostrar gráfica
