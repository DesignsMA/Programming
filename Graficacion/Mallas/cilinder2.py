from mathObjects import *
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
class CilinderMesh():
    def  __init__(self,radio:int=1,subdivisions: int=10, center: Point=Point(0,0,0), height: int=10):
        self.subdivisions = subdivisions
        self.radio = radio
        self.center = center
        self.height = height
        self.mesh = []
        
    def generateMesh(self):
        self.mesh = []
        for zi  in np.linspace(0,self.height,self.subdivisions):
            for theta in np.linspace(0, pi*2, self.subdivisions): #de 0-2Pi calcular theta
                pt = Point( self.center.x + self.radio*cos(theta), self.center.y + self.radio*sin(theta), zi ) # generar puntos de la circunferencia con radio ri
                self.mesh.append(pt) # añadir punto
    
    def graph(self):
        ptx = np.array([point.x for point in self.mesh])
        pty = np.array([point.y for point in self.mesh])
        ptz = np.array([point.z for point in self.mesh])
        
        fig = plt.figure() #generar figura
        ax = fig.add_subplot(projection='3d') #añadir subplot
        shapeM = self.subdivisions
        shapeN = self.subdivisions
        ptX = ptx.reshape(shapeM,shapeN)
        ptY = pty.reshape(shapeM,shapeN)
        ptZ = ptz.reshape(shapeM,shapeN)
        
        # Aplicar gradiente de colores a la superficie
        ax.plot_surface(ptX, ptY, ptZ, cmap='viridis', rstride=1, cstride=1, alpha=0.7)
        
        # Trazar la malla de alambre
        ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.5)
        
        ax.scatter(ptx, pty, ptz, c='black', s=5, depthshade=True) #graficar puntos

        # Configuraciones adicionales
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
        
    def __main__(self):

        disc =  CilinderMesh(2, 15, height=20)
        disc.generateMesh()
        disc.graph()