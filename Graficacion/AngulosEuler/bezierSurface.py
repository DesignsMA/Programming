import matplotlib.pyplot as plt
import numpy as np
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
                
    def generateMesh(self):
        self.mesh = []
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
        ptx = np.array([point.x for point in self.mesh])
        pty = np.array([point.y for point in self.mesh])
        ptz = np.array([point.z for point in self.mesh])
        
        fig = plt.figure() #generar figura
        ax = fig.add_subplot(projection='3d') #añadir subplot
        
        ptX = ptx.reshape(self.subdivisions+1,self.subdivisions+1)
        ptY = pty.reshape(self.subdivisions+1,self.subdivisions+1)
        ptZ = ptz.reshape(self.subdivisions+1,self.subdivisions+1)

        # Aplicar gradiente de colores a la superficie basado en z
        ax.plot_surface(ptX, ptY, ptZ, cmap='plasma',rstride=1, cstride=1, alpha=1)       
        # Trazar la malla de alambre
        ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)
        
        ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos

        # Configuraciones adicionales
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("Superficie de bézier")
        plt.show()
        
    def __main__(self):
        # MAIN
        # Definir los puntos de control para las curvas de Bézier, genera una parábola 3d
        mesh2  = np.array([
            [Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 0)],
            [Point(0, 1, 1), Point(1, 1, 2), Point(2, 1, 1)],
            [Point(0, 2, 0), Point(1, 2, 1), Point(2, 2, 0)]
        ])

        malla = BezierSurface(surfacePoints=mesh2, subdivisions=20)
        malla.generateMesh()  # Generar malla
        malla.interactiveGraph() # Mostrar gráfica
