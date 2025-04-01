# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
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
    paths = [
        r"D:\Users\sepma\Downloads\Data\C728\Git\C-C++-C#\C\git\Graficacion\VTK\PyVista\imgs\difraccion-1.jpg",  
        r"D:\Users\sepma\Downloads\Data\C728\Git\C-C++-C#\C\git\Graficacion\VTK\PyVista\imgs\difraccion-2.jpg",  
        r"D:\Users\sepma\Downloads\Data\C728\Git\C-C++-C#\C\git\Graficacion\VTK\PyVista\imgs\difraccion-3.jpg",  
        r"D:\Users\sepma\Downloads\Data\C728\Git\C-C++-C#\C\git\Graficacion\VTK\PyVista\imgs\difraccion-4.jpg",  
        r"D:\Users\sepma\Downloads\Data\C728\Git\C-C++-C#\C\git\Graficacion\VTK\PyVista\imgs\difraccion-5.jpg",  
        r"D:\Users\sepma\Downloads\Data\C728\Git\C-C++-C#\C\git\Graficacion\VTK\PyVista\imgs\difraccion-1.jpg",  
    ]
    
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
        sphere = Sphere(center=vertex, radius=0.3, texture_path=paths[i])
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