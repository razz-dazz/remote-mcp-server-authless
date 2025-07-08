"""
2D rendering engine for Pocket Physics.
Handles all graphics rendering using OpenGL.
"""

import math
from typing import List, Tuple, Optional
import pygame
import OpenGL.GL as gl
import OpenGL.GLU as glu
from .physics import Vector2D, PhysicsObject

class Color:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class RenderObject:
    def __init__(self, physics_obj: PhysicsObject, color: Optional[Color] = None):
        self.physics_obj = physics_obj
        self.color = color or Color(1.0, 1.0, 1.0)  # Default to white
        self.vertices = self._generate_circle_vertices(32)  # 32 segments for circle
        
    def _generate_circle_vertices(self, segments: int) -> List[Tuple[float, float]]:
        """Generate vertices for a circle."""
        vertices = []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            x = math.cos(angle)
            y = math.sin(angle)
            vertices.append((x, y))
        return vertices

class Renderer:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.objects: List[RenderObject] = []
        self.camera_position = Vector2D(0, 0)
        self.zoom = 1.0
        
        # Initialize Pygame and OpenGL
        pygame.init()
        pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self._init_gl()
        
    def _init_gl(self):
        """Initialize OpenGL settings."""
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(-self.width/2, self.width/2, -self.height/2, self.height/2)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
        # Enable transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
    def add_object(self, physics_obj: PhysicsObject, color: Optional[Color] = None):
        """Add a physics object to be rendered."""
        render_obj = RenderObject(physics_obj, color)
        self.objects.append(render_obj)
        
    def remove_object(self, physics_obj: PhysicsObject):
        """Remove a physics object from rendering."""
        self.objects = [obj for obj in self.objects if obj.physics_obj != physics_obj]
        
    def set_camera(self, position: Vector2D, zoom: float = 1.0):
        """Set camera position and zoom level."""
        self.camera_position = position
        self.zoom = zoom
        
    def clear(self):
        """Clear the screen."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glLoadIdentity()
        
    def render(self):
        """Render all objects."""
        self.clear()
        
        # Apply camera transform
        gl.glTranslatef(-self.camera_position.x, -self.camera_position.y, 0)
        gl.glScalef(self.zoom, self.zoom, 1)
        
        # Render each object
        for obj in self.objects:
            self._render_object(obj)
            
        # Swap buffers
        pygame.display.flip()
        
    def _render_object(self, render_obj: RenderObject):
        """Render a single object."""
        gl.glPushMatrix()
        
        # Move to object position
        gl.glTranslatef(render_obj.physics_obj.position.x, 
                    render_obj.physics_obj.position.y, 0)
        
        # Set color
        gl.glColor4f(render_obj.color.r, render_obj.color.g, 
                 render_obj.color.b, render_obj.color.a)
        
        # Draw circle
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glVertex2f(0, 0)  # Center point
        for vertex in render_obj.vertices:
            gl.glVertex2f(vertex[0], vertex[1])
        # Close the circle
        gl.glVertex2f(render_obj.vertices[0][0], render_obj.vertices[0][1])
        gl.glEnd()
        
        gl.glPopMatrix()
        
    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if the window should close."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
        
    def cleanup(self):
        """Clean up resources."""
        pygame.quit()

if __name__ == "__main__":
    # Basic test of the renderer
    from .physics import PhysicsObject, Vector2D
    
renderer = Renderer()

# Create a test object
test_object = PhysicsObject(
    position=Vector2D(0, 0),
    velocity=Vector2D(0, 0),
    acceleration=Vector2D(0, 0),
    mass=1.0
)

# Add it to renderer with a red color
renderer.add_object(test_object, Color(1.0, 0.0, 0.0))

# Main loop
running = True
try:
    while running:
        running = renderer.handle_events()
        renderer.render()
finally:
    renderer.cleanup()
