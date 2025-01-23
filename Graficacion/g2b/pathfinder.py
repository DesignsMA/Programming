import spline #importar el generador de curva
import subprocess
import math
import dijkstra
from collections import namedtuple, deque

points = []
for i in reversed(range(4)): # filas
    for j in range(4): # columnas
        points.append( spline.Point(i, j) ) # generar puntos
        
adj = []

i = 0
with open('adj.txt', 'w') as f:
    for i in range( len(points) ): # por cada punto
        u = 0
        for p in points: #comprobar con todos los puntos

            if ( math.sqrt( (p.x - points[i].x)**2 + (p.y - points[i].y)**2) == 1 \
                 and not ( (str(u), str(i), 1 ) in adj ) \
                 and not ( u == i)):
                 weight = 1
                 adj.append( (str(i), str(u), weight ))
                 f.write(f"{points[i].x} {points[i].y}\
                           {points[u].x} {points[u].y}\
                           {(points[u].x+points[i].x)/2}\
                           {(points[u].y+points[i].y)/2}\
                           |{weight}| \n")
            u += 1

graph = dijkstra.Graph(adj) # crear grafo
path = []
pathdijkstra = graph.dijkstra("0", "15")
print (adj)
print(pathdijkstra)

        
with open('matrix.txt', 'w') as f:
        i = 0
        for p in points:
            print(f"{i} |- {p.x} {p.y} 0\n")
            f.write(f"{p.x} {p.y} 0 {i}\n")
            i +=1
            
with open('path.txt', 'w') as f:
        for x in pathdijkstra:
            print(x)
            p = points[int(x)]
            path.append(p)
            f.write(f"{p.x} {p.y} 0\n")

with open('pathLines.txt', 'w') as f:
        for i in range(len(path)-1): #para cubrir todos los puntos
                f.write(f"{path[i].x} {path[i].y} {path[i+1].x} {path[i+1].y}\n")

spline.splinePoints(path) #Generar puntos de la curva de bezier


with open('bezier_data.txt', 'r') as f:
        
        for i in range( int(spline.resolution/2) -1):
              f.readline() #leer hasta la mitad
        center = f.readline()

        pathtxt = "Path="
        for i in range(len(pathdijkstra)-1):
              pathtxt += pathdijkstra[i] + "-"
        
        pathtxt += pathdijkstra[i]

with open('pathLabel.txt', 'w') as f:
      f.write(f"{center.split(" ")[0]} {center.split(" ")[1].strip("\n")} {pathtxt}")

command = "gnuplot -e \"set terminal pngcairo;\
           set output \'graph.png\';\
           set zeroaxis;\
           unset xtics;\
           unset ytics;\
           set border 0;\
           plot \'adj.txt\' using 1:2:($3-$1):($4-$2) title \'\' with vectors nohead lc rgb \'#2f95fd\',\
           \'adj.txt\' using 5:6:7 with labels title \'\' font \'Arial,7\',\
           'matrix.txt' using 1:2:3 with points title \'Graph\' ps 3 pt 7 lc rgb '#6100ff',\
           'bezier_data.txt' using 1:2 with points title \'Bézier Curve\' ps 0.2 pt 7 lc rgb '#ff5353',\
            \'pathLines.txt\' using 1:2:($3-$1):($4-$2) title \'\' with vectors nohead lc rgb \'#ee5252\' lw 1.7,\
            \'path.txt\' using 1:2:3 with points title \'Control\' ps 3 pt 7 lc rgb \'#ff5353\',\
            \'pathLabel.txt\' using 1:2:3 with labels title \'\' tc rgb \'#171717\' font \'DejaVu Sans Bold,9\',\
            \'matrix.txt\' using 1:2:4 with labels title \'\' tc rgb \'#ffffff\' font \'DejaVu Sans Bold,7\'\"\
            "
            
subprocess.run(command, shell=True)

        
        
        


        
