import pyvista as pv
import numpy as np
from time import sleep

def move_box_animated(box, target_center, steps=20):
    current_center = np.array(box.center)
    displacement = (target_center - current_center) / steps
    
    plotter = pv.Plotter()
    actor = plotter.add_mesh(box, color="orange", show_edges=True)
    plotter.add_axes()
    plotter.show(interactive_update=True)  # Modo interactivo
    
    for _ in range(steps):
        box.translate(displacement, inplace=True)
        plotter.update()
        sleep(0.05)
    
    plotter.show()  # Mantener ventana abierta

# Ejemplo de uso
box = pv.Box(bounds=(1, 3, 2, 4, 0, 2))  # Centro inicial en (2, 3, 1)
move_box_animated(box, target_center=[5.0, 0.0, 1.0])