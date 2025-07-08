"""
Integration test for Pocket Physics.
Tests the interaction between physics engine, renderer, and game engine.
"""

from engine.game import GameEngine
from engine.physics import PhysicsEngine, PhysicsObject, Vector2D
from engine.renderer import Renderer, Color
import time

def main():
    # Initialize components
    game_engine = GameEngine()
    physics_engine = PhysicsEngine()
    renderer = Renderer(800, 600)
    
    # Create test objects with different properties
    objects = [
        # Stationary object in center
        PhysicsObject(
            position=Vector2D(0, 0),
            velocity=Vector2D(0, 0),
            acceleration=Vector2D(0, 0),
            mass=1.0,
            restitution=0.8
        ),
        # Object falling from top
        PhysicsObject(
            position=Vector2D(0, 200),
            velocity=Vector2D(0, 0),
            acceleration=Vector2D(0, 0),
            mass=1.0,
            restitution=0.8
        ),
        # Object moving diagonally
        PhysicsObject(
            position=Vector2D(-100, 100),
            velocity=Vector2D(50, 0),
            acceleration=Vector2D(0, 0),
            mass=2.0,
            restitution=0.5
        )
    ]
    
    # Add objects to physics engine and renderer
    colors = [Color(1.0, 0.0, 0.0), Color(0.0, 1.0, 0.0), Color(0.0, 0.0, 1.0)]
    for obj, color in zip(objects, colors):
        physics_engine.add_object(obj)
        renderer.add_object(obj, color)
    
    # Initialize game
    game_engine.initialize()
    
    print("Starting integration test...")
    print("Controls:")
    print("- ESC: Exit")
    print("- Space: Toggle pause")
    print("Testing physics simulation, rendering, and game loop...")
    
    try:
        while game_engine.running:
            # Update game state
            game_engine.update()
            
            if not game_engine.paused:
                # Update physics
                physics_engine.update(game_engine.delta_time)
            
            # Render frame
            renderer.render()
            
            # Handle events (returns False if window should close)
            if not renderer.handle_events():
                game_engine.shutdown()
            
            # Maintain reasonable frame rate
            time.sleep(1/60)
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        print("Cleaning up...")
        renderer.cleanup()
        print("Integration test complete")

if __name__ == "__main__":
    main()
