import math

# Paso 1: Parámetros del círculo
h = 0  # Centro en X
k = 0  # Centro en Y
r = 5  # Radio
num_points = 100  # Número de divisiones (resolucion)
for i in range (num_points):
    t = 2 * math.pi * i / num_points
    x = h + r * math.cos(t) #se le suma lo recorrido por el centro
    y = k + r * math.sin(t) 
    print(x, y)

#para cerrar la figura
print(h + r, k)

#usamos gnuplot para graficar (plot para  2d, splot para 3d)