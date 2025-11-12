import pygame
import random
from entity_component_system import *

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MAX_ENEMIES = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Create systems
entity_manager = EntityManager()
physics_system = PhysicsSystem()
render_system = RenderSystem()
input_system = InputSystem(speed=150)
collision_system = CollisionSystem((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create player
player = entity_manager.create_entity()
physics_system.add(
    player,
    pos=(random.randrange(0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT)),
    size=random.randrange(6, 12),
)
render_system.add(
    player,
    colour=(random.randrange(255), random.randrange(255), random.randrange(255)),
    size=random.randrange(6, 12),
    physics=physics_system,
)
input_system.set_target(player, random.randrange(50, 100))

# Create enemy
for i in range(MAX_ENEMIES):
    enemy = entity_manager.create_entity()
    physics_system.add(
        enemy,
        pos=(random.randrange(0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT)),
        vel=(random.randrange(-100, 100), random.randrange(-100, 100)),
        size=random.randrange(6, 12),
    )
    render_system.add(
        enemy,
        colour=(random.randrange(255), random.randrange(255), random.randrange(255)),
        size=random.randrange(6, 12),
        physics=physics_system,
    )

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
    collision_system.update(physics_system)

    # Render
    screen.fill("purple")  # Fill the display with a solid colour
    render_system.draw(screen, physics_system)
    pygame.display.flip()  # refresh on-screen display

    clock.tick(60)  # wait until next frame (at 60 fps)

pygame.quit()
raise SystemExit
