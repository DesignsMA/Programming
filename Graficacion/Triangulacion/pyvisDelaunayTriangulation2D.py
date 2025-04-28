from pyvis.network import Network
import numpy as np
import random
# clases de utilidad
class Edge():
    def __init__(self, a: int = 0, b: int = 0):
        """Representación de un lado entre índices de puntos."""
        self.a = a
        self.b = b
    def __repr__(self):
        return f"Edge({self.a}, {self.b})"
    def tuple(self):
        return (self.a, self.b)

class Point2D():
    """Punto en 2D con utilidades básicas."""
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"
    def distance_to(self, other):
        return np.hypot(self.x - other.x, self.y - other.y)
    def arr(self):
        return np.array([self.x, self.y], dtype=np.float64)
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

class Triangle():
    """Triángulo definido por tres índices de vértices."""
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
    def vertices(self):
        return (self.a, self.b, self.c)
    def contains_vertex(self, idx):
        return idx in (self.a, self.b, self.c)      

# clase que maneja la lógica de la triangulación
class DelaunayTriangulation():
  
  def __init__(self, points: list):
      self.points = points
      self.sorted = points.copy()
      self.edges = []
      self.hull = []
      self.circumcenters = []

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

  def _circumcenter(self, A: Point2D, B: Point2D, C: Point2D):
        """Calcula circuncentro y radio del triángulo ABC."""
        ax, ay =  A.x, A.y
        bx, by = B.x, B.y
        cx, cy = C.x, C.y
        d = 2 * (ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))
        if abs(d) < 1e-12:
            return None, None
        ux = ((ax*ax + ay*ay)*(by - cy) + (bx*bx + by*by)*(cy - ay) + (cx*cx + cy*cy)*(ay - by)) / d
        uy = ((ax*ax + ay*ay)*(cx - bx) + (bx*bx + by*by)*(ax - cx) + (cx*cx + cy*cy)*(bx - ax)) / d
        center = Point2D(ux, uy)
        radius = center.distance_to(A)
        return center, radius

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
      # --- DELAUNAY TRIANGULATION (Bowyer-Watson) ---
      # Preparamos triángulo super
      min_x = min(p.x for p in self.sorted)
      max_x = max(p.x for p in self.sorted)
      min_y = min(p.y for p in self.sorted)
      max_y = max(p.y for p in self.sorted)
      dmax = max(max_x-min_x, max_y-min_y) * 10
      mid_x, mid_y = (min_x+max_x)/2, (min_y+max_y)/2
      super_pts = [Point2D(mid_x-dmax, mid_y-dmax), Point2D(mid_x, mid_y+dmax), Point2D(mid_x+dmax, mid_y-dmax)]
      base_index = len(self.sorted)
      self.sorted.extend(super_pts)
      # Triángulo inicial
      triangles = [Triangle(base_index, base_index+1, base_index+2)]
      # Para cada punto original
      for i in range(n):
          bad = []
          p = self.sorted[i]
          for t in triangles:
              A, B, C = self.sorted[t.a], self.sorted[t.b], self.sorted[t.c]
              if self.insideCircle(A, B, C, p):
                  bad.append(t)
          # recolectar bordes del hueco
          poly = []
          for t in bad:
              for ea, eb in [(t.a,t.b), (t.b,t.c), (t.c,t.a)]:
                  edge = Edge(min(ea,eb), max(ea,eb))
                  poly.append(edge)
          # eliminar triángulos inválidos
          triangles = [t for t in triangles if t not in bad]
          # bordes únicos
          unique = [e for e in poly if poly.count(e) == 1]
          # re-triangular hueco
          for e in unique:
              triangles.append(Triangle(e.a, e.b, i))
      # eliminar triángulos con vértices del supertriángulo
      triangles = [t for t in triangles if not any(v>=base_index for v in t.vertices())]
      # vaciar lista de edges y circuncentros
      self.edges.clear()
      self.circumcenters.clear()
      edge_set = set()
      for t in triangles:
          A, B, C = (self.sorted[j] for j in t.vertices())
          center, radius = self._circumcenter(A, B, C)
          if center is not None:
              self.circumcenters.append((center, radius))
          for ea, eb in [(t.a,t.b),(t.b,t.c),(t.c,t.a)]:
              edge_set.add((min(ea,eb), max(ea,eb)))
      self.edges = [Edge(a,b) for a,b in edge_set]
      # fin de triangulación
      return
      
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
    