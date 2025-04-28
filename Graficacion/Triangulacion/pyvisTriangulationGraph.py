from pyvis.network import Network
import random
from pyvisDelaunayTriangulation2D import DelaunayTriangulation, Point2D

# Configuración
bounds = [60, 60]
nodes = 16
canvas_size = 600

# factor para escalar de coordenadas [0..bounds] → píxeles
scale = (canvas_size / max(bounds)) * 2  
# desplazamiento para llevar el centro de bounds a (0,0)
off_x = bounds[0] / 2
off_y = bounds[1] / 2

# Creamos la red PyVis sin physics
net = Network(f"{canvas_size}px", f"{canvas_size}px", bgcolor="#161616", notebook=False)
net.set_options('''
{
  "physics": { "enabled": false },
  "interaction": { "dragNodes": true, "zoomView": true, "dragView": true },
  "nodes": { "font": { "size": 14, "color": "#ffffff" } }
}
''')

# Generar puntos aleatorios y triangular
pts = [Point2D(random.randint(10, bounds[0]-10),
               random.randint(10, bounds[1]-10))
       for _ in range(nodes)]
tri = DelaunayTriangulation(pts)
tri.triangulate()

# Añadir sólo los nodos originales, centrados y con Y invertida
for i, p in enumerate(tri.sorted[:nodes]):
    x_px = (p.x - off_x) * scale
    y_px = -(p.y - off_y) * scale   # <- OJO: invertimos Y para PyVis
    net.add_node(i, label=str(i), shape="dot", color="#ff5353",
                 x=x_px, y=y_px, size=10, physics=False)

# Detectar aristas del hull
hull = {(min(e.a, e.b), max(e.a, e.b)) for e in tri.hull}

# Añadir todas las aristas Delaunay
for e in tri.edges:
    a, b = e.a, e.b
    key = (min(a, b), max(a, b))
    if key in hull:
        net.add_edge(a, b, color="#4287f5", width=3, title=f"Hull {a}-{b}")
    else:
        net.add_edge(a, b, color="#ffffff", width=1, title=f"Edge {a}-{b}")

net.title = f"Delaunay Triangulation ({nodes} nodes)"
net.write_html('triangulation_output.html')
