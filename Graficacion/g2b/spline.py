import math
import random
class Point():
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
        
points = []
resolution = 1000

for i in range(12):
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
            
        for p in points:
            f.write(f"{p.x} {p.y} 0\n")
        

splinePoints(points)

    


