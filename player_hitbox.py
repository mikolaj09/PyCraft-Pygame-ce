import pygame
import pymunk
import world
import math
import space
import display
from constants import *


class PlayerHitBox:

    def __init__(self, player):
        self.player = player
        self.gamemode = self.player.gamemode
        self.running = False
        self.body = None
        self.shape = None
        self.generate_new_body()
        self.moving = False
        self.jumping = False
        self.direction = None

    @property
    def max_velocity(self):
        return PLAYER_RUNNING_SPEED * BLOCK_SIZE // DEFAULT_BLOCK_SIZE if self.running else PLAYER_SPEED * BLOCK_SIZE // DEFAULT_BLOCK_SIZE

    @property
    def _force_value(self):
        return PLAYER_RUNNING_MOVEMENT_FORCE * (BLOCK_SIZE // DEFAULT_BLOCK_SIZE) ** 2 if self.running else PLAYER_MOVEMENT_FORCE * (BLOCK_SIZE // DEFAULT_BLOCK_SIZE) ** 2

    @property
    def _jump_force_value(self):
        return PLAYER_RUNNING_JUMP_FORCE * (BLOCK_SIZE // DEFAULT_BLOCK_SIZE) ** 2 if self.running else PLAYER_JUMP_FORCE * (BLOCK_SIZE // DEFAULT_BLOCK_SIZE) ** 2

    @property
    def _swim_force_value(self):
        return PLAYER_RUNNING_SWIMMING_FORCE * (BLOCK_SIZE // DEFAULT_BLOCK_SIZE) ** 2 if self.running else PLAYER_SWIMMING_FORCE * (BLOCK_SIZE // DEFAULT_BLOCK_SIZE) ** 2

    def add_body_to_space(self):
        if self.body is not None and self.shape is not None and not self.body.space:
            space.space_instance.add(self.body, self.shape)

    def delete_body_from_space(self):
        if self.body is not None and self.shape is not None and self.body.space:
            space.space_instance.remove(self.body, self.shape)
            self.body = None
            self.shape = None

    def generate_new_body(self):
        self.body = type('Body', (object,), {'position': (display.display.width // 2, display.display.height // 2), 'space': False})
        self.shape = None
        if self.gamemode != SPECTATOR:
            body = pymunk.Body(200, float('inf'), pymunk.Body.DYNAMIC)
            body.position = (display.display.width // 2, display.display.height // 2)
            rx = PLAYER_WIDTH // 2 * BLOCK_SIZE // DEFAULT_BLOCK_SIZE
            ry = PLAYER_HEIGHT // 2 * BLOCK_SIZE // DEFAULT_BLOCK_SIZE
            points = []
            for i in range(50):
                angle = 2 * math.pi * i / 50
                x = math.cos(angle) * rx
                y = math.sin(angle) * ry
                points.append((x, y))

            shape = pymunk.Poly(body, points)
            shape.friction = 0.7
            shape.elasticity = 0.15
            body.damping = 0.6
            self.body = body
            self.shape = shape

    def move(self, keys1, keys2):
        if self.gamemode != SPECTATOR:
            block = self.locate_player_in_fluid(offset=[0, 20])
            self.running = keys1[pygame.K_LSHIFT]
            if block.name == AIR or (block.rigid and not block.solid):
                if keys2 == pygame.K_SPACE and round(self.body.velocity[1]) == 0:
                    self.body.apply_impulse_at_local_point((0, -self._jump_force_value))
            elif keys1[pygame.K_SPACE]:
                self.body.apply_force_at_local_point((0, -self._swim_force_value))

            if block.fluid:
                self._resistance(block.resistance)

            if keys1[pygame.K_d] and abs(self.body.velocity[0]) < self.max_velocity:
                self.body.apply_force_at_local_point((self._force_value, 0))
            elif keys1[pygame.K_a] and abs(self.body.velocity[0]) < self.max_velocity:
                self.body.apply_force_at_local_point((-self._force_value, 0))

            self.jumping = int(self.body.velocity[1]) < -50
            self.moving = abs(round(self.body.velocity[0])) > 0
            if round(self.body.velocity[0]) > 0:
                self.direction = RIGHT
            elif round(self.body.velocity[0]) < 0:
                self.direction = LEFT
        else:
            if keys1[pygame.K_SPACE]:
                self.body.position = [self.body.position[0], self.body.position[1] - 10]
            if keys1[pygame.K_LSHIFT]:
                self.body.position = [self.body.position[0], self.body.position[1] + 10]
            if keys1[pygame.K_d] or keys1[pygame.K_a]:
                if keys1[pygame.K_d]:
                    self.body.position = [self.body.position[0] + 10, self.body.position[1]]
                else:
                    self.body.position = [self.body.position[0] - 10, self.body.position[1]]

    def _resistance(self, resistance):

        if self.gamemode != SPECTATOR:
            if math.isinf(resistance):
                return

            x = -1 if self.body.velocity[0] > 0 else 1 if self.body.velocity[0] < 0 else 0
            y = -1 if self.body.velocity[1] > 0 else 1 if self.body.velocity[1] < 0 else 0
            constant = 15
            self.body.apply_force_at_local_point((
                x * resistance * self.body.velocity[0] ** 2 * constant,
                y * resistance * self.body.velocity[1] ** 2 * constant))

    def locate_player_in_fluid(self, offset=None):
        offset = (0, 0) if offset is None else offset
        return world.world_instance.get_block_chunk([self.player.renderer.player_rect.center[0] + offset[0],
                                                     self.player.renderer.player_rect.center[1] + offset[1]],
                                                    self.player.total_offset)

    def update(self, keys1, keys2):
        self.move(keys1, keys2)
