import math        
import rotaciones

def print_points(points):
    for i in range(len(points)):
        if(points[i][1] > 180): #operacion booleana con figura
         print(points[i][0], points[i][1], points[i][2])
         
h = 100  # Centro en X
k = 200  # Centro en Y
w = 0 # Centro en Z
R = 30  # Radio del centro
r = 20  # Radio del conducto
num_points = 120  # Número de divisiones (resolucion)
points =[]
for i in range(num_points): #generar puntos
    #2PI * i / num_points
    t = 2 * math.pi * i / num_points
    
    for u in range(num_points): #generar puntos
        #2PI * i / num_points
        g = 2 * math.pi * u / num_points

        x = h + math.cos(t)*(R+ r*math.cos(g)) #ecuacion parametrica
        y= k + math.sin(t)*(R+ r*math.cos(g))
        z = w + r*math.sin(g)
        points.append([x, y, z]) #agregar puntos a la lista
 #para cerrar la figura
points.append(points[0])


print_points(points)

#rotaciones.rotate_z_3d(points, math.pi/4)
#rotaciones.rotate_x_3d(points, math.pi/6)
#print_points(points)

        
        
    