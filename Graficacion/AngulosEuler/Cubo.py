from bezierSurface import *

def graphCube(l,w,h, subdivisions):
    # Definir los puntos de las 6 caras del cubo
    caras =[ np.array([[Point(0, 0, 0), Point(0, w, 0)],
                             [Point(l, 0, 0), Point(l, w, 0)]]), 
            
            np.array([[Point(0, 0, h), Point(0, w, h)],
                             [Point(l, 0, h), Point(l, w, h)]]),
            
            np.array([[Point(0, w, 0), Point(0, w, h)],
                              [Point(l, w, 0), Point(l, w, h)]]),
            
            np.array([[Point(0, 0, 0), Point(0, 0, h)],
                              [Point(l, 0, 0), Point(l, 0, h)]]),
            
            np.array([[Point(0, 0, 0), Point(0, 0, h)],
                             [Point(0, w, 0), Point(0, w, h)]]),
            
            np.array([[Point(l, 0, 0), Point(l, 0, h)],
                           [Point(l, w, 0), Point(l, w, h)]])
    ]
    # Crear la figura y el eje 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for cara in caras:
        mesh = BezierSurface(cara, subdivisions)
        mesh.generateMesh()
        
        ptx = np.array([point.x for point in mesh.mesh])
        pty = np.array([point.y for point in mesh.mesh])
        ptz = np.array([point.z for point in mesh.mesh])        
                
        ptX = ptx.reshape(subdivisions+1, subdivisions+1)
        ptY = pty.reshape(subdivisions+1, subdivisions+1)
        ptZ = ptz.reshape(subdivisions+1, subdivisions+1)

        # Aplicar gradiente de colores a la superficie
        ax.plot_surface(ptX, ptY, ptZ, cmap='viridis',rstride=1, cstride=1, alpha=1)       
        # Trazar la malla de alambre
        ax.plot_wireframe(ptX, ptY, ptZ, color='black', linewidth=0.2)
        
        ax.scatter(ptx, pty, ptz, c='black', s=3, depthshade=False) #graficar puntos
        
    # Configurar los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar la gráfica
    plt.show()# cara inferior
    
graphCube(20, 20, 1, 10)