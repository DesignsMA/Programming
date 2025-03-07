from disc import *
from mathObjects import *
def interseccion(mesh1, mesh2, disProm):
    res = []
    for p1 in mesh1:
        for p2 in mesh2:
            d = np.sqrt((p2.x - p1.x)**2+(p2.y - p1.y)**2+(p2.z - p1.z)**2) # distancia entre puntos
            if d <= disProm and p2 not in res:
                res.append(p2)
    
    return res

def graph(mesh):
    ptx = np.array([point.x for point in mesh])
    pty = np.array([point.y for point in mesh])
    ptz = np.array([point.z for point in mesh])
    
    fig = plt.figure() #generar figura
    ax = fig.add_subplot(projection='3d') #añadir subplot
    ax.scatter(ptx, pty, ptz, c='black', s=5, depthshade=False) #graficar puntos
    # Configuraciones adicionales
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


disc1 = DiscMesh(center=Point(-1,0,0), subdivisions=40)
disc1.generateMesh()
disc2 = DiscMesh(subdivisions=40)
disc2.generateMesh()
graph(disc1.mesh+disc2.mesh)
res = interseccion(disc1.mesh,disc2.mesh,0.03)
graph(res)