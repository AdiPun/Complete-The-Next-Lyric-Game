import numpy as np
import pygame

# ENTITIES


class EntityManager:
    def __init__(self, max_entities=1024):
        self.next_id = 0
        self.max_entities = max_entities
        self.active = np.zeros(
            max_entities, dtype=bool
        )  # Creates an array of 1024 False bools

    def create_entity(self):
        if self.next_id >= self.max_entities:
            raise Exception("Max entities reached!")
        eid = self.next_id
        self.active[eid] = True
        self.next_id += 1
        return eid

    def destroy_entity(self, eid):
        self.active[eid] = False


# SYSTEMS


class RenderSystem:
    def __init__(self):
        self.entities = {} # A dictionary of entities to look up colour and size

    def add(self, eid, colour=(255, 255, 255), size=8):
        self.entities[eid] = {"colour": colour, "size": size}

    def draw(self, screen, physics):
        for eid, comp in self.entities.items():
            if physics.active[eid]:
                pos = physics.pos[eid]
                pygame.draw.circle(
                    screen, comp["colour"], pos.astype(int), comp["size"]
                )


class PhysicsSystem:
    def __init__(self, max_entities=1024):
        self.pos = np.zeros((max_entities, 2), dtype=float) # Creates an array of 1024 (0.0,0.0)'s
        self.vel = np.zeros((max_entities, 2), dtype=float)
        self.active = np.zeros(max_entities, dtype=bool)

    def add(self, eid, pos=(0, 0), vel=(0, 0)):
        self.pos[eid] = pos
        self.vel[eid] = vel
        self.active[eid] = True

    def remove(self, eid):
        self.active[eid] = False

    def update(self, dt):
        self.pos[self.active] += self.vel[self.active] * dt # Adds the velocities to the positions of the active physics components


class InputSystem:
    def __init__(self, speed=120):
        self.speed = speed
        self.target_id = None

    def set_target(self, eid):
        self.target_id = eid

    def update(self, physics):
        if self.target_id is None:
            return

        keys = pygame.key.get_pressed()
        vel = np.zeros(2, dtype=float)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel[0] -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel[0] += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vel[1] -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vel[1] += 1

        # Normalising diagonal movement so no b hopping
        if np.any(vel):
            vel = vel / np.linalg.norm(vel) * self.speed

        physics.vel[self.target_id] = vel
