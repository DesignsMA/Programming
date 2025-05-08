# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
import random
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkPoints
)

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

from mysphere import Sphere
from mycube import Cube


def main():
    
    cube = Cube(center=(0,0,0),size=2, color="#ffffff")
    
    # Cube vertices (half-size = 1.0 since cube size = 2.0)
    vertices = [
        (1, 1, 1),    # Front-top-right
        (1, 1, -1),   # Front-top-left
        (1, -1, 1),   # Front-bottom-right
        (1, -1, -1),  # Front-bottom-left
        (-1, 1, 1),   # Back-top-right
        (-1, 1, -1),  # Back-top-left
        (-1, -1, 1),  # Back-bottom-right
        (-1, -1, -1)  # Back-bottom-left
    ]
    
    spheres = []
    for i, vertex in enumerate(vertices[:6]):  # Just first 6 vertices
        # Genera valores RGB aleatorios (0–255), y conviértelos a hex
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        sphere = Sphere(center=vertex, radius=0.3)
        sphere.color = hex_color
        sphere._update_actor_with_color()

        spheres.append(sphere)
    
    renderer(Actors=spheres+[cube])

def renderer(camPos: tuple = (1,1,1), Actors: list = [], width: int = 1280, height: int = 720):
    colors = vtkNamedColors()
    camera = vtkCamera()
    camera.SetPosition(*camPos)
    camera.SetFocalPoint(0, 0, 0)

    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    for actor in Actors:
        renderer.AddActor(actor.get_actor())
        
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()
    renderer.SetBackground(colors.GetColor3d("Cornsilk"))

    renWin.SetSize(width, height)
    renWin.SetWindowName("Render")

    # interact with data
    renWin.Render()
    iren.Start()



if __name__ == "__main__":
    main()