from disc import *
from mathObjects import *

def perteneceADisco(punto, xc, yc, zc, r):
    """Evalúa si un punto pertenece al disco en el plano z = zc"""
    if not np.isclose(punto.z, zc, atol=1e-6):
        print("El disco dos no está en el mismo plano que el disco uno")
        return False  # El punto no está en el plano del disco
        # ecuación del disco, si la distancia cuadra es menor o igual a cero, pertenece al disco
    return (punto.x - xc)**2 + (punto.y - yc)**2 - r**2 <= 0 # Debe estar dentro o en el borde

def interseccionDisco(d1: DiscMesh, d2: DiscMesh):
    " Retorna los puntos de intersección entre el disco uno y dos "
    res = [ p for p in d1.mesh if perteneceADisco(p, d2.center.x, d2.center.y, d2.center.z, d2.radio)]
    return res

def diferenciaDisco(d1: DiscMesh, d2: DiscMesh):
    """ Retorna los puntos de d1 que NO están en d2 """
    diferencia = [p for p in d1.mesh if not perteneceADisco(p, d2.center.x, d2.center.y, d2.center.z, d2.radio)]
    return diferencia


def graph(ax, color, mesh, size: int=1, alpha: float=1):
    ptx = np.array([point.x for point in mesh])
    pty = np.array([point.y for point in mesh])
    ptz = np.array([point.z for point in mesh])
    
    ax.scatter(ptx, pty, ptz, c=color, s=size, depthshade=False, alpha=alpha ) #graficar puntos
    # Configuraciones adicionales

fig = plt.figure() #generar figura
ax = fig.add_subplot(projection='3d') #añadir subplot
ax.set_box_aspect([1,0.8,1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

disc1 = DiscMesh(subdivisions=100, radio=10)
disc1.generateMesh()
disc2 = DiscMesh(center=Point(5,0,0), subdivisions=100, radio=10)
disc2.generateMesh()


res = set(interseccionDisco(disc1,disc2))
res_diff1 = set( diferenciaDisco(disc1,disc2)) # estan en d1 pero no en d2
res_diff2 = set( diferenciaDisco(disc2,disc1)) # estan en d2 pero no en d1
graph(ax, 'black', res_diff1, 1, alpha=1)
graph(ax, 'black', res_diff2, 1, alpha=1)
graph(ax,'#ff5353', res, 1)
plt.show()

