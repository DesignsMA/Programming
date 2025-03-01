from bezierSurface import *

def graph(mesh, m, n):
        ptx = np.array([point.x for point in mesh])
        pty = np.array([point.y for point in mesh])
        ptz = np.array([point.z for point in mesh])
        
        fig = plt.figure() #generar figura
        ax = fig.add_subplot(projection='3d') #añadir subplot
        shapeM = m
        shapeN = n
        ptX = ptx.reshape(shapeM,shapeN)
        ptY = pty.reshape(shapeM,shapeN)
        ptZ = ptz.reshape(shapeM,shapeN)
        
        # Aplicar gradiente de colores a la superficie
        ax.plot_surface(ptX, ptY, ptZ, cmap='viridis', rstride=1, cstride=1, alpha=0.7)
        
        # Trazar la malla de alambre
        ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.5)
        
        ax.scatter(ptx, pty, ptz, c='black', s=5, depthshade=False) #graficar puntos

        # Configuraciones adicionales
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

# cara inferior
mallado = BezierSurface(np.array( [[Point(0, 0, 0), Point(0, 20, 0)],
                                  [Point(-20, 0, 0), Point(-20, 20, 0)]] ))
mallado.generateMesh()
cuboMesh = mallado.mesh

mallado.surfacePoints= np.array( [[Point(0, 0, 0), Point(0, 0, 1)],
                                  [Point(-20, 0, 0), Point(-20, 0, 1)]] )

mallado.generateMesh()
cuboMesh = set(mallado.mesh + cuboMesh)
graph(cuboMesh, 11, 22)