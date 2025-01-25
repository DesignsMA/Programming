import math
import os
import subprocess

class Point():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

points = [Point(0, 0), Point(3, 6), Point(8, 6), Point(11, 2.1), Point(13.2, -2.77), Point(21, 1), Point(27, 10)]
resolution = 3000

def factorial(x: int):
    if x == 1 or x == 0:
        return 1
    else:
        return x * factorial(x - 1)

def binomial(n: int, k: int):
    return factorial(n) / (factorial(k) * factorial(n - k))

def generateImage(fileName: str = "bezier_data.txt", x: str = "noparam", y:  str = "noparam", lenght: float = 0.0):
    
    try:
        os.mkdir("output")
    except FileExistsError:
        print("Directory already created")
        
    command = f"gnuplot -e \"set terminal pngcairo size 1000, 1000;\
           set output \'output/{fileName.split(".")[0]}.png\';\
           set zeroaxis;\
           set label 1 'Lenght: {lenght}' at 0.6,0.4 left font 'DejaVu Sans Bold,12';\
           set label 2 '{x.strip('\n')}' at 0.6,0.2 left font 'DejaVu Sans Bold,12';\
           set label 3 '{y.strip('\n')}' at 0.6,0 left font 'DejaVu Sans Bold,12';\
           set key left;\
           unset xtics;\
           unset ytics;\
           set border 0;\
           plot \'{fileName}\' using 1:2 with points title \'Curve\' ps 0.4 pt 7 lc rgb '#ff5353',\
            \'{fileName}\' using 1:2:3 with points title \'Control\' ps 3 pt 7 lc rgb \'#bb3030\';\
            "
    subprocess.run(command, shell=True)


def splinePoints(points: list[Point], fileName: str = "bezier_data.txt"):
    n = len(points) - 1
    cfs = []
    arc_length = 0
    prev_pt = None  # Initialize previous point as None
    polynomial_formula_x = ""
    polynomial_formula_y = ""

    with open(fileName, 'w') as f:
        for u in range(n + 1):
            cfs.append(binomial(n, u))  # Calculate binomial coefficients

        for i in range(resolution):
            t = 0 + 1 * i / resolution  # For each t in the range 0-1
            pt = Point(0, 0)  # Create a new point for each iteration
            term_x = ""
            term_y = ""

            for u in range(n + 1):
                pt.x += cfs[u] * points[u].x * math.pow((1 - t), n - u) * math.pow(t, u)
                pt.y += cfs[u] * points[u].y * math.pow((1 - t), n - u) * math.pow(t, u)

                # Construct the polynomial terms
                term_x += f"{cfs[u] * points[u].x:.2f}*(1-t)^{n - u}*t^{u} + "
                term_y += f"{cfs[u] * points[u].y:.2f}*(1-t)^{n - u}*t^{u} + "

            # Remove the trailing " + " from the terms
            term_x = term_x[:-3]
            term_y = term_y[:-3]

            

            # Write the point to the file
            f.write(f"{pt.x} {pt.y}\n")

            if prev_pt is not None:
                dx = pt.x - prev_pt.x  # Calculate differential
                dy = pt.y - prev_pt.y
                arc_length += math.sqrt(dx**2 + dy**2)  # Add the distance to the arc length

            # Update previous point to the current point
            prev_pt = Point(pt.x, pt.y)  # Store a copy of the current point
        
        # Append the terms to the polynomial formulas
        polynomial_formula_x += f"x(t) = {term_x}\n"
        polynomial_formula_y += f"y(t) = {term_y}\n"
        
        for p in points:  # Write the control points
            f.write(f"{p.x} {p.y} 0\n")

        print("Ecuación Parametrica:\n", polynomial_formula_x, polynomial_formula_y)

    print("\nCurve arclength: ", arc_length)
    return polynomial_formula_x, polynomial_formula_y, arc_length

# *func() desempaca la tupla como elementos individuales, son enviados como argumentos de generateImage
#generateImage("g1.txt", *splinePoints(points[:2], "g1.txt"))
#generateImage("g2.txt", *splinePoints(points[:3], "g2.txt"))
#generateImage("g3.txt", *splinePoints(points[:4], "g3.txt"))
#generateImage("g4.txt", *splinePoints(points[:5], "g4.txt"))
#generateImage("g5.txt", *splinePoints(points[:6], "g5.txt"))
#generateImage("g6.txt", *splinePoints(points[:7], "g6.txt"))