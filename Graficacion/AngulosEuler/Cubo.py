from bezierSurface import *
import numpy as np
from cilinder2 import CilinderMesh
from disc import DiscMesh
from math import *

import matplotlib.patches as mpatches
class FigureSpace:    
    def __init__(self, l: float, w: float, h: float, subdivisions: int):
        """
        Inicializa un cubo con dimensiones l (largo), w (ancho), h (altura).

        :params:
            l (float): Largo del cubo (eje X).
            w (float): Ancho del cubo (eje Y).
            h (float): Altura del cubo (eje Z).
            subdivisions (int): Subdivisiones de cada cara del cubo.
        """
        self.l = l
        self.w = w
        self.h = h
        self.labels = []
        # Definir las caras del cubo como matrices de puntos
        self.faces = {
            'inferior': np.array([[Point(0, 0, 0), Point(l, 0, 0)],
                                  [Point(0, w, 0), Point(l, w, 0)]]),

            'superior': np.array([[Point(0, 0, h), Point(l, 0, h)],
                                 [Point(0, w, h), Point(l, w, h)]]),

            'trasera': np.array([[Point(0, w, 0), Point(l, w, 0)],
                                   [Point(0, w, h), Point(l, w, h)]]),

            'frontal': np.array([[Point(0, 0, 0), Point(l, 0, 0)],
                                   [Point(0, 0, h), Point(l, 0, h)]]),

            'izquierda': np.array([[Point(0, 0, 0), Point(0, w, 0)],
                                    [Point(0, 0, h), Point(0, w, h)]]),

            'derecha': np.array([[Point(l, 0, 0), Point(l, w, 0)],
                          [Point(l, 0, h), Point(l, w, h)]])
        }
        self.subdivisions =  subdivisions
        self.meshes = {}
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.normalVector = None
    def showGraph(self):
        plt.show(block=False)
    
    def setZlim(self, n):
        self.ax.set_zlim((-n,n))
        
    def graphCube(self):
        self.meshes = {}
        self.ax.set_zlim((-4,4))
        self.ax.set_box_aspect([1,1,1])
        for key, face in self.faces.items():
            mesh = BezierSurface(face, self.subdivisions)
            mesh.generateMesh()
            self.meshes.update([(key, mesh.mesh)])

            ptx = np.array([point.x for point in mesh.mesh])
            pty = np.array([point.y for point in mesh.mesh])
            ptz = np.array([point.z for point in mesh.mesh])        

            ptX = ptx.reshape(self.subdivisions+1, self.subdivisions+1)
            ptY = pty.reshape(self.subdivisions+1, self.subdivisions+1)
            ptZ = ptz.reshape(self.subdivisions+1, self.subdivisions+1)

            # Aplicar gradiente de colores a la superficie
            self.ax.plot_surface(ptX, ptY, ptZ, color='red',rstride=1, cstride=1, alpha=0.3)       
            # Trazar la malla de alambre
            self.ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)

            self.ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos
    
        # Configurar los ejes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
    
    def addGraph(self, mesh, subdivisions, color:str = 'orange'):
        ptx = np.array([point.x for point in mesh])
        pty = np.array([point.y for point in mesh])
        ptz = np.array([point.z for point in mesh])

        ptX = ptx.reshape(subdivisions,subdivisions)
        ptY = pty.reshape(subdivisions,subdivisions)
        ptZ = ptz.reshape(subdivisions,subdivisions)
        
        surface =self.ax.plot_surface(ptX, ptY, ptZ, color=color,rstride=1, cstride=1, alpha=0.4)       
        # Trazar la malla de alambre
        wireframe =self.ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)
        scatter = self.ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos
        self.ax.set_box_aspect([1,1,1])
        return surface, wireframe, scatter
    
    def normalVectorToFace(self, face: str = 'frontal'):
        cara = self.faces[face]
        self.normalVector = self.normalToSurface(cara[0,0], cara[0,1], cara[1,0], l=2, lnw=2, txt="cubo")
        print("Vector normal a la cara ",face, " : ", self.normalVector)
    
    def normalToSurface(self, p1:Point, p2:Point, p3:Point, color: str = 'blue', l: float = 1, lnw: float = 1, txt: str =None, center: Point = Point(0,0,0) ):
        v1 = np.array([p2.x - p1.x, p2.y - p1.y, p2.z - p1.z])
        v2 = np.array([p3.x - p1.x, p3.y - p1.y, p3.z - p1.z])
        normal = np.cross(v1, v2)        # Normalizar la normal para evitar problemas de escala, magnitud 1
        normal = normal / np.linalg.norm(normal)
        # Graficar la normal trasladada al origen
        
        self.ax.scatter([p1.x,p2.x,p3.x], [p1.y,p2.y,p3.y], [p1.z,p2.z,p3.z], color=color, s=70)
        self.ax.quiver(center.arr()[0], center.arr()[1], center.arr()[2], normal[0], normal[1], normal[2], length=l, color=color, linewidth=lnw,)

        if txt is not None:
            self.createLabel("Normal al "+txt, color)

        return Point(normal[0], normal[1], normal[2])

    def createLabel(self, txt, color):
            color_patch = mpatches.Patch(color=color, label=txt)
            self.labels.append(color_patch)
            self.ax.legend(handles=self.labels, loc=(1,1))

## Main
cube = FigureSpace(20,20,1,1)
cube.normalVectorToFace('superior')

r = 10
divisions = 10
cilinder = CilinderMesh(r, height=1, subdivisions=divisions) # cilindro de 10x1
cilinder.generateMesh()
disc = DiscMesh(10, divisions)
disc.generateMesh()
cilinderFig = [*cube.addGraph(cilinder.mesh, divisions)]
discFig = [*cube.addGraph(disc.mesh, divisions)]
cube.graphCube()

p1 = Point(10,0,0)
p2 = Point(r*cos(120), r*sin(120), 0)
p3 = Point(r*cos(240),  r*sin(240), 0)
normalDisco = cube.normalToSurface( p1, p2, p3, 'green', 2.2, 2, "disco")
print(f"Vector normal al disco: {normalDisco}")
cube.showGraph()
# cambiando alturas del disco

input("Presione para modificar z en disco... ")
p1.z = 0
p2.z = 1
p3.z = 1
normalDiscoModificada = cube.normalToSurface( p1, p2, p3, '#3ffdff', 3, 2, "disco modificado")
print(f"Vector normal al disco modificado: {normalDiscoModificada}")

input("Presione para mostrar disco y cilindro rotado...")
# Encontrar el eje y ángulo de rotación
eje_rotacion = np.cross(normalDisco.arr(), normalDiscoModificada.arr())
eje_rotacion /= np.linalg.norm(eje_rotacion)
angulo_rotacion = np.arccos(np.clip(np.dot(normalDisco.arr(), normalDiscoModificada.arr()), -1.0, 1.0))
# Rotar cada punto del disco y cilindro
for pt, pt2 in zip(disc.mesh, cilinder.mesh):
    if isinstance(pt, Point):
        pt.rotate_point(pt, eje_rotacion, angulo_rotacion)
        pt2.rotate_point(pt2, eje_rotacion, angulo_rotacion)
        
for fig, fig2 in zip(cilinderFig, discFig):
    fig.remove()
    fig2.remove()

cilinderFig2 = [*cube.addGraph(cilinder.mesh, divisions, '#3ffdff')]
discFig2 = [*cube.addGraph(disc.mesh, divisions, '#3ffdff')]
cube.createLabel("Figura rotada", '#3ffdff')
cube.graphCube()

input("Presione para deshacer rotaciones...")
# Obtener la normal de referencia (estado original)
normalFirme = cube.normalVector

# Calcular el ángulo entre los planos
anguloPlanos = degrees(np.arccos(
    abs(np.dot(normalDiscoModificada.arr(), normalFirme.arr())) /
    (normalDiscoModificada.norm()*normalFirme.norm())
))

print(f"Ángulo entre planos: {anguloPlanos}°")

# Calcular los ángulos de Euler
cos_phi = normalDiscoModificada.z / normalDiscoModificada.norm()
phi = np.arccos(np.clip(cos_phi, -1.0, 1.0))  # Clip para evitar errores numéricos

# Ángulo de rotación en el plano XY
theta = np.arctan2(normalDiscoModificada.y, normalDiscoModificada.x)

# Crear las matrices de rotación inversas
R_y_inv = Point.rotation_matrix_y(-degrees(phi))  # Deshacer la inclinación
R_z_inv = Point.rotation_matrix_z(-degrees(theta))  # Deshacer la rotación en XY

# Multiplicar en el orden correcto
R_total_inv = np.dot(R_y_inv, R_z_inv)

print("Matriz de rotación inversa:")
print(R_total_inv)

for fig, fig2 in zip(cilinderFig2, discFig2):
    fig.remove()
    fig2.remove()

# Aplicar la rotación inversa a cada punto
for pt, pt2 in zip(cilinder.mesh, disc.mesh):
    if isinstance(pt, Point) and isinstance(pt2, Point):
        pt.rotateWithMatrix(R_total_inv)  # Desrotar cada punto
        pt2.rotateWithMatrix(R_total_inv)  # Desrotar cada punto
        
cilinderFig2 = [*cube.addGraph(cilinder.mesh, divisions, '#8bff7e')]
discFig2 = [*cube.addGraph(disc.mesh, divisions, '#8bff7e')]
cube.createLabel("Figura des-rotada", '#8bff7e')

input("Cerrar.")
