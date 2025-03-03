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
        
        
    def graphCube(self):
        self.meshes = {}
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
        return surface, wireframe, scatter
    
    def normalVectorToFace(self, face: str = 'frontal'):
        cara = self.faces[face]
        self.normalVector = self.normalToSurface(cara[0,0], cara[0,1], cara[1,0], l=2, lnw=2, txt="cubo")
        print("Vector normal a la cara ",face, " : ", self.normalVector)
    
    def normalToSurface(self, p1:Point, p2:Point, p3:Point, color: str = 'blue', l: float = 1, lnw: float = 1, txt: str =None, center: Point = Point(0,0,0) ):
        v1 = p2.arr() - p1.arr()
        v2 = p3.arr() - p1.arr()
        normal = np.cross(v1,v2) # producto cruz para  obtener la normal a una cara
        # Normalizar la normal para evitar problemas de escala, magnitud 1
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

class NormVector:
    @staticmethod
    def direction_cosines(pt: Point):
        """
        Calcula los cosenos directores del vector representado por el punto.

        Retorna:
            tuple: Cosenos directores (cos_alpha, cos_beta, cos_gamma).
        """
        norm = pt.norm() # magnitud del vector
        if norm == 0:
            raise ValueError("El vector no puede ser un vector nulo.")
        cos_alpha = pt.x / norm
        cos_beta = pt.y / norm
        cos_gamma = pt.z / norm
        return cos_alpha, cos_beta, cos_gamma

    @staticmethod
    def direction_angles(pt: Point):
        """
        Calcula los ángulos que forma el vector con los ejes x, y, y z.

        Retorna:
            tuple: Ángulos en grados (alpha, beta, gamma).
        """
        cos_alpha, cos_beta, cos_gamma = NormVector.direction_cosines(pt)
        alpha = degrees(acos(cos_alpha))  # Ángulo con el eje x
        beta = degrees(acos(cos_beta))    # Ángulo con el eje y
        gamma = degrees(acos(cos_gamma))  # Ángulo con el eje z
        return alpha, beta, gamma


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
normalDisco = cube.normalToSurface( p1, p2, p3, 'green', 1.8, 2, "disco", p1)
print(f"Vector normal al disco: {normalDisco}")
cube.showGraph()
# cambiando alturas del disco

input("Presione para modificar z en disco... ")
p1.z = 0
p2.z = 1
p3.z = 1
normalDiscoModificada = cube.normalToSurface( p1, p2, p3, '#3ffdff', 1.5, 2, "disco modificado", p1)
print(f"Vector normal al disco modificado: {normalDiscoModificada}")

input("Presione para mostrar disco y cilindro rotado...")
alpha, beta, gamma = NormVector.direction_cosines(normalDiscoModificada) # obtener angulos

for pt, pt2 in zip(cilinder.mesh,disc.mesh):
    if isinstance(pt, Point):
        pt.rotate(alpha, beta, gamma) # rotar cada punto
        pt2.rotate(alpha, beta, gamma) # rotar cada punto

for fig, fig2 in zip(cilinderFig, discFig):
    fig.remove()
    fig2.remove()


cilinderFig2 = [*cube.addGraph(cilinder.mesh, divisions, '#3ffdff')]
discFig2 = [*cube.addGraph(disc.mesh, divisions, '#3ffdff')]
cube.createLabel("Figura rotada", '#3ffdff')
cube.graphCube()

input("Presione para deshacer rotaciones...")

# Deshacer rotaciones
normalFirme = cube.normalVector

# Calcular los ángulos theta_z y phi
theta = degrees(acos( normalDiscoModificada*normalFirme/( normalDiscoModificada.norm()*normalFirme.norm() ) )) #obtener angulo entre el eje Z y el vector normal al disco nuevo
gamma = degrees(atan2(normalDiscoModificada.y, normalDiscoModificada.x))

# Matrices de rotación
rotation_z = Point.rotation_matrix_z(-gamma)  # Rotar alrededor del eje z por -phi
rotation_y = Point.rotation_matrix_y(-theta)  # Rotar alrededor del eje y por -theta_z
rotation_total = np.dot(rotation_y, rotation_z)  # Combinar las rotaciones

print(rotation_total)
# Eliminar figuras anteriores (si es necesario)
for fig, fig2 in zip(cilinderFig2, discFig2):
    fig.remove()
    fig2.remove()

# Rotar los puntos del cilindro y disco
for pt, pt2 in zip(cilinder.mesh, disc.mesh):
    if isinstance(pt, Point) and isinstance(pt2, Point):
        pt.rotateWithMatrix(rotation_total) # rotar cada punto
        pt2.rotateWithMatrix(rotation_total) # rotar cada punto

cilinderFig2 = [*cube.addGraph(cilinder.mesh, divisions, '#8bff7e')]
discFig2 = [*cube.addGraph(disc.mesh, divisions, '#8bff7e')]
cube.createLabel("Figura des-rotada", '#8bff7e')

        

input("Cerrar.")
