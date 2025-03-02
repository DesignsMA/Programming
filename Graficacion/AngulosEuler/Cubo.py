from bezierSurface import *
import numpy as np
class Cube:    
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
        self.normal = []
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
            self.ax.plot_surface(ptX, ptY, ptZ, color='red',rstride=1, cstride=1, alpha=0.5)       
            # Trazar la malla de alambre
            self.ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)

            self.ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos

        # Configurar los ejes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Mostrar la gráfica
        plt.show()# cara inferior
    
    def normal(self, face: str = 'frontal'):
        cara = self.faces[face]
        v1 = cara[0,1].arr() - cara[0, 0].arr()
        v2 = cara[1,0].arr() - cara[0, 0].arr()
        normal = np.cross(v1,v2) # producto cruz para  obtener la normal a una cara
        # Normalizar la normal para evitar problemas de escala
        normal = normal / np.linalg.norm(normal)
        
        self.normal = normal
        #Graficar la cara del cubo (triángulo formado por P0, P1, P2)
        # Graficar la normal en el origen
        self.ax.quiver(
            0, 0, 0,  # Punto de inicio (origen)
            normal[0], normal[1], normal[2],  # Componentes de la normal, componentes del vector flecha
            color='blue', label='Normal', length=5, arrow_length_ratio=0.07 # Longitud del vector
        )

cube = Cube(20,20,1,10)
cube.normal()
cube.graphCube()
