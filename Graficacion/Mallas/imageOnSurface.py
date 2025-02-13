from mathObjects import *
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
from imageToBinary import imageToBinary
from cilinder2 import *
from bezierSurface import *
    
def graph(mesh: list, m:int=128, n:int=128):
    ptx = np.array([point.x for point in mesh])
    pty = np.array([point.y for point in mesh])
    ptz = np.array([point.z for point in mesh])
    
    fig = plt.figure() #generar figura
    ax = fig.add_subplot(projection='3d') #añadir subplot
    
    # Ajustar la relación de aspecto para que los ejes tengan la misma escala
    ax.set_box_aspect([1, 1, 1])  # Relación de aspecto igual en X, Y, Z
    
    ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos
    # Configuraciones adicionales
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
        

surface = BezierSurface(subdivisions=127)
surface.generateMesh()
pixel_array = imageToBinary("no.webp")
pixel_array = np.where(pixel_array > 128, 1, 0)
print(pixel_array)

imageMesh = []
with open("bin.txt", 'r+') as f:
        m, n = pixel_array.shape
        mesh = np.array(surface.mesh).reshape(128,128)
        # Iterar sobre cada elemento de la matriz
        for i in range(m):  # Iterar sobre las filas
            for j in range(n):  # Iterar sobre las columnas
                if pixel_array[i,j] == 1:
                    imageMesh.append(mesh[i,j])
           

graph(imageMesh)
    