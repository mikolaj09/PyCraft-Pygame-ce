import pygame
import pymunk
import math
import space
import display
from random import choice, choices, randint
from abc import ABC, abstractmethod
from constants import *


class EntityBase(ABC):

    def __init__(self, entities, name):
        self.sprite = pygame.transform.scale(entities.entities[name][SURFACE], (PLAYER_WIDTH * BLOCK_SIZE // DEFAULT_BLOCK_SIZE, PLAYER_HEIGHT * BLOCK_SIZE // DEFAULT_BLOCK_SIZE))
        self.position = [display.display.width // 2, display.display.height // 2]
        self.rect = self.sprite.get_rect(center=(display.display.width // 2, display.display.height // 2))
        self.health_points = 0

        self.body = None
        self.shape = None

    @property
    def alive(self):
        """Checks if the entity is alive"""
        return self.health_points > 0

    @abstractmethod
    def spawn(self) -> None:
        """Spawns the entity"""
        pass

    @abstractmethod
    def get_sprites(self) -> list:
        """Returns sprites of entity"""
        pass

    @abstractmethod
    def update(self, offset: tuple[int, int] or list[int, int]) -> None:
        """Updates the entity"""
        pass

    def kill(self) -> None:
        """Removes the entity from space"""


class EntityLogic:

    def __init__(self):
        self.direction = choice((True, False))
        self.time1 = 0
        self.time2 = 0
        self.time3 = 0
        self.moving = False

    @staticmethod
    def _move_right(body):
        body.apply_force_at_local_point((100000, 0))

    @staticmethod
    def _move_left(body):
        body.apply_force_at_local_point((-100000, 0))

    @staticmethod
    def _jump(body):
        if round(body.velocity[1]) == 0:
            body.apply_impulse_at_local_point((0, -30000))

    def _change_direction(self):
        self.direction = not self.direction

    def passive_step(self, body):
        if self.time1 > randint(5, 30):
            self._change_direction()
            self.time1 = 0

        if choices((True, False), weights=[1, 4]):
            self.moving = not self.moving

        if self.moving:
            self._move_right(body) if self.direction else self._move_left(body)

        if self.moving and round(body.velocity[1]) == 0 and round(body.velocity[0]) == 0:
            self._jump(body)
            self.time2 = 0

    def update(self, body):
        self.time1 += 1 / 60
        self.time2 += 1 / 60
        self.time3 += 1 / 60
        self.passive_step(body)


class Entity(EntityBase):

    def __init__(self, entities, name):
        super().__init__(entities, name)
        self.logic = EntityLogic()

        body = pymunk.Body(100, float('inf'), pymunk.Body.DYNAMIC)
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
        shape.elasticity = 0.2
        body.damping = 0.5

        self.body = body
        self.shape = shape

    def spawn(self):
        self.health_points = 20
        space.space_instance.add(self.body, self.shape)

    def set_position(self, position, total_offset):
        self.position = position
        self.body.position = [self.position[0] + total_offset[0] + 20, self.position[1] + total_offset[1] + 20]

    def get_sprites(self) -> list:
        return [(self.sprite, self.position)]

    def update(self, total_offset):
        self.position = [self.body.position[0] - 12 - total_offset[0], self.body.position[1] - 36 - total_offset[1]]
        self.logic.update(self.body)

    def kill(self):
        if self.body.space:
            space.space_instance.remove(self.body, self.shape)


class EntityTypes:
    def __init__(self, sprites):

        self.entities = {PLAYER: {SURFACE: None, HEALTH: 20, SPEED: 10},
                         ZOMBIE: {SURFACE: None, HEALTH: 20, SPEED: 4},
                         PIG:    {SURFACE: None, HEALTH: 10, SPEED: 6}}

        for i in sprites:
            name = i[NAME][:-4]
            if name in self.entities:
                self.entities[name][SURFACE] = i[SURFACE]


_entity_types_instance = None


def get_entity_types(sprites=None):
    global _entity_types_instance
    if _entity_types_instance is None:
        if sprites is None:
            raise ValueError()
        _entity_types_instance = EntityTypes(sprites)
    return _entity_types_instance
