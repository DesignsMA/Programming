from mathObjects import *
from matplotlib import cm
import matplotlib.pyplot as plt
import pprint as pp
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
from imageToBinary import imageToBinary
from __init__ import *

def imageOnSurface(image: str, mesh: np.ndarray, m1:int=128, n1:int=128, umbral: int=128):
    graph(mesh, "Superficie original", 0.5)
    pixel_array = imageToBinary(image, umbral) # generar arreglo de pixeles en escala de grises
    pixel_array = np.where(pixel_array > umbral, 1, 0) #donde cualquier elemento del arreglo mayor a 128 =1, y menor a 128 = 0
    pp.pp(pixel_array) # imprimir arreglo en su totalidad
    imageMesh = [] # instanciar arreglo de la nueva malla
    
    m, n = pixel_array.shape
    mesh = np.array(surface.mesh).reshape(m,n) # dar la misma forma al arreglo unidimensional mesh
    # Iterar sobre cada elemento de la matriz
    for i in range(m):  # Iterar sobre las filas
        for j in range(n):  # Iterar sobre las columnas
            if pixel_array[i,j] == 1:
                imageMesh.append(mesh[i,j])

    return imageMesh # retornar nueva malla | superficie

    
def graph(mesh: list, title: str = "Superficie generada", ptS: int = 1):
    ptx = np.array([point.x for point in mesh])
    pty = np.array([point.y for point in mesh])
    ptz = np.array([point.z for point in mesh])
    
    fig = plt.figure() #generar figura
    ax = fig.add_subplot(projection='3d') #añadir subplot
    
    # Ajustar la relación de aspecto para que los ejes tengan la misma escala
    ax.set_box_aspect([1, 1, 1])  # Relación de aspecto igual en X, Y, Z
    
    ax.scatter(ptx, pty, ptz, c='black', s=ptS, depthshade=False) #graficar puntos
    # Configuraciones adicionales
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    plt.show()
        
# Puntos de control para la figura parecida a un paracaídas
paracaidas = np.array([
    [Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 0)],
    [Point(0, 1, 1), Point(1, 1, 2), Point(2, 1, 1)],
    [Point(0, 2, 0), Point(1, 2, 1), Point(2, 2, 0)]
])

while True:
    
    opt = input("""\n¿Que superficie quieres modificar?:\n
                    1. Malla Bilineal (Defecto)
                    2. Superficie de bézier
                    3. Disco
                    4. Cilindro
                    5. Esfera
                    6. Torus
                    -1. Salir
                    """)
    
    if opt == '1':
        surface = MallaBilineal(subdivisions=127)
    elif opt == '2':
        surface = BezierSurface(paracaidas,subdivisions=127)
    elif opt == '3':
        surface = DiscMesh(subdivisions=128)
    elif opt == '4':
        surface = CilinderMesh(subdivisions=128)
    elif opt == '5':
        surface = SphereMesh(subdivisions=128)
    elif opt == '6':
        surface = TorusMesh(subdivisions=128)
    elif opt == '-1':
        break

    opt = input("Introduce el nombre de la imagen | Escribe main para ver el mallado: ")
    if opt == "main":
        surface.__main__()
    else:
        surface.generateMesh()
        graph(imageOnSurface(opt, surface.mesh, umbral=128))