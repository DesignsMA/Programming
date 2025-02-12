from mathObjects import *
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
class DiscMesh():
    def  __init__(self,radio:int=1,subdivisions: int=10, center: Point=Point(0,0,0)):
        self.subdivisions = subdivisions+1
        self.radio = radio
        self.center = center
        self.mesh = []
        
    def generateMesh(self):
        self.mesh = []
        for ri in np.linspace(0,self.radio,self.subdivisions): #dividir r en self.subdivisions partes
            for theta in np.linspace(0, pi*2, self.subdivisions): #de 0-2Pi calcular theta
                pt = Point( self.center.x + ri*cos(theta), self.center.y + ri*sin(theta) ) # generar puntos de la circunferencia con radio ri
                self.mesh.append(pt) # añadir punto
    
    def graph(self):
        ptx = np.array([point.x for point in self.mesh])
        pty = np.array([point.y for point in self.mesh])
        ptz = np.array([point.z for point in self.mesh])
        
        fig = plt.figure() #generar figura
        ax = fig.add_subplot(projection='3d') #añadir subplot
        
        ptX = ptx.reshape(self.subdivisions,self.subdivisions)
        ptY = pty.reshape(self.subdivisions,self.subdivisions)
        ptZ = ptz.reshape(self.subdivisions,self.subdivisions)

        color_data = np.hypot(ptX, ptY)  # Distancia radial
        norm_color = (color_data - color_data.min()) / (color_data.max() - color_data.min())  # Normalizar
        # Aplicar gradiente de colores a la superficie
        ax.plot_surface(ptX, ptY, ptZ, facecolors=cm.inferno(norm_color), rstride=1, cstride=1, alpha=0.5)       
        # Trazar la malla de alambre
        ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)
        
        ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=True) #graficar puntos

        # Configuraciones adicionales
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
        

disc =  DiscMesh(2, 15)
disc.generateMesh()
disc.graph()