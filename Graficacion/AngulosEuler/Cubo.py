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
        self.normalVector = []
    
    def showGraph(self):
        plt.show()
        
    def graphCube(self):
        self.meshes = {}
        self.ax.set_box_aspect([1, 1, 0.3])  # Relación de aspecto igual en X, Y, Z

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
            self.ax.plot_surface(ptX, ptY, ptZ, color='red',rstride=1, cstride=1, alpha=0.5)       
            # Trazar la malla de alambre
            self.ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)

            self.ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos
    
        # Configurar los ejes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
    
    def addGraph(self, mesh, subdivisions):
        ptx = np.array([point.x for point in mesh])
        pty = np.array([point.y for point in mesh])
        ptz = np.array([point.z for point in mesh])

        ptX = ptx.reshape(subdivisions,subdivisions)
        ptY = pty.reshape(subdivisions,subdivisions)
        ptZ = ptz.reshape(subdivisions,subdivisions)
        
        self.ax.plot_surface(ptX, ptY, ptZ, color='red',rstride=1, cstride=1, alpha=0.5)       
        # Trazar la malla de alambre
        self.ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)
        self.ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos

    
    def normalVectorToFace(self, face: str = 'frontal'):
        cara = self.faces[face]
        self.normalVector = self.normalToSurface(cara[0,0], cara[0,1], cara[1,0], txt="cubo")
        print("Vector normal a la cara ",face, " : ", self.normalVector)
    
    def normalToSurface(self, p1:Point, p2:Point, p3:Point, color: str = 'blue', l: float = 1.5, lnw: float = 6, txt: str =None ):
        v1 = p2.arr() - p1.arr()
        v2 = p3.arr() - p1.arr()
        normal = np.cross(v1,v2) # producto cruz para  obtener la normal a una cara
        # Normalizar la normal para evitar problemas de escala
        normal = normal / np.linalg.norm(normal)
        # Graficar la normal trasladada al origen
        self.ax.quiver(
            0, 0, 0,  # Punto de inicio (origen)
            normal[0], normal[1], normal[2],  # Componentes de la normal, componentes del vector flecha
            color=color, label='Normal', length=l, arrow_length_ratio=0.12, # Longitud del vector
            pivot='tail', linewidth=lnw
        )
        if txt is not None:
            color_patch = mpatches.Patch(color=color, label=f"Normal al {txt}")
            self.labels.append(color_patch)
            self.ax.legend(handles=self.labels, loc=(1,1))

        return normal


cube = FigureSpace(20,20,1,10)
cube.normalVectorToFace('superior')

r = 10
cilinder = CilinderMesh(r, height=1) # cilindro de 10x1
cilinder.generateMesh()

cube.addGraph(cilinder.mesh, 10)
cube.graphCube()


p1 = Point(10,0,0)
p2 = Point(r*cos(120), r*sin(120), 0)
p3 = Point(r*cos(240),  r*sin(240), 0)
print(f"Vector normal al disco: { cube.normalToSurface( p1, p2, p3, 'green', 1.8, 2, "disco")}")

# cambiando alturas del disco

p1.z = 0
p2.z = 1
p3.z = 1
cube.showGraph()

