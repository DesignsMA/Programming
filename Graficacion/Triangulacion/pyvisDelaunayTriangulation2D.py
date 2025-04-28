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
  
  def tuple(self):
      "Returns the tuple equivalent of the class."
      return (self.a,self.b) # tuple
  
  def arr(self):
      "Returns the numpy array equivalent of the class."
      return np.array([self.a,self.b], dtype=np.float64) # retornar arreglo de tipo float64

class Point2D():
  """
    Point2D | Representación de un punto en dos dimensiones.
  """
    
  def __init__(self, x: float = 0, y: float = 0):
      """      
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
  
  def arr(self):
      "Returns the numpy array equivalent of the class."
      return np.array([self.x,self.y], dtype=np.float64) # retornar arreglo de tipo float64
      

# clase que maneja la lógica de la triangulación
class DelaunayTriangulation():
  
  def __init__(self, points: list):
      self.points = points
      self.sorted = points.copy()
      self.edges = []
      self.hull = []
      self.circuncenters = []

  def insideCircle(self, A: Point2D, B: Point2D, C: Point2D, P: Point2D):
    ax = A.x - P.x
    ay = A.y - P.y
    bx = B.x - P.x
    by = B.y - P.y
    cx = C.x - P.x
    cy = C.y - P.y
    
    # Esto calcula el determinante (debe ser > 0 para estar dentro del círculo)
    return (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) > 0
  
  def crossProduct(self, A: Point2D, B: Point2D):
    return A.x * B.y - A.y * B.x

  def triangulate(self):
      n = len(self.points)
      self.sorted = self.sortByX(self.sorted,0,n-1) # ordenar puntos en funcion de x (menor a mayor)
      
      # crear envolvente convexa
      # parte inferior
      
      for i in range(n):
        while len(self.edges) >=2:
            j = len(self.edges) - 2
            k = len(self.edges) - 1
            A = self.sorted[self.edges[j].a] # obtener (*a*,b)
            B = self.sorted[self.edges[j].b] 
            C = self.sorted[self.edges[k].b] 
            
            if self.crossProduct( Point2D(B.x - A.x, B.y - A.y), Point2D(C.x - B.x, C.y - B.y) ) > 0:
                break # romper ciclo
            
            self.edges.pop()# remover el ultimo elemento

        self.edges.append( Edge( len(self.edges), i ) )
      
      lower = len(self.edges)
      
      i = n -2
      t = lower + 1
      # parte superior
      while i >= 0:
          while len(self.edges) >= t:
              j = len(self.edges) -2
              k = len(self.edges) -1
              A = self.sorted[self.edges[j].a] # obtener (*a*,b)
              B = self.sorted[self.edges[j].b] 
              C = self.sorted[self.edges[k].b]
              if np.cross( Point2D(B.x - A.x, B.y - A.y).arr(), Point2D(C.x - B.x, C.y - B.y).arr() ) > 0:
                break # romper ciclo
            
              self.edges.pop() # remover el ultimo elemento

          self.edges.append( Edge( i,  len(self.edges)) )

          i-=1
          
      self.edges.pop() # remover duplicados 
      self.hull = self.edges.copy() # almacenar envolvente
      
      # triangular
      ...
      
  # Implementación de quick sort para puntos
  
  def sortByX(self, points: list, start: int, end: int):
      # particion de puntos por quick sort
      def partition(points: list, start: int, end: int):
          pivot = points[end] # el ultimo elemento sera nuestro pivote
          i = start - 1
          for j in range(start,end): # [start, end) | ordenar de menor a mayor
              if points[j].x <= pivot.x:
                  i+=1
                  temp = points[i] 
                  points[i] = points[j]
                  points[j] = temp
                  
          temp = points[i+1]
          points[i+1] = points[end]
          points[end] = temp
          return i+1 # retornar nuevo pivote
      
      if start >= end: # solo hay un elemento en el arreglo
          return points
      
      pivot = partition(points, start, end) # obtener pivote y particionar
      
      self.sortByX(points, start, pivot - 1) # volver a particionar pero para el lado izquierdo
      self.sortByX(points, pivot+1, end) # volver a particionar pero para el lado derecho
      return points