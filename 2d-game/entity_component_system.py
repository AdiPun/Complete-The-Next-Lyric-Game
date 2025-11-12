import numpy as np
import pygame

MAX_ENTITIES = 1024

# ENTITIES


class EntityManager:
    def __init__(self):
        self.next_id = 0
        self.max_entities = MAX_ENTITIES
        self.active = np.zeros(
            MAX_ENTITIES, dtype=bool
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
        self.entities = {}  # A dictionary of entities to look up colour and size

    def add(self, eid, colour=(255, 255, 255), size=8, physics=None):
        if physics:
            size = physics.radius[eid] * 2
        self.entities[eid] = {"colour": colour, "size": size}

    def draw(self, screen, physics):
        for eid, comp in self.entities.items():
            if physics.active[eid]:
                pos = physics.pos[eid]
                pygame.draw.circle(
                    screen, comp["colour"], pos.astype(int), comp["size"]
                )


class PhysicsSystem:
    def __init__(self):
        self.pos = np.zeros((MAX_ENTITIES, 2), dtype=float)
        self.vel = np.zeros((MAX_ENTITIES, 2), dtype=float)
        self.active = np.zeros(MAX_ENTITIES, dtype=bool)
        self.radius = np.zeros(MAX_ENTITIES, dtype=float)

    def add(self, eid, pos=(0, 0), vel=(0, 0), size=10):
        self.pos[eid] = pos
        self.vel[eid] = vel
        self.active[eid] = True
        self.radius[eid] = size / 2

    def remove(self, eid):
        self.active[eid] = False

    def update(self, dt):
        self.pos[self.active] += (
            self.vel[self.active] * dt
        )  # Adds the velocities to the positions of the active physics components


class InputSystem:
    def __init__(self, speed=80):
        self.speed = speed
        self.target_id = None

    def set_target(self, eid, speed=80):
        self.target_id = eid
        self.speed = speed

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


class CollisionSystem:
    def __init__(self, screen_size, bounce=True):
        self.width, self.height = screen_size
        self.bounce = bounce

    def update(self, physics):
        # Only choose entities with active physics components
        # np.where returns a tuple so we just want the first set

        active_ids = np.where(physics.active)[0]

        for eid in active_ids:
            x, y = physics.pos[eid]
            vx, vy = physics.vel[eid]
            r = physics.radius[eid]

            # Bounce off walls
            # Bounce x plane

            if x + r > self.width:
                x = self.width - r
                vx = -abs(vx) if self.bounce else 0
            elif x - r < 0:
                x = r
                vx = abs(vx) if self.bounce else 0

            # Bounce y plane

            if y + r > self.height:
                y = self.height - r
                vy = -abs(vy) if self.bounce else 0
            if y - r < 0:
                y = r
                vy = abs(vy) if self.bounce else 0

            # Bounce between entities
            for oeid in active_ids:

                # Skips itself
                if oeid == eid:
                    continue

                ox, oy = physics.pos[oeid]
                ovx, ovy = physics.vel[oeid]
                orad = physics.radius[oeid]

                dx = x - ox
                dy = y - oy

                if dx * dx + dy * dy <= (r + orad) ** 2:

                    # Oppose velocities
                    vx, ovx = -vx, -ovx
                    vy, ovy = -vy, -ovy

                    # Separate slightly
                    overlap = (r + orad) - np.sqrt(dx * dx + dy * dy)
                    x += (dx / (abs(dx) + 1e-6)) * overlap * 0.5
                    y += (dy / (abs(dy) + 1e-6)) * overlap * 0.5
                    ox -= (dx / (abs(dx) + 1e-6)) * overlap * 0.5
                    oy -= (dy / (abs(dy) + 1e-6)) * overlap * 0.5

                    physics.pos[oeid] = (ox, oy)
                    physics.vel[oeid] = (ovx, ovy)

            # Update entity position and velocity
            physics.pos[eid] = (x, y)
            physics.vel[eid] = (vx, vy)
