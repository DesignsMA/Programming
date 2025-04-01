from vtkmodules.vtkFiltersGeneral import vtkBooleanOperationPolyDataFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData
)

class Figure:
    def __init__(self, source: vtkPolyData, color: str = "#ff5353"):
        """
        Initialize a Figure with a VTK source and color.
        
        Args:
            source: VTK source object (e.g., vtkSphereSource, vtkBooleanOperationPolyDataFilter)
            color: Hex color string (default: "#ff5353")
        """
        self.source = source
        self.color = color
        self.actor = None
        self._update_actor()
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color string to normalized RGB tuple (0-1 range)."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def _update_actor(self):
        """Internal method to update the actor when source or color changes."""
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(self.source.GetOutputPort())
        
        self.actor = vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(*self._hex_to_rgb(self.color))
    
    def set_color(self, color: str):
        """Set the color of the figure using a hex string."""
        self.color = color
        if self.actor:
            self.actor.GetProperty().SetColor(*self._hex_to_rgb(color))
    
    def union(self, other):
        """Combine this figure with another figure."""
        return self._boolean_operation(other, 'union')
    
    def intersection(self, other):
        """Get the intersection with another figure."""
        return self._boolean_operation(other, 'intersection')
    
    def difference(self, other):
        """Subtract another figure from this one."""
        return self._boolean_operation(other, 'difference')
    
    def _boolean_operation(self, other, operation_type: str):
        """
        Internal method to perform boolean operations.
        
        Args:
            other: Another Figure instance
            operation_type: 'union', 'intersection', or 'difference'
        
        Returns:
            New Figure instance with the result
        """
        if not isinstance(other, Figure):
            raise ValueError("Operand must be a Figure instance")
        
        boolean_op = vtkBooleanOperationPolyDataFilter()
        
        if operation_type == 'union':
            boolean_op.SetOperationToUnion()
        elif operation_type == 'intersection':
            boolean_op.SetOperationToIntersection()
        elif operation_type == 'difference':
            boolean_op.SetOperationToDifference()
        else:
            raise ValueError(f"Unknown operation type: {operation_type}")
        
        boolean_op.SetInputConnection(0, self.source.GetOutputPort())
        boolean_op.SetInputConnection(1, other.source.GetOutputPort())
        
        return Figure(boolean_op, self.color)  # Inherits color from first operand
    
    def get_actor(self) -> vtkActor:
        """Get the VTK actor for rendering."""
        if self.actor is None:
            self._update_actor()
        return self.actor