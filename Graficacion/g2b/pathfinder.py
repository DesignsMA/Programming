import spline #importar el generador de curva
import subprocess
import dijkstra
from collections import namedtuple, deque

points = [] #creando matriz de puntos
for i in reversed(range(4)): # filas
    for j in range(4): # columnas
        points.append( spline.Point(i, j) ) # generar puntos
        
adjDistance = [
    # Vertical
    ("16", "12", 9), ("12", "8", 11), ("8", "4", 3),       
    ("15", "11", 8), ("11", "7", 3), ("7", "3", 5),       
    ("14", "10", 5), ("10", "6", 5), ("6", "2", 5),       
    ("13", "9", 2), ("9", "5", 12), ("5", "1", 3),                    
    #" H"orizontal 
    ("16", "15", 10), ("12", "11", 2), ("8", "7", 1), ("4", "3", 13), 
    ("15", "14", 9), ("11", "10", 4), ("7", "6", 1), ("3", "2", 4), 
    ("14", "13", 1), ("10", "9", 3), ("6", "5", 2), ("2", "1", 2),               
]

adjTime = [
    # Vertical
    ("16", "12", 4), ("12", "8", 3), ("8", "4", 7),       
    ("15", "11", 2), ("11", "7", 9), ("7", "3", 13),       
    ("14", "10", 9), ("10", "6", 10), ("6", "2", 6),       
    ("13", "9", 8), ("9", "5", 7), ("5", "1", 4),                    
    #" H"orizontal 
    ("16", "15", 7), ("12", "11", 10), ("8", "7", 9), ("4", "3", 9), 
    ("15", "14", 4), ("11", "10", 9), ("7", "6", 8), ("3", "2", 5), 
    ("14", "13", 9), ("10", "9", 6), ("6", "5", 8), ("2", "1", 3),               
]
alpha = 1  # Preferencia por distancia
beta = 1   # Preferencia por tiempo

adjCombined = [
    (u, v, alpha * distance + beta * time) 
    for (u, v, distance), (_, _, time) in zip(adjDistance, adjTime)
]

def calculatePath(points: list[spline.Point], adj: list[tuple[str, str, int]], fileName: str = "graph.png"):
    with open('adj.txt', 'w') as f:
        for t in adj:
            i = int(t[0])-1
            u = int(t[1])-1
            weight = t[2]
            f.write(f"{points[i].x} {points[i].y}\
                      {points[u].x} {points[u].y}\
                      {(points[u].x+points[i].x)/2}\
                      {(points[u].y+points[i].y)/2}\
                      |{weight}| \n")

    graph = dijkstra.Graph(adj) # crear grafo
    paths = graph.dijkstra("1", "16")
    for z in range(len(paths)): #por cada camino posible
        pathdijkstra =  paths[z]
        path = []
        print (adj)
        print(pathdijkstra)


        with open('matrix.txt', 'w') as f:
                i = 1
                for p in points:
                    print(f"{i} |- {p.x} {p.y} 0\n")
                    f.write(f"{p.x} {p.y} 0 {i}\n")
                    i +=1

        with open('path.txt', 'w') as f:
                for x in pathdijkstra:
                    print(x)
                    p = points[int(x)-1]
                    path.append(p)
                    f.write(f"{p.x} {p.y} 0\n")

        with open('pathLines.txt', 'w') as f:
                for i in range(len(path)-1): #para cubrir todos los puntos
                        f.write(f"{path[i].x} {path[i].y} {path[i+1].x} {path[i+1].y}\n")

        paramx, paramy, arclenght = spline.splinePoints(path) #Generar puntos de la curva de bezier

        pathtxt = "Path="
        for i in range(len(pathdijkstra)-1):
              pathtxt += pathdijkstra[i] + "-"

        pathtxt += pathdijkstra[i]

        command = f"gnuplot -e \"set terminal pngcairo size 900,800;\
                   set output \'{fileName}-path[{z+1}].png\';\
                   set zeroaxis;\
                   set yrange [-0.4:3];\
                   unset xtics;\
                   unset ytics;\
                   set border 0;\
                   set label 1 '{pathtxt} | Lenght: {arclenght} units' at 0,-0.2 left font 'DejaVu Sans Bold,12';\
                   set label 2 '{paramx.strip('\n')}' at 0,-0.3 left font 'DejaVu Sans Bold,9.5';\
                   set label 3 '{paramy.strip('\n')}' at 0,-0.4 left font 'DejaVu Sans Bold,9.5';\
                   plot \'adj.txt\' using 1:2:($3-$1):($4-$2) title \'\' with vectors nohead lc rgb \'#2f95fd\',\
                   \'adj.txt\' using 5:6:7 with labels title \'\' font 'DejaVu Sans Bold,7',\
                   'matrix.txt' using 1:2:3 with points title \'Graph\' ps 3 pt 7 lc rgb '#6100ff',\
                   'bezier_data.txt' using 1:2 with points title \'Bézier Curve\' ps 0.2 pt 7 lc rgb '#ff5353',\
                    \'pathLines.txt\' using 1:2:($3-$1):($4-$2) title \'\' with vectors nohead lc rgb \'#ee5252\' lw 1.7,\
                    \'path.txt\' using 1:2:3 with points title \'Control\' ps 3 pt 7 lc rgb \'#ff5353\',\
                    \'matrix.txt\' using 1:2:4 with labels title \'\' tc rgb \'#ffffff\' font 'DejaVu Sans Bold,8'\"\
                    "

        subprocess.run(command, shell=True)


calculatePath(points, adjDistance, "fig3")
calculatePath(points, adjTime, "fig4")
calculatePath(points, adjCombined, "fig5-6")

        


        
