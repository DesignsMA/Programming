from pyvis.network import Network
import numpy as np
import random
# clases de utilidad

class Edge():
  def __init__(self, a: float = 0, b: float = 0):
      """
      Representación de un lado.
      
      :params:
      a (float): Miembro 'a' del lado.
      
      b (float): Miembro 'b' del lado.
      """
      self.a = a
      self.b = b
  
  def __repr__(self):
     return f"Edge({self.a}, {self.b})"
  
  def getTuple(self): # retorna dupla de valores
      return (self.a,self.b)
  
  def getArray(self):
      return np.array([self.a,self.b], dtype=np.float64) # retornar arreglo de tipo float64

class Point2D():
  def __init__(self, x: float = 0, y: float = 0):
      """
      Point2D | Representación de un punto en dos dimensiones.
      
      :params:
        x (float): Coordenada en el eje X.
        
        y (float): Coordenada en el eje Y.
      """
      self.x = x
      self.y = y
    
  def __repr__(self):
      return f"Point2D({self.x}, {self.y})"
  
  def __lt__(self, other):
      """ Define el orden de los puntos (orden por x, luego por y) """
      if self.x == other.x:
          return self.y < other.y
      return self.x < other.x

  def distance_to(self, other):
      """Calcula la distancia entre dos puntos"""
      return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

# clase que maneja la lógica de la triangulación
class DelaunayTriangulation():
  
  def __init__(self):
    pass
  
  