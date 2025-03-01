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