import math
import random
class Point():
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
        
points = []
resolution = 3000

for i in range(6):
    points.append(Point(random.random(), random.random()))
    
def factorial(x:int):
    if x == 1 or x==0:
        return 1
    else:
        return x*factorial(x-1)
    
def binomial(n:int, k:int):
    return factorial(n)/(factorial(k)*factorial(n-k))

def splinePoints(points:list[Point]):
    n = len(points)-1
    cfs = []
    pt = Point(0,0)
    arc_length = 0
    prev_pt = Point(0,0)
    with open('bezier_data.txt', 'w') as f:
        
        for u in range(n+1):
            cfs.append(binomial(n,u)) #calcular coeficientes binomiales

        for i in range(resolution):
            t = 0+1*i/resolution #por cada  t en el rango de 0-1
            pt.x = pt.y = 0
            for u in range(n+1):
                pt.x += cfs[u]*points[u].x*math.pow((1-t),n-u)*math.pow(t,u)
                pt.y += cfs[u]*points[u].y*math.pow((1-t),n-u)*math.pow(t,u)

            f.write(f"{pt.x} {pt.y}\n")
            
            if prev_pt is not None:
                # Calculate distance between the current point and the previous point
                dx = pt.x - prev_pt.x
                dy = pt.y - prev_pt.y
                arc_length += math.sqrt(dx**2 + dy**2)  # Add the distance to the total arc length

            # Update previous point to the current point
            prev_pt = pt
        
        for p in points:
            f.write(f"{p.x} {p.y} 0\n")
            
    print("Curve arclenght: ", arc_length)

splinePoints(points[:2])
splinePoints(points[:3])
splinePoints(points[:4])
splinePoints(points[:5])
splinePoints(points[:6])
    


