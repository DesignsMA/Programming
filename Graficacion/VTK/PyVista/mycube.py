# noinspection PyUnresolvedReferences
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkPoints
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData
)

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
)



from myfigure import Figure

class Cube(Figure):
    
    def __init__(self, center: tuple = (0, 0, 0), size: float = 1.0, 
                 color: str = "#ff5353"):
        """
        Initialize a VTK cube actor with customizable properties.

        Args:
            center (tuple): (x, y, z) coordinates of cube center (default: (0, 0, 0))
            size (float): Length of cube edges (default: 1.0)
            color (str): Hex color string (e.g., "#FF5353") (default: "#ff5353")
        """
        # Create cube geometry
        cube = self._create_cube(center, size)
        
        # Initialize the Figure parent class
        super().__init__(cube, color)

        # Store parameters as attributes
        self.center = center
        self.size = size

    def _create_cube(self, center, size):
        """Internal method to create cube geometry"""
        # Calculate half-size for centering
        hs = size / 2.0
        cx, cy, cz = center
        
        # Define 8 vertices of the cube (offset by center)
        x = [
            (cx - hs, cy - hs, cz - hs), (cx + hs, cy - hs, cz - hs),
            (cx + hs, cy + hs, cz - hs), (cx - hs, cy + hs, cz - hs),
            (cx - hs, cy - hs, cz + hs), (cx + hs, cy - hs, cz + hs),
            (cx + hs, cy + hs, cz + hs), (cx - hs, cy + hs, cz + hs)
        ]

        # Define 6 faces (quadrilaterals) of the cube
        pts = [
            (0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
            (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)
        ]

        # Create VTK objects
        cube = vtkPolyData()
        points = vtkPoints()
        polys = vtkCellArray()

        # Load the point, cell, and data attributes
        for i, xi in enumerate(x):
            points.InsertPoint(i, xi)
        for pt in pts:
            polys.InsertNextCell(self._mk_vtk_id_list(pt))

        # Assign pieces to vtkPolyData
        cube.SetPoints(points)
        cube.SetPolys(polys)
        
        return cube

    def _mk_vtk_id_list(self, it):
        """Helper to create vtkIdList from Python iterable"""
        vil = vtkIdList()
        for i in it:
            vil.InsertNextId(int(i))
        return vil
    
    def _update_actor(self):
        """
        Overridden method to update the actor with specific cube rendering settings.
        Creates mapper and actor with scalar visibility and range.
        """
        # Create mapper with specific cube settings
        cubeMapper = vtkPolyDataMapper()
        cubeMapper.SetInputData(self.source)
        cubeMapper.ScalarVisibilityOff()  # Disable scalar coloring
        
        # Create actor
        self.actor = vtkActor()
        self.actor.SetMapper(cubeMapper)
        
        # Set color property
        self.actor.GetProperty().SetColor(*self._hex_to_rgb(self.color))
