"""
Entry point for Pocket Physics game.
Initializes and runs the game engine, physics engine, and renderer.
"""

from engine.game import GameEngine
from engine.physics import PhysicsEngine, PhysicsObject, Vector2D
from engine.renderer import Renderer, Color
import time

def main():
    # Initialize components
    game_engine = GameEngine()
    physics_engine = PhysicsEngine()
    renderer = Renderer()
    
    # Create a test physics object
    test_object = PhysicsObject(
        position=Vector2D(0, 50),
        velocity=Vector2D(0, 0),
        acceleration=Vector2D(0, 0),
        mass=1.0
    )
    
    physics_engine.add_object(test_object)
    renderer.add_object(test_object, Color(0.0, 1.0, 0.0))  # Green color
    
    game_engine.initialize()
    
    try:
        while game_engine.running:
            game_engine.update()
            
            # Update physics with delta time
            physics_engine.update(game_engine.delta_time)
            
            # Render the scene
            renderer.render()
            
            # Handle events and check if window should close
            if not renderer.handle_events():
                print("Window close event detected. Shutting down game engine.")
                game_engine.shutdown()
            
            # Sleep to maintain 60 FPS
            time.sleep(1/60)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down game engine.")
        game_engine.shutdown()
    finally:
        print("Cleaning up renderer resources.")
        renderer.cleanup()

if __name__ == "__main__":
    main()
