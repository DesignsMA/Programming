from __future__ import annotations
import pyvista as pv # Se usa una API de alto nivel para vtk con el fín de simplificar procesos
import numpy as np
from math import cos, sin, sqrt
import time
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def arr(self):
        return np.array([self.x, self.y, self.z])
    
    def norm(self):
        return np.linalg.norm(self.arr())
    
    @staticmethod
    def rotation_matrix_z(theta_deg):
        """Matriz de rotación alrededor del eje Z"""
        theta = np.radians(theta_deg)
        return np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
    
    @staticmethod
    def rotation_matrix_y(theta_deg):
        """Matriz de rotación alrededor del eje Y"""
        theta = np.radians(theta_deg)
        return np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
    
    def rotateWithMatrix(self, rotation_matrix):
        """Aplica una matriz de rotación al punto"""
        rotated = np.dot(rotation_matrix, self.arr())
        self.x, self.y, self.z = rotated[0], rotated[1], rotated[2]
        
def normalToSurface(p1: tuple, p2: tuple, p3: tuple) -> tuple:
    """
    Calcula el vector normal unitario a un plano definido por tres puntos.
    
    Args:
        p1, p2, p3: Tuplas con coordenadas (x, y, z) de los puntos que definen el plano
        
    Returns:
        tuple: Vector normal normalizado (nx, ny, nz)
    """
    # Convertir puntos a arrays numpy
    p1_arr = np.array(p1)
    p2_arr = np.array(p2)
    p3_arr = np.array(p3)
    
    # Calcular vectores del plano
    v1 = p2_arr - p1_arr
    v2 = p3_arr - p1_arr
    
    # Calcular producto vectorial (normal)
    normal = np.cross(v1, v2)
    
    # Normalizar el vector (magnitud 1)
    normal = normal / np.linalg.norm(normal)
    
    # Retornar como tupla
    return tuple(normal)

# Cada intancia retorna la polydata de las figuras
disc = pv.Disc(outer=10, c_res=100, inner=0) # centro en 0,0,0
box = pv.Box(bounds=(0,20,0,20,0,1))

p1 = (10,0,0) #puntos del disco
p2 = (10*cos(120), 10*sin(120), 0)
p3 = (10*cos(240),  10*sin(240), 0)
normalDisco = normalToSurface(p1,p2,p3)

# Obtener los puntos de la cara superior (z = 1)
# Los puntos de una caja en PyVista están ordenados en un patrón específico
points = box.points

# Los puntos de la cara superior son los últimos 4 puntos en el array de puntos de la caja
# (PyVista organiza los puntos de la caja en un orden particular)
p1 = tuple(points[4])  # (20, 0, 1)
p2 = tuple(points[5])  # (20, 20, 1)
p3 = tuple(points[6])  # (0, 20, 1)

# Calcular la normal usando tu función
normal = normalToSurface(p1, p2, p3)

p = pv.Plotter() # dividiendo en malla de 3 x 3
# Top row
p.subplot(0, 0)
p.add_mesh(disc, color='#53ff53', show_edges=True, use_transparency=True, opacity=0.6) # añade mesh al subplot
p.add_mesh(box, color='ff5353', show_edges=True) # añade mesh al subplot

# Mostrar la normal como una flecha
arrow = pv.Arrow(
    direction=normalDisco,
    scale=10,  # Longitud de la fslecha
    shaft_radius=0.01,
    tip_radius=0.03,
    tip_length=0.1
)
p.add_mesh(
    arrow,
    color="green",
    label=f"Normal: {np.round(normalDisco, 2)}"
)

# Mostrar la normal como una flecha
arrow = pv.Arrow(
    direction=normal,
    scale=18,  # Longitud de la fslecha
    shaft_radius=0.01,
    tip_radius=0.03,
    tip_length=0.1
)
p.add_mesh(
    arrow,
    color="red",
    label=f"Normal: {np.round(normal, 2)}"
)

p1 = (10,0,0) #puntos del disco
p2 = (10*cos(120), 10*sin(120), 1)
p3 = (10*cos(240),  10*sin(240), 1)
normalDiscoModificada = normalToSurface(p1,p2,p3)

arrow = pv.Arrow(
    direction=normalDiscoModificada,
    scale=10,  # Longitud de la fslecha
    shaft_radius=0.01,
    tip_radius=0.03,
    tip_length=0.1
)
p.add_mesh(
    arrow,
    color="purple",
    label=f"Normal Modificada: {np.round(normalDiscoModificada, 2)}"
)

# Normalizar vectores
normalDiscoModificada = np.array(normalDiscoModificada) / np.linalg.norm(normalDiscoModificada)
normalFirme = np.array(normal) / np.linalg.norm(normal)

eje_rotacion = np.cross(np.array(normalDisco), np.array(normalDiscoModificada))
eje_rotacion /= np.linalg.norm(eje_rotacion)
angulo_rotacion = np.arccos(np.clip(np.dot(np.array(normalDisco), np.array(normalDiscoModificada)), -1.0, 1.0))


discRotated = disc.copy()
discRotated.rotate_vector(eje_rotacion,np.degrees(angulo_rotacion), inplace=True)

p.add_mesh(discRotated, color='#ff5399', show_edges=True) # añade mesh al subplot
# Definir normales (ejemplo)
normalFirme = Point(normal[0], normal[1], normal[2])  # Normal de la cara superior del cubo
# Normalizar vector objetivo
normalDiscoModificada_norm = normalDiscoModificada

# Calcular ángulo entre planos
anguloPlanos = np.degrees(np.arccos(
    np.clip(np.dot(normalDiscoModificada_norm, normalFirme.arr()), -1.0, 1.0)
))
print(f"Ángulo entre planos: {anguloPlanos:.2f}°")

# Calcular ángulos de Euler
theta = np.arctan2(normalDiscoModificada_norm[1], normalDiscoModificada_norm[0])  # Rotación en XY
phi = np.arccos(np.clip(normalDiscoModificada_norm[2], -1.0, 1.0))  # Inclinación

# Crear matrices de rotación directa
R_z = Point.rotation_matrix_z(np.degrees(theta))
R_y = Point.rotation_matrix_y(np.degrees(phi))
R_total = np.dot(R_y, R_z)

# Rotar el disco
discRotated = disc.copy()
discRotated.points = np.dot(discRotated.points, R_total.T)  # Rotación directa

# Crear matrices de rotación inversa
R_y_inv = Point.rotation_matrix_y(-np.degrees(phi))
R_z_inv = Point.rotation_matrix_z(-np.degrees(theta))
R_total_inv = np.dot(R_z_inv, R_y_inv)  # Orden inverso

# Desrotar el disco
discDef = discRotated.copy()
discDef.points = np.dot(discDef.points, R_total_inv.T)  # Desrotación

p.add_mesh(discDef, color='red', show_edges=True, opacity=0.5, edge_color='purple') # añade mesh al subplot


p.add_legend()
p.show()