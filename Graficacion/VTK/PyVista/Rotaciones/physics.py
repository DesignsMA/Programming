import pyvista as pv
import numpy as np
from time import sleep
from abc import ABC, abstractmethod
from random import random

class SphereObject():
    def __init__(self, p: np.array, dp: np.array, r: float = 1.0, res: int = 20, color: str = 'red'):
        self.r = r
        self.color = color
        self.p = np.array(p, dtype=np.float64)
        self.dp = np.array(dp, dtype=np.float64)
        self.mesh = pv.Sphere(radius=r, center=self.p, theta_resolution=res, phi_resolution=res)
    
    def move(self):
        self.p += self.dp
        self.mesh.translate(self.dp, inplace=True)

    def bounce(self):
        """Simple bounce by reversing direction"""
        self.dp = -self.dp


class Container(ABC):
    def __init__(self, mesh):
        self.mesh = mesh
        self.center = np.array([0, 0, 0])
        self.rotation_matrix = np.eye(3)  # Identity matrix initially
    
    def rotate(self, angle: float, axis: str):
        """Rotate the container and update rotation matrix"""
        if axis == 'x':
            self.mesh.rotate_x(angle, inplace=True)
            theta = np.radians(angle)
            rot = np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])
        elif axis == 'y':
            self.mesh.rotate_y(angle, inplace=True)
            theta = np.radians(angle)
            rot = np.array([
                [np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)]
            ])
        elif axis == 'z':
            self.mesh.rotate_z(angle, inplace=True)
            theta = np.radians(angle)
            rot = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])
        
        self.rotation_matrix = rot @ self.rotation_matrix
    
    @abstractmethod
    def check_collision(self, sphere: SphereObject) -> bool:
        pass

class BoxContainer(Container):
    def __init__(self, bound: float):
        bounds = (-bound, bound, -bound, bound, -bound, bound)
        super().__init__(pv.Box(bounds=bounds))
        self.bound = bound
    
    def check_collision(self, sphere: SphereObject) -> bool:
        # Transform to local coordinates
        local_pos = self.rotation_matrix.T @ (sphere.p - self.center)
        
        # Check against local bounds
        umbral = 0.01
        for i in range(3):
            if abs(local_pos[i]) + sphere.r + sphere.r*umbral  >= self.bound:
                return True
        return False

class CylinderContainer(Container):
    def __init__(self, radius: float, height: float):
        # Orientar el cilindro en el eje X
        super().__init__(pv.Cylinder(center=(0, 0, 0), direction=(1, 0, 0), radius=radius, height=height, resolution=20))
        self.radius = radius
        self.height = height  # total length along X axis

    def check_collision(self, sphere: SphereObject) -> bool:
        # Transformar a coordenadas locales (considerando rotación)
        local_pos = self.rotation_matrix.T @ (sphere.p - self.center)
        x, y, z = local_pos
        s = sphere.r

        # Margen de seguridad
        margin = 0.01 * s

        # Colisión con paredes laterales (radio en eje Z)
        dist_to_axis = np.sqrt(y**2 + z**2)
        wall_collision = (dist_to_axis + s + margin) > self.radius

        # Colisión con extremos en X
        top_collision = (x + s + margin) > (self.height / 2)
        bottom_collision = (x - s - margin) < (-self.height / 2)

        return wall_collision or top_collision or bottom_collision
    
class TorusContainer(Container):
    def __init__(self, major_radius: float, minor_radius: float):
        torus = pv.ParametricTorus(ringradius=major_radius, crosssectionradius=minor_radius)
        super().__init__(torus)
        self.major_r = major_radius
        self.minor_r = minor_radius
        print(self.rotation_matrix)
    
    def rotate(self, angle: float, axis: str):
        """Rotate the container and update rotation matrix"""
        if axis == 'x':
            self.mesh.rotate_x(angle, inplace=True)
            theta = np.radians(angle)
            rot = np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])
        elif axis == 'y':
            self.mesh.rotate_y(angle, inplace=True)
            theta = np.radians(angle)
            rot = np.array([
                [np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)]
            ])
        elif axis == 'z':
            self.mesh.rotate_z(angle, inplace=True)
            theta = np.radians(angle)
            rot = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])
        
        self.rotation_matrix = self.rotation_matrix @ rot

    def check_collision(self, sphere: SphereObject) -> bool:
        # Transformar a coordenadas locales con rotación actual
        local_pos = self.rotation_matrix.T @ (sphere.p - self.center)
        x, y, z = local_pos
    
        R = self.major_r
        r = self.minor_r
        s = sphere.r
    
        # Distancia al eje central del toro
        d = np.sqrt(x**2 + y**2)
        distance_sq = (d - R)**2 + z**2
    
        # Margen de seguridad para evitar atascamientos
        margin = 0.16 * s  # 5% del radio de la esfera
        
        # Condición de colisión mejorada
        return ((r - s - margin)**2 <= distance_sq <= (r + s + margin)**2) and \
               (R - r - s - margin < d < R + r + s + margin)
               
class PhysicsSimulator():
    def __init__(self, plotter: pv.Plotter, container: str = 'cube', nspheres: int = 2, rsphere: float = 0.8):
        self.plotter = plotter
        self.container = self._init_container(container)
        self.spheres = []
        self.running = False
        self.current_rotations = np.array([0.0, 0.0, 0.0])  # Track rotations in X,Y,Z
        
        for _ in range(nspheres):
            if isinstance(self.container, BoxContainer):
                bound = self.container.bound
                p = np.random.uniform(-bound + 2, bound - 2, 3)  # 2 = sphere radius
            elif isinstance(self.container, CylinderContainer):
                radius = self.container.radius - rsphere
                half_length = self.container.height / 2 - rsphere

                # Posición aleatoria dentro del cilindro (eje X, radio en Z-Y)
                for _ in range(nspheres):
                    theta = np.random.uniform(0, 2*np.pi)
                    r = np.random.uniform(0, radius)
                    x = np.random.uniform(-half_length, half_length)
                    y = r * np.cos(theta)
                    z = r * np.sin(theta)
                    p = np.array([x, y, z])
            
            elif isinstance(self.container, TorusContainer):
                major_r = self.container.major_r
                minor_r = self.container.minor_r
                
                for _ in range(nspheres):
                    theta = np.random.uniform(0, 2*np.pi)
                    
                    phi = np.random.uniform(0, 2*np.pi)
                    
                    tube_r = np.random.uniform(0.2*minor_r, 0.8*minor_r)
                    
                    p = np.array([
                        (major_r + tube_r * np.cos(phi)) * np.cos(theta),
                        (major_r + tube_r * np.cos(phi)) * np.sin(theta),
                        tube_r * np.sin(phi)
                    ])
                    
            dp = np.random.uniform(-1, 1, 3)
            dp = dp / np.linalg.norm(dp) * 0.08  # Small initial velocity
            
            # Random color
            color = np.random.choice(['red', 'green', 'blue', 'yellow', 'cyan', 'magenta'])
            
            self.spheres.append(SphereObject(p=p, dp=dp, r=rsphere, color=color, res=10))
            
    
    def _init_container(self, container_type: str) -> Container:
        if container_type == "cube":
            return BoxContainer(bound=20)
        elif container_type == "cylinder":
            return CylinderContainer(radius=20, height=40)
        elif container_type == "torus":
            return TorusContainer(major_radius=30, minor_radius=20)
        raise ValueError(f"Invalid container type: {container_type}")
    
    def run_simulation(self):
        self.running = True
        rotation_sequence = [
            (30, 'x'), (60, 'x'), (90, 'x'),
            (30, 'y'), (60, 'y'), (90, 'y'),
            (30, 'z'), (60, 'z'), (90, 'z')
        ]
        current_step = 0
        pause_counter = 0

        while self.running:
            # Handle rotations
            if pause_counter <= 0:
                if current_step < len(rotation_sequence):  # Fixed: changed <= to <
                    target_angle, axis = rotation_sequence[current_step]
                    rotation_amount = 0.010  # Degrees per frame

                    # Apply rotation
                    self.container.rotate(rotation_amount, axis)

                    # Update rotation tracker
                    if axis == 'x':
                        self.current_rotations[0] += rotation_amount
                        current_angle = self.current_rotations[0]
                    elif axis == 'y':
                        self.current_rotations[1] += rotation_amount
                        current_angle = self.current_rotations[1]
                    else:  # 'z'
                        self.current_rotations[2] += rotation_amount
                        current_angle = self.current_rotations[2]

                    # Check if target angle reached
                    if current_angle >= target_angle:
                        current_step += 1
                        pause_counter = 30  # 1.5 second pause
                else:
                    current_step = 0
                    self.current_rotations = np.array([0.0, 0.0, 0.0])
            else:
                pause_counter -= 1

            # Physics update with collision handling
            for sphere in self.spheres:
                

                # Check collision and handle
                if self.container.check_collision(sphere):
                    sphere.bounce()
                    sphere.move()


                sphere.move()
                    

                # Sphere-sphere collisions
                for other in self.spheres:
                    if other != sphere:
                        umbral = 0.015
                        distance = np.linalg.norm(sphere.p - other.p)
                        if distance < sphere.r + other.r + sphere.r*umbral:
                            # Simple bounce for both spheres
                            sphere.bounce()
                            other.bounce()
                            sphere.move()
                            other.move()
            self.plotter.update()
            sleep(0.001)
                    
# Setup and run simulation
pv.set_plot_theme('dark')
plotter = pv.Plotter()
spheres =input("Especifique el numero de esferas\n: ")
container = input("Especifique el contenedor\ntorus | cube | cylinder\n: ")
simulator = PhysicsSimulator(plotter, container=container, nspheres=int(spheres))

plotter.add_mesh(simulator.container.mesh, opacity=0.2)
for sphere in simulator.spheres:
    plotter.add_mesh(sphere.mesh, color=sphere.color)

plotter.add_key_event("1", lambda: simulator.run_simulation())
plotter.add_key_event("x", lambda: exit())
plotter.show_axes()
plotter.show()

