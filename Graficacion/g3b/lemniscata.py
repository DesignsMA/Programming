import math

h = 0  # Centro en X
k = 0  # Centro en Y
r = 5  # Radio
num_points = 400  # Número de divisiones (resolucion)

for i in range(num_points):
    #2PI * i / num_points
    t = 2 * math.pi * i / num_points
    x = h + r * math.cos(t) / (1+ math.sin(t)**2) #ecuacion parametrica de lemniscata
    y= h + r * math.cos(t)*math.sin(t) /  (1+ math.sin(t)**2)
    print(x,y)
