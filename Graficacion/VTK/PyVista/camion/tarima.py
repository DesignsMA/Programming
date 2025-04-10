import pyvista as pv
import numpy as np
from time import sleep

# Configuración inicial
pv.set_plot_theme("document")
plotter = pv.Plotter()

# Crear el trailer (contenedor principal)
#(xMin, xMax, yMin, yMax, zMin, zMax)
trailer = pv.Box(bounds=(0, 6, 0, 3, 0, 3))  # 6m x 3m x 3m
plotter.add_mesh(trailer, color="tan", opacity=0.2, name="trailer")

# Crear las cajas
def create_box(size, position, color, name):
    box = pv.Box(bounds=(
        position[0], position[0] + size[0],
        position[1], position[1] + size[1],
        position[2], position[2] + size[2]
    ))
    plotter.add_mesh(box, color=color, name=name)
    return box

def definirCajas():
    # Posiciones iniciales de las cajas en el área de stock
    # 10 cajas de 2x1x1 (20 m³)
    big_boxes = []
    for i in range(10):
        h = i+0.05*i
        pos = [7,0, h] # 1 de separación del camion
        box = create_box([2, 1, 1], pos, "red", f"big_box_{i}")
        big_boxes.append(box)

    # 16 cajas de 1x1x1 (16 m³)
    small_boxes = []
    for i in range(16):
        h = i+0.05*i
        x = i//8 # dividir en 8
        if x == 1:
            h = i+0.05*i - (8+0.05*8)
            x = 1+0.05
        pos = [7,1+x, h]
        box = create_box([1, 1, 1], pos, "blue", f"small_box_{i}")
        small_boxes.append(box)
    
    return small_boxes, big_boxes

# Función para mover una caja a una posición específica
def move_box(box:pv.PolyData, target_center, steps=20,lwh:  list = [1,1,1]):
    box.rotate_y(-90,inplace=True)
    current_center = np.array(box.center)
    displacement = ((target_center - current_center)+np.array((lwh[0]/2,lwh[1]/2,lwh[2]/2))) / steps
    for _ in range(steps):
        box.translate(displacement, inplace=True)
        plotter.update()
        sleep(0.05)

# Primera combinación: Todas las cajas grandes primero
def combination_1():
    small_boxes, big_boxes = definirCajas()
    # Mover cajas grandes (2x1x1)
    positions = [
        [0, 0, 0], [0, 1, 0], [0, 2, 0],  # Fila inferior
        [1, 0, 0], [1, 1, 0], [1, 2, 0],  # Fila media
        [2, 0, 0], [2, 1, 0], [2, 2, 0],  # Fila superior
        [3, 0, 0]  # Una caja apilada
    ]
    
    for i, pos in enumerate(positions[:10]):
        move_box(big_boxes[i], pos, lwh=[1,1,2])
    
    # Mover cajas pequeñas (1x1x1)
    small_positions = [
        [0, 0, 2], [1, 0, 2], [2, 0, 2], [3, 0, 2], [3, 1, 1], [3, 2,1],
        [0, 1, 2], [1, 1, 2], [2, 1, 2], [3, 1, 2], [3, 1, 0], [3, 2, 0],
        [0, 2, 2], [1, 2, 2], [2, 2, 2], [3, 2, 2]
    ]
    
    for i, pos in enumerate(small_positions[:16]):
        move_box(small_boxes[i], pos)

# Segunda combinación: Mezcla de cajas grandes y pequeñas con rotaciones
def combination_2():
    small_boxes, big_boxes = definirCajas()
    # Acomodo más eficiente de cajas pequeñas
    small_positions = [
        [0, 0, 0], [0, 1, 0], [0, 2, 0],  # Apiladas
        [0, 0, 1], [0, 1, 1], [0, 2, 1],
        [0, 0, 2], [0, 1, 2], [0, 2, 2],
        [1, 0, 0], [1, 1, 0], [1, 2, 0],  # Apiladas
        [1, 0, 1], [1, 1, 1], [1, 2, 1],
        [1, 0, 2]
    ]
    
    for i, pos in enumerate(small_positions[:16]):
        move_box(small_boxes[i], pos)
        
    # Posiciones con cajas rotadas
    positions_big = [
        [2, 0, 0], [2, 1, 0], [2, 2, 0],
        [3, 0, 0], [3, 1, 0], [3, 2, 0], 
        [4, 0, 0], [4, 1, 0], [4, 2, 0],
        [5, 0, 0],   # Caja rotada en nivel superior
    ]
    
    for i, pos in enumerate(positions_big[:10]):
        move_box(big_boxes[i], pos,lwh=[1,1,2])
    

# Configurar botones para las combinaciones
plotter.add_text("Presiona:\n1 - Mejor Espacio\n2 - Mejor Acceso\nx - Salir", 
                position="lower_left", font_size=10)

def exitprogram():
    plotter.close()
    exit()

plotter.add_key_event("1", lambda: combination_1())
plotter.add_key_event("2", lambda: combination_2())
plotter.add_key_event("x", lambda: exitprogram())

# Configuración de la cámara
plotter.camera.position = (10, 5, 10)
plotter.camera.focal_point = (3, 1.5, 1.5)
plotter.show(interactive_update=True, auto_close=False)
definirCajas()
plotter.show()