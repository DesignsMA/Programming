from pyvis.network import Network
import random
import math
import numpy as np
from pyvisDelaunayTriangulation2D import DelaunayTriangulation, Triangle, Point2D
import pyvista as pv


while input('X para salir: ').lower() != 'x':
    plotter = pv.Plotter()
    plotter.add_key_event("x", plotter.close)
    is3D = False
    # Crear puntos aleatorios
    tipo = input("¿Que quieres generar?\nPuntos de una esfera (esfera) | Random (rand)\n: ")
    if tipo.lower() == 'esfera':
        is3D = input('¿Visualizar en 3D?\nSí | No\n:  ').lower() != 'no'
        thetaV = float( input("Grados en theta: ") )
        phyV = float( input("Grados en phy: ") )
        res = int( input("Subdivisiones: ") )
        genPoints = []
        for theta in np.linspace(0, thetaV*math.pi/180, res): #de 0-2Pi calcular phi
            for phy in np.linspace(0, phyV*math.pi/180, res): #de 0-2Pi calcular theta
                x = 10*math.sin(theta)*math.cos(phy)
                y = 10*math.sin(theta)*math.sin(phy)
                z = 10*math.cos(theta)
                genPoints.append(Point2D(x*100,y*100,z*100)) # por cien para escalar

    else:
        points = int( input("Cuantos puntos quieres generar: ") )
        genPoints = [Point2D(random.random()*100, random.random()*100) for _ in range(points)]

    drawCenter = input("¿Mostrar los circuncentros? | Si - No\n: ")
    
    # Triangulación
    dt = DelaunayTriangulation(genPoints)
    dt.bowyer_watson()

    # Visualización (usando pyvis)
    net = Network(height="900px", width="100%", notebook=False, bgcolor="#161616")

    if drawCenter.lower() != 'no':
        # circuncentros
        for i, triangle in enumerate(dt.triangles):
            if isinstance(triangle, Triangle) and not triangle.is_degenerate:
                circuncenter, radius = triangle.get_circumcircle()

                # Punto pequeño para el circuncentro
                net.add_node(n_id=f"c{i}", 
                           x=circuncenter.x*10, 
                           y=circuncenter.y*10, 
                           size=3, 
                           color="#00ff99",
                           font={'size': 0},
                           physics=False)

                # Círculo circunscrito (usando múltiples nodos para simular círculo)
                circle_nodes = 32  # Número de puntos para aproximar el círculo
                for j in range(circle_nodes):
                    angle = 2 * math.pi * j / circle_nodes
                    x = circuncenter.x*10 + radius*10 * math.cos(angle)
                    y = circuncenter.y*10 + radius*10 * math.sin(angle)

                    net.add_node(n_id=f"circ_{i}_{j}",
                               x=x, 
                               y=y, 
                               size=1, 
                               color="#00ff99",
                               font={'size': 0},
                               opacity=0,
                               physics=False)

                    # Conectar puntos del círculo
                    if j > 0:
                        net.add_edge(f"circ_{i}_{j-1}", f"circ_{i}_{j}", 
                                   width=0.5, 
                                   font={'size': 0},
                                   opacity=0.2,
                                   color="#00ff99",
                                   physics=False)
                # Cerrar el círculo
                net.add_edge(f"circ_{i}_{circle_nodes-1}", f"circ_{i}_0", 
                           width=0.5, 
                           font={'size': 0},
                           opacity=0.2,
                           color="#00ff99",
                           physics=False)
                
    # Añadir puntos
    for i, point in enumerate(dt.points):
        net.add_node(i, x=point.x*10, y=point.y*10, size=6, color="#ff5353", borderWidth=1, physics=False)
        
        if is3D:
            sphere = pv.Sphere(center=point.arr3D(), theta_resolution=10, phi_resolution=10, radius=4)
            plotter.add_mesh(sphere, color='#ff5353')
    # Añadir aristas
    edge_set = set()
    for triangle in dt.triangles:
        for edge in triangle.edges:
            edge_set.add(edge)
            
    for edge in edge_set:
        if len(edge) == 2:
            p1, p2 = edge
            id1 = dt.points.index(p1)
            id2 = dt.points.index(p2)
            net.add_edge(id1, id2, physics=False, width=2, color="#ff5050")
            if is3D:
                line = pv.Line(p1.arr3D(),p2.arr3D())
                plotter.add_mesh(line, color='#ff5353')
        

    net.set_options('''
    {
      "physics": { "enabled": false },
      "interaction": { "dragNodes": true, "zoomView": true, "dragView": true }
    }
    ''')
    net.write_html("delaunay.html", notebook=False)
    
    if is3D:
        plotter.show('Triangulación de una esfera.')
        

plotter.close()