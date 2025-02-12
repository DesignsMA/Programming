from mathObjects import *
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
class SphereMesh():
    def  __init__(self,radio:float=1,subdivisions: int=15, center: Point=Point(0,0,0)):
        self.subdivisions = subdivisions+1
        self.r = radio
        self.center = center
        self.mesh = []
        
    def generateMesh(self):
        self.mesh = []
        for theta in np.linspace(0, pi*2, self.subdivisions): #de 0-2Pi calcular phi
            for phy in np.linspace(0, pi*2, self.subdivisions): #de 0-2Pi calcular theta
                x = self.r*sin(theta)*cos(phy)
                y = self.r*sin(theta)*sin(phy)
                z = self.r*cos(theta)

                pt = self.center + Point(x,y,z) # generar puntos de la circunferencia con radio ri
                self.mesh.append(pt) # añadir punto
    
    def graph(self, title: str="Torus"):
        ptx = np.array([point.x for point in self.mesh])
        pty = np.array([point.y for point in self.mesh])
        ptz = np.array([point.z for point in self.mesh])
        
        fig = plt.figure() #generar figura
        ax = fig.add_subplot(projection='3d') #añadir subplot
        
        # Ajustar la relación de aspecto para que los ejes tengan la misma escala
        ax.set_box_aspect([1, 1, 1])  # Relación de aspecto igual en X, Y, Z
        
        ptX = ptx.reshape(self.subdivisions,self.subdivisions)
        ptY = pty.reshape(self.subdivisions,self.subdivisions)
        ptZ = ptz.reshape(self.subdivisions,self.subdivisions)

        # Aplicar gradiente de colores a la superficie
        ax.plot_surface(ptX, ptY, ptZ, cmap='viridis',rstride=1, cstride=1, alpha=0.6)       
        # Trazar la malla de alambre
        ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)
        
        ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=True) #graficar puntos

        # Configuraciones adicionales
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        plt.show()
        

Sphere = SphereMesh(radio=1,subdivisions=8)
Sphere.generateMesh()
Sphere.graph("Sphere")
