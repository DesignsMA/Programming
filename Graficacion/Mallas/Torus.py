from mathObjects import *
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
class TorusMesh():
    def  __init__(self,radio:float=6, conductRadio:float=3,subdivisions: int=15, center: Point=Point(0,0,0)):
        self.subdivisions = subdivisions
        self.R = radio
        self.r = conductRadio
        self.center = center
        self.mesh = []
        
    def generateMesh(self):
        self.mesh = []
        for theta in np.linspace(0, pi*2, self.subdivisions): #de 0-2Pi calcular phi
            for phy in np.linspace(0, pi*2, self.subdivisions): #de 0-2Pi calcular theta
                x = (self.R + self.r*cos(theta))*cos(phy)
                y = (self.R + self.r*cos(theta))*sin(phy)
                z = self.r*sin(theta)

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

        # Establecer límites de los ejes proporcionales al radio menor (r) y al centro
        ax.set_zlim([self.center.z - self.r * 2, self.center.z + self.r * 2])
        ax.set_xlim([self.center.x - self.r * 2, self.center.x + self.r * 2])
        ax.set_ylim([self.center.y - self.r * 2, self.center.y + self.r * 2])
        
        ptX = ptx.reshape(self.subdivisions,self.subdivisions)
        ptY = pty.reshape(self.subdivisions,self.subdivisions)
        ptZ = ptz.reshape(self.subdivisions,self.subdivisions)

        color_data = np.hypot(ptX, ptY)  # Distancia radial
        norm_color = (color_data - color_data.min()) / (color_data.max() - color_data.min())  # Normalizar
        # Aplicar gradiente de colores a la superficie
        ax.plot_surface(ptX, ptY, ptZ,facecolors=cm.plasma(norm_color),rstride=1, cstride=1, alpha=1)       
        # Trazar la malla de alambre
        ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)
        
        ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=True) #graficar puntos

        # Configuraciones adicionales
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        plt.show()
        
    def __main__(self):
        torus = TorusMesh(subdivisions=25)
        torus.generateMesh()
        torus.graph("Ring Torus| Dona (R>r)")
        torus = TorusMesh(radio=3,conductRadio=3,subdivisions=25)
        torus.generateMesh()
        torus.graph("Horn Torus| (R==r)")
        torus = TorusMesh(radio=1.5,conductRadio=3,subdivisions=25)
        torus.generateMesh()
        torus.graph("Spindle Torus| (R<r)")
        