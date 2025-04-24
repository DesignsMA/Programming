from pyvista import *
import numpy as np
from numpy.random import random
from time import sleep
from abc import ABC, abstractmethod
    
class SphereObject():
    
    def __init__(self, p: np.array, dp: np.array, r:float = 2.0,  res: int = 20, color: str = 'red'):
        """
          Inicializa una esfera con sus atributos para su uso en una simulación.

          Args:
              p (np.ndarray): Posición actual de la esfera en el espacio (centro).
              dp (np.ndarray): Vector de desplazamiento que indica la dirección hacia donde se dirige la esfera.
              r (float): Radio de la esfera. Por defecto es 2.0.
              res (int, optional): Resolución de la malla (número de divisiones angulares). Por defecto es 20.
              color (str): Color de la esfera. Por defecto es 'red'.
        """
        self.r = r
        self.color = color
        self.mesh = Sphere(radius=r, center=p, direction=dp, theta_resolution=res, phi_resolution=res)
        self.p = p
        self.dp = dp
    
    def move(self):
        """
            Actualiza la posición de la esfera de acuerdo a su desplazamiento | No actualiza la vista.
            
        """
        self.p += self.dp # actualizar posición
        self.mesh.translate(self.dp, inplace=True)  # Actualiza la malla

    # Tipos de colisión
    
    def bounce(self, normal: np.array):
        """Invierte la dirección basado en la normal de la superficie colisionada."""
        self.dp = -self.dp  # Simple, para paredes planas
        
class Container(ABC):
    def __init__(self, mesh):
        self.mesh = mesh
    
    @abstractmethod
    def check_collision(self, sphere: SphereObject) -> np.array:
        """Retorna la normal de la superficie colisionada (o None si no hay colisión)."""
        pass
    
class BoxContainer(Container):
    def __init__(self, bound: float):
        bounds = (-bound, bound, -bound, bound, -bound, bound) # limites
        super().__init__(Box(bounds=bounds)) # inicializar malla
        self.bound = bound # limite general
    
    def check_collision(self, sphere: SphereObject) -> np.array:
        normal = np.zeros(3)
        collided = False
        
        # Verificar colisión con cada cara del cubo
        for i in range(3):  # Ejes X, Y, Z
            if sphere.p[i] - sphere.r <= -self.bound:
                normal[i] = 1.0  # Normal hacia afuera de la cara negativa
                collided = True
            elif sphere.p[i] + sphere.r >= self.bound:
                normal[i] = -1.0  # Normal hacia afuera de la cara positiva
                collided = True
        
        return normal if collided else None

class CylinderContainer(Container):
    def __init__(self, radius: float, height: float):
        super().__init__(Cylinder(radius=radius, height=height))
        self.radius = radius
        self.height = height
    
    def check_collision(self, sphere: SphereObject) -> np.array:
        normal = np.zeros(3)
        collided = False
        
        # Colisión con la pared lateral (XZ)
        dist_xz = np.sqrt(sphere.p[0]**2 + sphere.p[2]**2)
        if dist_xz + sphere.r >= self.radius:
            normal[0] = sphere.p[0] / dist_xz  # Normal radial en X
            normal[2] = sphere.p[2] / dist_xz  # Normal radial en Z
            collided = True
        
        # Colisión con las tapas (Y)
        if sphere.p[1] - sphere.r <= -self.height/2:
            normal[1] = 1.0  # Normal de la tapa inferior
            collided = True
        elif sphere.p[1] + sphere.r >= self.height/2:
            normal[1] = -1.0  # Normal de la tapa superior
            collided = True
        
        return normal if collided else None

class TorusContainer(Container):
    def __init__(self, major_radius: float, minor_radius: float):
        super().__init__(ParametricTorus(ringradius=major_radius, crosssectionradius=minor_radius))
        self.major_r = major_radius
        self.minor_r = minor_radius
    
    def check_collision(self, sphere: SphereObject) -> np.array:
        # Distancia al centro del anillo (plano XZ)
        dist_xz = np.sqrt(sphere.p[0]**2 + sphere.p[2]**2)
        closest_x = (self.major_r * sphere.p[0]) / dist_xz if dist_xz > 0 else 0
        closest_z = (self.major_r * sphere.p[2]) / dist_xz if dist_xz > 0 else 0
        
        # Punto más cercano en el toro
        closest_point = np.array([closest_x, sphere.p[1], closest_z])
        
        # Vector desde el punto más cercano a la esfera
        collision_vector = sphere.p - closest_point
        distance = np.linalg.norm(collision_vector)
        
        if distance <= sphere.r + self.minor_r:
            normal = collision_vector / distance  # Normal unitaria
            return normal
        return None
class PhysicsSimulator():
    
    def __init__(self, plotter: Plotter, container: str = ['cube', 'cilinder', 'torus']):
        self.plot = plotter
        self.containerType = container
        self.initContainer()
        self.spheres = []
        self.running = False
    
    def initContainer(self):
        self.container = Box(bounds=(-10,10,-10,10,-10,10))
        pass

    def checkContainerCollision(self, sphere: SphereObject):
        pass
        
        
    def checkSphereCollision(self, sphere1: SphereObject, sphere2: SphereObject):
        pass

    def runSimulation(self):
        while True:
            for sphere in self.spheres:
                sphere.move()
                self.checkContainerCollision(sphere)
                self.checkSphereCollision(sphere, other_spheres)
            plotter.update()
            sleep(0.05)
    
set_plot_theme('dark')
plotter = Plotter()

simulator = PhysicsSimulator(plotter=plotter, container='cube')

plotter.add_key_event(" ", lambda: simulator.runSimulation)
