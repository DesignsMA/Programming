from pyvis.network import Network
import numpy as np
import random
# clases de utilidad
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
      "Retorna el equivalente en numpy array."
      return np.array([self.x,self.y], dtype=np.float64) # retornar arreglo de tipo float64
  
  def __eq__(self, other):
      return self.x == other.x and self.y == other.y
  
  def __hash__(self):
      return hash((self.x, self.y))
class Triangle():
    
    def __init__(self, A: Point2D, B: Point2D, C: Point2D):
        """Inicializa un triángulo con tres puntos 2D.
        
        Args:
            A: Primer vértice del triángulo
            B: Segundo vértice del triángulo
            C: Tercer vértice del triángulo
        """
        self.A = A
        self.B = B
        self.C = C
        self.circumcenter = None  # Centro del circuncírculo
        self.radius = None          # Radio del circuncírculo
        self._circumcircle_valid = False             # Bandera de validación
        self.edges = frozenset({frozenset({self.A, self.B}), 
                               frozenset({self.B, self.C}), 
                               frozenset({self.C, self.A})})
    def _calculate_circumcircle(self):
        a = self.B.distance_to(self.C)
        b = self.A.distance_to(self.C)
        c = self.A.distance_to(self.B)
        
        if self.is_degenerate:
            self._circumcircle_valid = False
            return False
            
        a2, b2, c2 = a*a, b*b, c*c
        sum_weights = a2*(b2 + c2 - a2) + b2*(a2 + c2 - b2) + c2*(a2 + b2 - c2)
        
        if abs(sum_weights) < 1e-10:
            self._circumcircle_valid = False
            return False
            
        wx = a2*(b2 + c2 - a2)*self.A.x + b2*(a2 + c2 - b2)*self.B.x + c2*(a2 + b2 - c2)*self.C.x
        wy = a2*(b2 + c2 - a2)*self.A.y + b2*(a2 + c2 - b2)*self.B.y + c2*(a2 + b2 - c2)*self.C.y
        
        self.circumcenter = Point2D(wx / sum_weights, wy / sum_weights)
        self.radius = self.circumcenter.distance_to(self.A)
        self._circumcircle_valid = True
        return True
    
    def get_circumcircle(self):
        if not self._circumcircle_valid:
            self._calculate_circumcircle()
        return self.circumcenter, self.radius
    
    def point_in_circumcircle(self, point: Point2D):
        if not self._circumcircle_valid:
            if not self._calculate_circumcircle():
                return False
        
        if self.circumcenter is None or self.radius is None:
            return False
            
        distance_sq = (point.x - self.circumcenter.x)**2 + (point.y - self.circumcenter.y)**2
        return distance_sq <= (self.radius**2 + 1e-10)
        
    @property
    def is_degenerate(self) -> bool:
        area = 0.5 * abs((self.B.x - self.A.x)*(self.C.y - self.A.y) - 
                         (self.B.y - self.A.y)*(self.C.x - self.A.x))
        return area < 1e-10
        
    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return {self.A, self.B, self.C} == {other.A, other.B, other.C}
    
    def __hash__(self):
        return hash((frozenset({self.A, self.B, self.C})))
# clase que maneja la lógica de la triangulación
class DelaunayTriangulation():
  
  def __init__(self, points: list):
      self.points = points
      self.sorted = points.copy()
      self.hull = []
      self.triangles = []  # Almacenará triángulos
      self.super_triangle = None  # Triángulo inicial que contiene todos los puntos
  
  def bowyer_watson(self):
        self.triangles = []
        self.super_triangle = self.superTriangle()
        self.triangles.append(self.super_triangle)
        
        for point in self.points:
            bad_triangles = []
            
            # Encontrar todos los triángulos cuyo circuncírculo contiene el punto
            for triangle in self.triangles:
                if triangle.point_in_circumcircle(point):
                    bad_triangles.append(triangle)
            
            # Encontrar el polígono formado por las aristas únicas
            polygon_edges = []
            for triangle in bad_triangles:
                for edge in triangle.edges:
                    # Si la arista es compartida con otro triángulo malo, no es parte del polígono
                    shared = False
                    for other in bad_triangles:
                        if triangle == other:
                            continue
                        if edge in other.edges:
                            shared = True
                            break
                    if not shared:
                        polygon_edges.append(edge)
            
            # Eliminar los triángulos malos
            for triangle in bad_triangles:
                if triangle in self.triangles:
                    self.triangles.remove(triangle)
            
            #  Crear nuevos triángulos desde el punto a cada arista del polígono
            for edge in polygon_edges:
                edge_points = list(edge)
                new_triangle = Triangle(edge_points[0], edge_points[1], point)
                self.triangles.append(new_triangle)
        
        # Eliminar triángulos que comparten vértices con el supertriángulo
        super_vertices = {self.super_triangle.A, self.super_triangle.B, self.super_triangle.C}
        self.triangles = [
            t for t in self.triangles 
            if not ({t.A, t.B, t.C} & super_vertices)
        ]
      
  def superTriangle(self):      
    xMin = yMin =  float('inf')  # Inicializar con infinito
    xMax = yMax = float('-inf')
    for p in self.points:
        if p.x < xMin:
            xMin = p.x
        if p.y < yMin:
            yMin = p.y
            
        if p.x > xMax:
            xMax = p.x
        if p.y > yMax:
            yMax = p.y
    
    margen = 10*max(xMax -xMin, yMax -yMin)
    v1 = Point2D( xMin - margen, yMin-margen)
    v2 = Point2D( xMax + margen, yMin -margen)
    v3 = Point2D( (xMin + xMax)/2, yMax + margen )
    return Triangle(v1,v2,v3)

  
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