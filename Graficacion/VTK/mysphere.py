# noinspection PyUnresolvedReferences
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkJPEGReader, vtkPNGReader
from vtkmodules.vtkRenderingCore import vtkTexture
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere
import os

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
)
from myfigure import Figure

class Sphere(Figure):
    def __init__(self, center: tuple = (0, 0, 0), radius: float = 1.0, 
                 resolution: int = 100, color: str = "#ff5353", texture_path: str = None):
        """
        Initialize a VTK sphere with optional texture.

        Args:
            center (tuple): (x, y, z) sphere center coordinates
            radius (float): Sphere radius
            resolution (int): Angular resolution
            color (str): Fallback hex color if no texture
            texture_path (str): Path to texture image (JPEG/PNG)
        """
        # Create sphere geometry
        self.sphere_source = vtkSphereSource()
        self.sphere_source.SetCenter(*center)
        self.sphere_source.SetRadius(radius)
        self.sphere_source.SetPhiResolution(resolution)
        self.sphere_source.SetThetaResolution(resolution)

        # Initialize parent class
        super().__init__(self.sphere_source, color)

        # Store parameters
        self.center = center
        self.radius = radius
        self.resolution = resolution
        self.texture_path = texture_path

        # Handle texture if path provided
        if self.texture_path:
            self._setup_texture()

    def _setup_texture(self):
        """Load and apply texture to the sphere."""
        try:
            # Fix path formatting for Windows
            texture_path = os.path.normpath(self.texture_path)
            
            # Verify file exists
            if not os.path.exists(texture_path):
                raise FileNotFoundError(f"Texture file not found: {texture_path}")

            # Load appropriate reader
            if texture_path.lower().endswith(('.jpg', '.jpeg')):
                reader = vtkJPEGReader()
            elif texture_path.lower().endswith('.png'):
                reader = vtkPNGReader()
            else:
                raise ValueError("Only JPEG/PNG textures supported")
            
            reader.SetFileName(texture_path)
            reader.Update()

            # Create texture coordinates
            texture_map = vtkTextureMapToSphere()
            texture_map.SetInputConnection(self.sphere_source.GetOutputPort())
            texture_map.PreventSeamOn()
            texture_map.Update()

            # Create and apply texture
            texture = vtkTexture()
            texture.SetInputConnection(reader.GetOutputPort())
            texture.InterpolateOn()

            # Update mapper with textured geometry
            mapper = vtkPolyDataMapper()
            mapper.SetInputConnection(texture_map.GetOutputPort())
            
            self.actor = vtkActor()
            self.actor.SetMapper(mapper)
            self.actor.SetTexture(texture)

        except Exception as e:
            print(f"Error loading texture: {e}")
            # Fall back to solid color if texture fails
            self._update_actor_with_color()

    def _update_actor_with_color(self):
        """Fallback method to create actor with solid color."""
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(self.sphere_source.GetOutputPort())
        
        self.actor = vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(*self._hex_to_rgb(self.color))

    def _update_actor(self):
        """Override parent method to handle both cases."""
        if hasattr(self, 'actor'):
            return  # Already created
        
        if self.texture_path:
            self._setup_texture()
        else:
            self._update_actor_with_color()