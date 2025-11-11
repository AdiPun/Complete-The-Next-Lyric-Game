import pygame
from entity_component_system import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Create systems
entity_manager = EntityManager()
physics_system = PhysicsSystem()
render_system = RenderSystem()
input_system = InputSystem(speed=150)

# Create player
player = entity_manager.create_entity()
physics_system.add(player, pos=(200, 200))
render_system.add(player, colour=(255, 255, 255), size=10)
input_system.set_target(player)

# Create enemy
enemy = entity_manager.create_entity()
physics_system.add(enemy, pos=(100, 100), vel=(30, 20))
render_system.add(enemy, colour=(255, 0, 0), size=6)

# Main game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds
    # Process player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    input_system.update(physics_system)
    physics_system.update(dt)

    # Render
    screen.fill("purple")  # Fill the display with a solid colour
    render_system.draw(screen, physics_system)
    pygame.display.flip()  # refresh on-screen display

    clock.tick(60)  # wait until next frame (at 60 fps)

pygame.quit()
raise SystemExit
