from mathObjects import *
import matplotlib.pyplot as plt
import numpy as np
import pprint as pp
import sys
from mpl_toolkits.mplot3d import Axes3D  # Importar herramientas 3D

class TensorProductSurface():
    """
    Inicializa una superficie de producto tensorial.

    Parámetros:
        controlPoints (np.ndarray, opcional): Matriz de puntos de control. Por defecto es None.
        type (int, opcional): Tipo de función base a utilizar (0: Bernstein, 1: B-spline). Por defecto es 0.
        subdivisions (int, opcional): Número de subdivisiones para generar la malla. Por defecto es 10.
    """
    def __init__(self, controlPoints: np.ndarray = None, typeS: int = 0, subdivisions: int = 10, splineGrade: int = 2):
        self.mesh = []
        self.controlPoints = controlPoints
        self.typeS = typeS
        self.function = self._select_function()
        self.subdivisions = subdivisions
        self.m = controlPoints.shape[0]
        self.n = controlPoints.shape[1]
        self.p = splineGrade
        self.knotType = list()
        if  typeS == 1:
            self.select_knot_type("u")
            self.select_knot_type("v")
                
    def _select_function(self):
        """
        Selecciona la función base según el tipo.
        """
        if self.typeS == 0:
            return self.bernstein_basis_polynomial
        elif self.typeS == 1:
            return self.b_spline
        else:
            raise ValueError("Tipo de función base no soportado.")
        
    def bernstein_basis_polynomial(self, v: int, n: int, x: int, opt: None = None): # ( n | v) | Me
        return binomial(n,v)*x**v*(1-x)**(n-v)
    
    def select_knot_type(self, uv: str):
        print(f"""
             Tipo de knot vector. Puede ser:
                0 - Periódico:
                    - Se utiliza para crear una superficie o curva continua y cerrada, de forma que los puntos de control finales se conecten\
                      de nuevo con los iniciales, generando una estructura "circular". Este tipo es ideal cuando se desea que la malla o curva\
                      tenga una continuidad en ambas direcciones y no haya "bordes" visibles.

                1 - Uniforme:
                    - Los intervalos entre los nodos son iguales, lo que genera una distribución uniforme de los puntos de control a lo largo de\
                      la curva o superficie. Este tipo es útil cuando se desea una distribución equidistante y controlada de los puntos, pero sin\
                      cerrarse (como en el caso periódico).

                2 - Abierto (Clásico):
                    - Este tipo de knot vector coloca varios nodos en el inicio y el final del intervalo, lo que asegura que los extremos de la\
                      curva o superficie lleguen exactamente a los primeros y últimos puntos de control, pero no tienen continuidad en esos puntos.\
                      Es muy común en curvas o superficies abiertas.

                3 - Clásico extendido (Con una pequeña variación en la distribución):
                    - Similar al tipo abierto, pero con una ligera variación en la distribución de los nodos intermedios. Este tipo puede ser útil\
                      para obtener una transición más suave en la parte exterior de la curva o superficie, especialmente cuando se desea un \
                      comportamiento más flexible en los bordes sin perder la adherencia a los puntos de control.
                Selecciona el knot vector en dirección {uv} : 
              """)
        try:
            tipo = int(input())
            if tipo not in [0, 1, 2, 3]:
                raise ValueError
        except:
            print("¡Entrada no válida! Usando tipo 0 por defecto.")
            tipo = 0
        self.knotType.append(tipo)
    
    def generate_knot_vector(self, n: int, direction: str):
        """
        Genera un knot vector (vector de nodos) para B-splines según el tipo seleccionado por el usuario.

        Parámetros:
            n (int): Número de puntos de control - 1.
            direction (str): Dirección en la que se genera el knot vector ("u" o "v").
        Retorna:
            list: Knot vector generado.
        """
        p = self.p
        if direction == "u":
            knot_type = self.knotType[0]  # Asume que self.knotType[0] es el tipo para "u"
        elif direction == "v":
            knot_type = self.knotType[1]  # Asume que self.knotType[1] es el tipo para "v"

        # Si se pasa un knot_type explícito como parámetro, usarlo
        if knot_type == 0:  # Periódico
            num_nodos = n + p + 2  # Número total de nudos
            knot_vector = [i / (num_nodos - 1) for i in range(num_nodos)]

        elif knot_type == 1:  # Uniforme
            # Distribuir los nudos uniformemente entre 0 y 1
            knot_vector = [i / (n + p) for i in range(n + p + 2)]

        elif knot_type == 2:  # Abierto (Clásico)
            knots = [0.0] * (p + 1)  # Primeros p+1 ceros
            num_intervalos = n - p + 1  # Número de intervalos intermedios
            for i in range(1, num_intervalos):
                knots.append(i / num_intervalos)  # Nodos intermedios entre 0 y 1
            knots += [1.0] * (p + 1)  # Últimos p+1 unos
            knot_vector = knots

        elif knot_type == 3:  # Clásico extendido
            # El clásico extendido es similar al abierto pero con una pequeña variación
            knots = [0.0] * (p + 1)  # Primeros p+1 ceros
            num_intervalos = n - p + 1  # Número de intervalos intermedios
            for i in range(1, num_intervalos):
                knots.append((i + 0.5) / num_intervalos)  # Ajuste en la distribución de nodos
            knots += [1.0] * (p + 1)  # Últimos p+1 unos
            knot_vector = knots

        else:
            raise ValueError("Tipo de knot vector no válido. Usa 0 para periódico, 1 para uniforme, 2 para abierto, 3 para clásico extendido.")
    
        return knot_vector

    def b_spline(self, i: int, p: int, x: float, knot_vector: list):
        """
        Calcula la función base B-spline N_{i,p}(x) utilizando el algoritmo recursivo de Cox-de Boor.
        """
        # Caso base: grado 0
        if p == 0:
            if knot_vector[i] <= x < knot_vector[i + 1]:
                return 1.0
            # Asegurar que en el último nodo se evalúe correctamente en 1.0
            elif x == 1.0 and knot_vector[i + 1] == 1.0:
                return 1.0
            else:
                return 0.0

        # Caso recursivo: grado p > 0
        else:
            term1 = 0.0
            term2 = 0.0

            if knot_vector[i + p] != knot_vector[i]:  # Evitar división por 0
                term1 = (x - knot_vector[i]) / (knot_vector[i + p] - knot_vector[i]) * self.b_spline(i, p - 1, x, knot_vector)

            if knot_vector[i + p + 1] != knot_vector[i + 1]:  # Evitar división por 0
                term2 = (knot_vector[i + p + 1] - x) / (knot_vector[i + p + 1] - knot_vector[i + 1]) * self.b_spline(i + 1, p - 1, x, knot_vector)

            return term1 + term2
    
    def generateCoordinate(self, u: float, v: float, attr: str):
        """
        Genera una coordenada (x, y o z) para un punto en la superficie.

        Parámetros:
            u (float): Parámetro en la dirección u.
            v (float): Parámetro en la dirección v.
            attr (str): Atributo de la coordenada a calcular ('x', 'y' o 'z').

        Retorna:
            float: Valor de la coordenada generada.
        """
        coord = 0.0

        vArg = self.n - 1
        uArg = self.m - 1
        optU = optV = None
        if self.typeS == 1:
            optU = self.generate_knot_vector(uArg, "u")  # Generar knot vector para u
            print("Dirección U: ",optU)
            optV = self.generate_knot_vector(vArg, "v")  # Generar knot vector para v
            print("Dirección V: ",optV)
            uArg = vArg = self.p

        for i in range(self.m):
            for j in range(self.n):
                if self.typeS == 0:
                    basis_u = self.bernstein_basis_polynomial(i, uArg, u, optU)
                    basis_v = self.bernstein_basis_polynomial(j, vArg, v, optV)
                elif self.typeS == 1:
                    basis_u = self.b_spline(i, uArg, u, optU)
                    basis_v = self.b_spline(j, vArg, v, optV)
                coord += getattr(self.controlPoints[i, j], attr) * basis_u * basis_v
        return coord

    def generate_mesh(self):
        if self.controlPoints is None:
            print("Se necesita de una matriz de puntos de control.")
            return
        
        for u_index in range(self.subdivisions + 1):
            u = u_index * (1.0 / self.subdivisions)  # Calcular en direccion u
            for v_index in range(self.subdivisions + 1):
                v = v_index * (1.0 / self.subdivisions)  # Calcular en direccion v
                x = self.generateCoordinate(u, v, 'x')
                y = self.generateCoordinate(u, v, 'y')
                z = self.generateCoordinate(u, v, 'z')
                self.mesh.append(Point(x, y, z))  # Añadir como punto       
    
    def interactiveGraph(self):
        for point in self.mesh:
            print(f"{point}", end=' | ')
        # Convertir a un array de numpy para facilitar la visualización
        mesh_points = np.array([[point.x, point.y, point.z] for point in self.mesh])

        pp.pp(mesh_points)
        # Reorganizar los puntos en una cuadrícula para la visualización 3D
        # mesh_points[:, 0] DE TODAS LAS FILAS, EXTRAE EL ELEMENTO CERO
        # .reshape(subdivisions, subdivisions)  MODIFCA EL ARREGLO 1D A 2D,, es decir si el arreglo 1d tiene 3 elementos y realizas un reshape(1,3)
        # obtienes un arreglo 2d con 3 filas donde sea [1,2,3] -> [ [1], [2], [3] ]
        subdivisions = self.subdivisions + 1
        X = mesh_points[:, 0].reshape(subdivisions, subdivisions)
        Y = mesh_points[:, 1].reshape(subdivisions, subdivisions)
        Z = mesh_points[:, 2].reshape(subdivisions, subdivisions)
        
        pp.pp(X)
        pp.pp(Y)
        pp.pp(Z)
        # Visualizar la malla en 3D
        fig = plt.figure() #nueva ventana
        #ax = fig.add_subplot(111, projection='3d'): Añade un subplot (gráfico) en la figura con proyección 3D. El argumento 111 indica que es el primer (y único) gráfico en una cuadrícula de 1x1.
        ax = fig.add_subplot(111, projection='3d')  # Crear un gráfico 3D

        # Graficar la superficie | la  superficie compuesta por los puntos
        ax.plot_surface(X, Y, Z, color='black', alpha=0.12)

        # Graficar los puntos de la malla
        ax.scatter(X, Y, Z, color='red')
        #extrae todos los elementos de la primera fila x[i,j] i = filas, j = columnas
        pp.pp(X[0,:])
        pp.pp(Y[0,:])
        pp.pp(Z[0,:])
        #extrae todos los elementos de la primera columna x[i,j] i = filas, j = columnas
        pp.pp(X[:,0])
        pp.pp(Y[:,0])
        pp.pp(Z[:,0])
        # Conectar los puntos con líneas
        for i in range(subdivisions):
            ax.plot(X[i, :], Y[i, :], Z[i, :], color='black')  # Líneas en dirección u
            ax.plot(X[:, i], Y[:, i], Z[:, i], color='black')  # Líneas en dirección v

        # Etiquetar los ejes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Agregar un título al gráfico
        plt.title('Superficie de bézier')

        # Mostrar el gráfico
        plt.show()
    
    def controlPointsGraph(self, control_points):
        # Visualizar la superficie
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Graficar puntos de control
        x = np.array([[p.x for p in row] for row in control_points])
        y = np.array([[p.y for p in row] for row in control_points])
        z = np.array([[p.z for p in row] for row in control_points])
        ax.scatter(x, y, z, c="red", s=50, label="Puntos de control")

        # Graficar la superficie
        # ax.plot_surface(surface_points_x, surface_points_y, surface_points_z, color="blue", alpha=0.5)

        # Etiquetas y título
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.title("Superficie B-spline")
        plt.legend()
        plt.show()

    def __main__(self):
        # Definir los puntos de control para las curvas de Bézier
        control_points = np.array([
            [Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 1), Point(3, 0, 0)],
            [Point(0, 1, 1), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 1)],
            [Point(0, 2, 1), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 1)],
            [Point(0, 3, 0), Point(1, 3, 1), Point(2, 3, 1), Point(3, 3, 0)]
        ])

        mesh = np.array([
                    [Point(-1, 0, 0), Point(0, 0, 1), Point(1, 0, 0)],
                    [Point(-1, -1.5, 0), Point(0, -1.5, 1), Point(1, -1.5, 0)],
                    [Point(-1, -3, 0), Point(0, -3, 1), Point(1, -3, 0)],
                    ])

        #malla = TensorProductSurface(controlPoints=control_points)
        #malla.generate_mesh()
        #malla.interactiveGraph()
        # Crear y visualizar la superficie B-spline
        malla2 = TensorProductSurface(controlPoints=mesh, typeS=1, subdivisions=24, splineGrade=2)
        malla2.generate_mesh()
        malla2.controlPointsGraph(control_points=mesh)
        malla2.interactiveGraph()
