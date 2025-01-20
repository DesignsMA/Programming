import math

def print_points(points):
    for i in range(len(points)):
         print(points[i][0], points[i][1], points[i][2])
         
        
h = 100  # Centro en X
k = 200  # Centro en Y
R = 20  # Radio
r = 2  # Radio del conducto
w = 0 # Centro en Z
num_points = 120  # Número de divisiones (resolucion)
points =[]
for i in range(num_points): #generar puntos
    #2PI * i / num_points
    t = 2 * math.pi * i / num_points
    for u in range(num_points): #generar puntos
            #2PI * i / num_points
            g = 2 * math.pi * u / num_points

            x = h + (math.cos(t) / (1+ math.sin(t)**2))*(R+ r*math.cos(g)) #ecuacion parametrica
            y = k + (math.cos(t) * math.sin(t) / (1 + math.sin(t)**2))*(R+ r*math.cos(g)*2)
            z = w + r*math.sin(g)
            points.append([x, y, z]) #agregar puntos a la lista
     #para cerrar la figura

#fuera del for
points.append(points[0])
print_points(points)




        
        
    