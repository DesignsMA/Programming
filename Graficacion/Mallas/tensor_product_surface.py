import matplotlib.pyplot as plt
import numpy as np
import pprint as pp
from mpl_toolkits.mplot3d import Axes3D  # Importar herramientas 3D

#Funciones básicas
def factorial(x: int):
    if x == 1 or x == 0:
        return 1
    else:
        return x * factorial(x - 1)

def binomial(n: int, k: int): # (n | k)
    """
    Calcula el coeficiente binomial (n | k), que representa el número de formas de elegir k elementos de un conjunto de n elementos.

    Parámetros:
        n (int): El número total de elementos.
        k (int): El número de elementos a elegir.

    Retorna:
        float: El valor del coeficiente binomial (n | k).
    """
    return factorial(n) / (factorial(k) * factorial(n - k))

#Clases
class Point():
    def __init__(self, x: float, y: float, z: float = 0.0):
        """
        Inicializa un punto en el espacio 3D con coordenadas (x, y, z).

        Parámetros:
            x (float): Coordenada x del punto.
            y (float): Coordenada y del punto.
            z (float, opcional): Coordenada z del punto. Por defecto es 0.0.
        """
        self.y = y
        self.x = x
        self.z = z

    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __add__(self, otro):
        return Point(self.x + otro.x, self.y + otro.y, self.z + otro.z)
    
    def __radd__(self, otro):
        return self.__add__(otro)
    
    def __mul__(self, otro):
        if isinstance(otro, (float, int)):  # Multiplicar por un escalar
            return Point(self.x * otro, self.y * otro, self.z * otro)
        else:
            raise TypeError("Solo se puede multiplicar por un escalar (int o float)")

    def __rmul__(self, otro):
        return self.__mul__(otro)

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y and self.z == otro.z
    
    def __str__(self):
        return f"({self.x} {self.y} {self.z})"
    
    def __format__(self, format_spec):
        # Define how the Point should be formatted based on the format_spec
        if format_spec == "coords":
            return f"({self.x}, {self.y}, {self.z})"
        elif format_spec == "verbose":
            return f"Point(x={self.x}, y={self.y}, z={self.z})"
        elif format_spec == "short":
            return f"P({self.x},{self.y},{self.z})"
        else:
            # Default formatting
            return f"({self.x}, {self.y}, {self.z})"

class TensorProductSurface():
    """
    Inicializa una superficie de producto tensorial.

    Parámetros:
        controlPoints (np.ndarray, opcional): Matriz de puntos de control. Por defecto es None.
        type (int, opcional): Tipo de función base a utilizar (0: Bernstein, 1: B-spline). Por defecto es 0.
        subdivisions (int, opcional): Número de subdivisiones para generar la malla. Por defecto es 10.
    """
    def __init__(self, controlPoints: np.ndarray = None, type: int = 0, subdivisions: int = 10):
        self.mesh = []
        self.controlPoints = controlPoints
        self.type = 0
        self.function = self._select_function()
        self.subdivisions = subdivisions
        self.m = controlPoints.shape[0]
        self.n = controlPoints.shape[1]
                
    def _select_function(self):
        """
        Selecciona la función base según el tipo.
        """
        if self.type == 0:
            return self.bernstein_basis_polynomial
        elif self.type == 1:
            return self.b_spline_basis_polynomial
        else:
            raise ValueError("Tipo de función base no soportado.")
        
    def bernstein_basis_polynomial(self, v: int, n: int, x: int): # ( n | v) | Me
        return binomial(n,v)*x**v*(1-x)**(n-v)
    
    def select_knot_vector(self, m: int, p: int=0):
        print("""
              
              """)
        type = type = int(input())

        if type == 0:
            return [u for u in range(m+1)] #  espaciado constante y cerrado
        elif type == 1:
            temp = [0,0.5]
            return temp + [u for u in range(m+1)] #espaciado diferente
        elif type == 2:
            temp = [u for u in range(m+1)]
            for i in range(p+1):
                temp.insert(0, temp[0])
                temp.append(temp[len(temp)])
            return temp
        else:
            print("Opción desconocida, usando 0.")
            return [u for u in range(m+1)] 
    
    def b_spline(self, i: int, p: int, x: int):
        pass
        #for i in range(resolution):
        #t = 0 + 1 * i / resolution  # generar (resolution)-puntos en el rango 0-1
        #pt = Point(0, 0)  
        #term_x = ""
        #term_y = ""
        #for u in range(n + 1):
        #    pt.x += cfs[u] * points[u].x * math.pow((1 - t), n - u) * math.pow(t, u)
        #    pt.y += cfs[u] * points[u].y * math.pow((1 - t), n - u) * math.pow(t, u)

    def generateCoordinate( self, u: float, v:float, attr: str):
        coord = 0
        for i in range(self.m):
            for j in range(self.n):
                coord += getattr(self.controlPoints[i,j], attr)*self.function(i, self.m-1, u)\
                         *self.function(j, self.n-1, v)
        return coord
                
    def generate_mesh(self):
        if self.controlPoints is None:
            print("Se necesita de una matriz de puntos de control.")
            return
        
        for u_index in range(self.subdivisions + 1):
            u = u_index * (1.0 / self.subdivisions)  # Calcular en direccion u
            for v_index in range(self.subdivisions + 1):
                v = v_index * (1.0 / self.subdivisions)  # Calcular en direccion v
                x = self.generateCoordinate(u, v, 'x')
                y = self.generateCoordinate(u, v, 'y')
                z = self.generateCoordinate(u, v, 'z')
                self.mesh.append(Point(x, y, z))  # Añadir como punto       
                     
    
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

# Definir la malla 4x4 de puntos de control usando la clase Point
control_points = np.array([
    [Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 1), Point(3, 0, 0)],
    [Point(0, 1, 1), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 1)],
    [Point(0, 2, 1), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 1)],
    [Point(0, 3, 0), Point(1, 3, 1), Point(2, 3, 1), Point(3, 3, 0)]
])

malla = TensorProductSurface(controlPoints=control_points,type=0,subdivisions=20)
malla.generate_mesh()  # Generar malla
malla.interactiveGraph() # Mostrar gráfica
