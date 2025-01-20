import spline #importar el generador de curva
import math
import dijkstra
from collections import namedtuple, deque
from pprint import pprint as pp

points = []
for i in range(4): # filas
    for j in range(4): # columnas
        points.append( spline.Point(i, j) ) # generar puntos
        
adj = []

i = 0
for i in range( len(points) ): # por cada punto
    u = 0
    for p in points: #comprobar con todos los puntos
        
        if ( math.sqrt( (p.x - points[i].x)**2 + (p.y - points[i].y)**2) == 1 \
             and not ( (str(u), str(i), 1 ) in adj ) \
             and not ( u == i)):
             weight = 1
             adj.append( (str(i), str(u), weight ))
        u += 1

graph = dijkstra.Graph(adj) # crear grafo
print (adj)
pp(graph.dijkstra("12", "3"))

with open('matrix.txt', 'w') as f:
        i = 0
        for p in points:
            i +=1
            print(f"{i} |- {p.x} {p.y} 0\n")
            f.write(f"{p.x} {p.y} 0\n")
            
with open('path.txt', 'w') as f:
        path = deque()
        for x in graph.dijkstra("12", "3"):
            print(x)
            p = points[int(x)]
            path.appendleft(p)
            f.write(f"{p.x} {p.y} 0\n")
        
        spline.splinePoints(path)
        
        
        


        
