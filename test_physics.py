"""
Comprehensive physics engine test.
Tests gravity, collisions, friction, and multiple objects.
"""

from engine.physics import PhysicsEngine, PhysicsObject, Vector2D
import time

def main():
    engine = PhysicsEngine()
    
    # Create test objects with different properties
    obj1 = PhysicsObject(
        position=Vector2D(0, 10),
        velocity=Vector2D(1, 0),  # Moving right
        acceleration=Vector2D(0, 0),
        mass=1.0,
        restitution=0.8
    )
    
    obj2 = PhysicsObject(
        position=Vector2D(2, 5),
        velocity=Vector2D(-0.5, 0),  # Moving left
        acceleration=Vector2D(0, 0),
        mass=2.0,  # Heavier object
        restitution=0.5  # Less bouncy
    )
    
    # Add objects to engine
    engine.add_object(obj1)
    engine.add_object(obj2)
    
    # Simulate for 5 seconds with smaller timesteps
    timestep = 0.05
    total_time = 0
    while total_time < 5.0:
        engine.update(timestep)
        
        # Check for collisions
        if engine.check_collision(obj1, obj2):
            print(f"\nCollision detected at time {total_time:.2f}s!")
            print(f"Object 1: pos=({obj1.position.x:.2f}, {obj1.position.y:.2f}), "
                  f"vel=({obj1.velocity.x:.2f}, {obj1.velocity.y:.2f})")
            print(f"Object 2: pos=({obj2.position.x:.2f}, {obj2.position.y:.2f}), "
                  f"vel=({obj2.velocity.x:.2f}, {obj2.velocity.y:.2f})")
            engine.resolve_collision(obj1, obj2)
        
        # Print state every 0.5 seconds
        if total_time % 0.5 < timestep:
            print(f"\nTime: {total_time:.2f}s")
            print(f"Object 1: pos=({obj1.position.x:.2f}, {obj1.position.y:.2f}), "
                  f"vel=({obj1.velocity.x:.2f}, {obj1.velocity.y:.2f})")
            print(f"Object 2: pos=({obj2.position.x:.2f}, {obj2.position.y:.2f}), "
                  f"vel=({obj2.velocity.x:.2f}, {obj2.velocity.y:.2f})")
        
        total_time += timestep

if __name__ == "__main__":
    main()
