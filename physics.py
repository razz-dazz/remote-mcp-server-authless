"""
Physics engine for Pocket Physics.
Handles all physics calculations including gravity, momentum, friction, and collisions.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Vector2D:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

@dataclass
class PhysicsObject:
    position: Vector2D
    velocity: Vector2D
    acceleration: Vector2D
    mass: float
    friction_coefficient: float = 0.1
    restitution: float = 0.8  # Bounce factor
    
    def apply_force(self, force: Vector2D):
        """Apply a force to the object."""
        # F = ma -> a = F/m
        self.acceleration = force * (1.0 / self.mass)

class PhysicsEngine:
    def __init__(self):
        self.gravity = Vector2D(0, -9.81)  # Standard gravity
        self.objects: List[PhysicsObject] = []
        
    def add_object(self, obj: PhysicsObject):
        """Add a physics object to the simulation."""
        self.objects.append(obj)
        
    def remove_object(self, obj: PhysicsObject):
        """Remove a physics object from the simulation."""
        if obj in self.objects:
            self.objects.remove(obj)
            
    def update(self, delta_time: float):
        """Update physics simulation for all objects."""
        for obj in self.objects:
            # Apply gravity
            gravitational_force = self.gravity * obj.mass
            obj.apply_force(gravitational_force)
            
            # Update velocity
            obj.velocity = obj.velocity + obj.acceleration * delta_time
            
            # Apply friction
            if obj.velocity.x != 0 or obj.velocity.y != 0:
                friction_magnitude = obj.friction_coefficient * obj.mass * abs(self.gravity.y)
                friction_direction = Vector2D(
                    -math.copysign(1, obj.velocity.x),
                    -math.copysign(1, obj.velocity.y)
                )
                friction_force = friction_direction * friction_magnitude
                obj.apply_force(friction_force)
            
            # Update position
            obj.position = obj.position + obj.velocity * delta_time
            
            # Reset acceleration for next frame
            obj.acceleration = Vector2D(0, 0)
            
            # Basic collision with ground (y = 0)
            if obj.position.y < 0:
                obj.position.y = 0
                obj.velocity.y = -obj.velocity.y * obj.restitution
                
    def check_collision(self, obj1: PhysicsObject, obj2: PhysicsObject) -> bool:
        """
        Basic collision detection between two objects.
        This is a simplified version - in a real implementation, 
        you'd want more sophisticated collision detection.
        """
        # For now, treating objects as points with a minimum distance
        min_distance = 1.0  # Minimum distance for collision
        dx = obj1.position.x - obj2.position.x
        dy = obj1.position.y - obj2.position.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < min_distance
        
    def resolve_collision(self, obj1: PhysicsObject, obj2: PhysicsObject):
        """
        Basic collision resolution using elastic collisions.
        This is a simplified version - in a real implementation,
        you'd want more sophisticated collision resolution.
        """
        # Calculate collision normal
        dx = obj2.position.x - obj1.position.x
        dy = obj2.position.y - obj1.position.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance == 0:
            return  # Avoid division by zero
            
        normal = Vector2D(dx / distance, dy / distance)
        
        # Calculate relative velocity
        relative_velocity = obj2.velocity + (obj1.velocity * -1)
        
        # Calculate impulse scalar
        restitution = min(obj1.restitution, obj2.restitution)
        impulse_scalar = -(1 + restitution) * (
            relative_velocity.x * normal.x + relative_velocity.y * normal.y
        ) / (1/obj1.mass + 1/obj2.mass)
        
        # Apply impulse
        impulse = normal * impulse_scalar
        obj1.velocity = obj1.velocity + (impulse * (-1/obj1.mass))
        obj2.velocity = obj2.velocity + (impulse * (1/obj2.mass))

if __name__ == "__main__":
    # Basic test of the physics engine
    engine = PhysicsEngine()
    
    # Create a test object (1kg mass at position (0, 10) with no initial velocity)
    test_object = PhysicsObject(
        position=Vector2D(0, 10),
        velocity=Vector2D(0, 0),
        acceleration=Vector2D(0, 0),
        mass=1.0
    )
    
    engine.add_object(test_object)
    
    # Simulate for a few steps
    for _ in range(10):
        engine.update(0.1)  # Update with 0.1 second timestep
        print(f"Position: ({test_object.position.x:.2f}, {test_object.position.y:.2f})")
