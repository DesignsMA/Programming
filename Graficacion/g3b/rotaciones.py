import math


def rotate_z_3d(points: list[ list[float] ] , theta: float):
    """
    Rota los puntos alrededor del eje Z.
    param: points: Lista de puntos en formato [[x, y, z], ...]
    param: theta: Ángulo de rotación en radianes
    """
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)

    for point in points:
        x, y, z = point
        point[0] = x * cos_theta - y * sin_theta
        point[1] = x * sin_theta + y * cos_theta
        # z no cambia en la rotación en Z
        point[2] = z


def rotate_x_3d(points: list[ list[float] ] , theta: float):
    """
    Rota los puntos alrededor del eje X.
    :param points: Lista de puntos en formato [[x, y, z], ...]
    :param theta: Ángulo de rotación en radianes
    """
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)

    for point in points:
        x, y, z = point
        point[1] = y * cos_theta - z * sin_theta
        point[2] = y * sin_theta + z * cos_theta
        # x no cambia en la rotación en X
        point[0] = x


def rotate_y_3d(points: list[ list[float] ] , theta: float):
    """
    Rota los puntos alrededor del eje Y.
    :param points: Lista de puntos en formato [[x, y, z], ...]
    :param theta: Ángulo de rotación en radianes
    """
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)

    for point in points:
        x, y, z = point
        point[0] = x * cos_theta + z * sin_theta # nueva x
        point[2] = z * cos_theta - x * sin_theta # nueva z
        # y no cambia en la rotación en Y
        point[1] = y
        
#def rotate_circle(points: list[ list[float] ] , theta: float, axis: str):
    
    

