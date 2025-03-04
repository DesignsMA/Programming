#Funciones básicas
import numpy as np
from math import cos, sin, radians, sqrt
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
    
    def __sub__(self, otro):
        return Point(self.x - otro.x, self.y - otro.y, self.z - otro.z)
    
    def __rsub__(self, otro):
        return Point(otro.x - self.x, otro.y - self.y, otro.z - self.z)
    
    def __mul__(self, otro):
        if isinstance(otro, (float, int)):  # Multiplicar por un escalar
            return Point(self.x * otro, self.y * otro, self.z * otro)
        elif isinstance(otro, Point):  # Producto escalar entre dos puntos
            return self.x * otro.x + self.y * otro.y + self.z * otro.z
        else:
            raise TypeError("Solo se puede multiplicar por un escalar (int o float) o calcular el producto escalar con otro Point")

    def __rmul__(self, otro):
        return self.__mul__(otro)
    
    def __truediv__(self, otro):
      if isinstance(otro, (float, int)):
          if otro == 0:
              raise ZeroDivisionError("No se puede dividir por cero")
          return Point(self.x / otro, self.y / otro, self.z / otro)
      else:
          raise TypeError("Solo se puede dividir por un escalar (int o float)")

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y and self.z == otro.z

    def __hash__(self):
        """
        Devuelve un valor hash para el punto.
        Esto permite que los objetos de la clase Point sean usados en conjuntos y como claves en diccionarios.
        """
        return hash((self.x, self.y, self.z))  # Usamos una tupla de las coordenadas para el hash
    
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
        
    def arr(self):
        return np.array( [ self.x, self.y, self.z ])
    
    @staticmethod
    def rotation_matrix_x(angle: float):
        """
        Retorna la matriz de rotación alrededor del eje x.

        Parámetros:
            angle (float): Ángulo de rotación en grados.
        """
        angle = radians(angle)  # Convertir a radianes
        return np.array([
            [1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)]
        ])
        
    def norm(self):
        """
        Calcula la norma (magnitud) del vector representado por el punto.
        """
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    @staticmethod
    def rotation_matrix_y(angle: float):
        """
        Retorna la matriz de rotación alrededor del eje y.

        Parámetros:
            angle (float): Ángulo de rotación en grados.
        """
        angle = radians(angle)  # Convertir a radianes
        return np.array([
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]
        ])

    @staticmethod
    def rotation_matrix_z(angle: float):
        """
        Retorna la matriz de rotación alrededor del eje z.

        Parámetros:
            angle (float): Ángulo de rotación en grados.
        """
        angle = radians(angle)  # Convertir a radianes
        return np.array([
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]
        ])
    
    @staticmethod
    def centroid(p1, p2, p3):
        """Calcula el centroide de tres puntos."""
        if not all(isinstance(p, Point) for p in [p1, p2, p3]):
            raise TypeError("Los argumentos deben ser instancias de Point.")

        cx = (p1.x + p2.x + p3.x) / 3
        cy = (p1.y + p2.y + p3.y) / 3
        cz = (p1.z + p2.z + p3.z) / 3

        return Point(cx, cy, cz)

    def rotate(self, angle_x: float = 0, angle_y: float = 0, angle_z: float = 0):
        """
        Aplica una rotación al punto alrededor de los ejes x, y, y z.

        Parámetros:
            angle_x (float): Ángulo de rotación alrededor del eje x en grados.
            angle_y (float): Ángulo de rotación alrededor del eje y en grados.
            angle_z (float): Ángulo de rotación alrededor del eje z en grados.
        """
        # Convertir el punto a un array de NumPy
        point_arr = self.arr()

        # Aplicar las rotaciones en el orden z, y, x (común en gráficos 3D)
        if angle_z != 0:
            point_arr = np.dot(self.rotation_matrix_z(angle_z), point_arr)
        if angle_y != 0:
            point_arr = np.dot(self.rotation_matrix_y(angle_y), point_arr)
        if angle_x != 0:
            point_arr = np.dot(self.rotation_matrix_x(angle_x), point_arr)

        # Actualizar las coordenadas del punto
        self.x, self.y, self.z = point_arr

    def rotateWithMatrix(self, rotation_matrix):
        rotated_arr = np.dot(rotation_matrix, self.arr())  # Aplicar la rotación
        self.x, self.y, self.z = rotated_arr
