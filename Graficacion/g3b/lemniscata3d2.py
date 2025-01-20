import math

# Parámetros de la lemniscata
h = 100  # Centro en X
k = 200  # Centro en Y
r = 20  # Radio de la lemniscata
circle_radius = 5  # Radio de los círculos
num_points = 400  # Puntos de la lemniscata
num_circle_points = 50  # Puntos por círculo

# Generar puntos de la lemniscata
points = []
for i in range(num_points):
    t = 2 * math.pi * i / num_points
    x = h + r * math.cos(t) / (1 + math.sin(t)**2)
    y = k + r * math.cos(t) * math.sin(t) / (1 + math.sin(t)**2)
    z = 0
    points.append([x, y, z])

# Para cerrar la figura
points.append(points[0])

# Función para generar un círculo en torno a un punto
def generate_circle(center, normal, radius, num_points):
    """
    Genera puntos de un círculo en 3D.
    :param center: Centro del círculo (x, y, z)
    :param normal: Vector normal al plano del círculo
    :param radius: Radio del círculo
    :param num_points: Número de puntos en el círculo
    :return: Lista de puntos del círculo en 3D
    """
    theta = [2 * math.pi * i / num_points for i in range(num_points)]
    circle_points = []
    
    # Vector arbitrario perpendicular al normal
    if abs(normal[0]) < abs(normal[1]):
        perp = [0, -normal[2], normal[1]]
    else:
        perp = [-normal[2], 0, normal[0]]
    
    # Ortogonalizar y normalizar
    perp = [v / math.sqrt(sum(p**2 for p in perp)) for v in perp]
    binormal = [
        normal[1] * perp[2] - normal[2] * perp[1],
        normal[2] * perp[0] - normal[0] * perp[2],
        normal[0] * perp[1] - normal[1] * perp[0]
    ]
    
    for t in theta:
        x = center[0] + radius * (math.cos(t) * perp[0] + math.sin(t) * binormal[0])
        y = center[1] + radius * (math.cos(t) * perp[1] + math.sin(t) * binormal[1])
        z = center[2] + radius * (math.cos(t) * perp[2] + math.sin(t) * binormal[2])
        circle_points.append([x, y, z])
    
    return circle_points

# Generar círculos alrededor de cada punto
all_circles = []
for i in range(len(points) - 1):
    # Tangente aproximada | Direccion de la curva entre dos puntos para determinar la rotacion del ci
    dx = points[i + 1][0] - points[i][0] #diferencia en x
    dy = points[i + 1][1] - points[i][1] #diferencia en y
    dz = points[i + 1][2] - points[i][2] #diferencia en z
    tangent = [dx, dy, dz] #vector tangente
    norm = math.sqrt( sum(t**2 for t in tangent) ) #
    tangent = [t / norm for t in tangent]  # Normalizar
    
    # Generar círculo
    circle = generate_circle(points[i], tangent, circle_radius, num_circle_points)
    all_circles.append(circle)
    all_circles.append([circle[0]])  # Para separar círculos

# Exportar los datos para visualización en Gnuplot o Matplotlib
with open("lemniscata.txt", "w") as f:
    for circle in all_circles:
        for point in circle:
            f.write(point[0], point[1], point[2])
        f.write("\n")  # Separar círculos con una línea en blanco

print("Datos guardados en 'lemniscata.txt'.")
