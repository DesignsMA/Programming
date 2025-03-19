from Mallas import *
#(x−h)²+ (y−k)²+ (z−l)²=r²
def perteneceAEsfera(punto: Point, esfera: SphereMesh):
    """Evalúa si un punto pertenece a una esfera por medio del despeje de su ecuación
       (x−h)²+ (y−k)²+ (z−l)²=r²
    """
    xc,yc,zc = punto.tuple()
    return (punto.x - xc)**2 + (punto.y - yc)**2 + (punto.z - zc)**2 - esfera.r**2 <= 0 # Debe estar dentro o en el borde

def interseccionEsfera(e1: SphereMesh, e2: SphereMesh):
    " Retorna los puntos de intersección entre la esfera uno y dos "
    res = [ p for p in e1.mesh if perteneceAEsfera(p, e2)]
    return res

def diferenciaEsfera(e1: SphereMesh, e2: SphereMesh):
    """ Retorna los puntos de e1 que NO están en e2 """
    diferencia = [p for p in e1.mesh if not perteneceAEsfera(p, e2)]
    return diferencia


def graph(ax, color, mesh, size: int=1, alpha: float=1):
    ptx = np.array([point.x for point in mesh])
    pty = np.array([point.y for point in mesh])
    ptz = np.array([point.z for point in mesh])
    
    ax.scatter(ptx, pty, ptz, c=color, s=size, depthshade=False, alpha=alpha ) #graficar puntos

fig = plt.figure() #generar figura
ax = fig.add_subplot(projection='3d') #añadir subplot
ax.set_box_aspect([1,1,1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

sphere1 = SphereMesh(subdivisions=100, radio=10)
sphere1.generateMesh()
sphere2 = SphereMesh(center=Point(5,0,0), subdivisions=100, radio=10)
sphere2.generateMesh()


res = set(interseccionEsfera(sphere1,sphere2))
res_diff1 = set( diferenciaEsfera(sphere1,sphere2)) # estan en d1 pero no en d2
res_diff2 = set( diferenciaEsfera(sphere2,sphere1)) # estan en d2 pero no en d1
graph(ax, 'black', res_diff1+res_diff2, 1, alpha=1)
graph(ax,'#ff5353', res, 1)
plt.show()

