import pygame
import pymunk
import space
from constants import *


class BlockHitbox:

    def __init__(self, block):
        self.block = block
        self.body = None
        self.shape = None
        self.rect = pygame.Rect(*self.block.position, BLOCK_SIZE, BLOCK_SIZE)

    def change_hitbox(self):
        if not self.block.solid:
            self.delete_body()

    def generate_body(self):
        if self.block.solid and not self.block.fluid:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body.position = [self.block.world_position[0] + BLOCK_SIZE // 2, self.block.world_position[1] + BLOCK_SIZE // 2]
            self.shape = pymunk.Poly.create_box(self.body, size=(BLOCK_SIZE, BLOCK_SIZE))
            self.shape.friction = self.block.properties[FRICTION]
            self.shape.elasticity = self.block.properties[ELASTICITY]
            space.space_instance.add(self.body, self.shape)

    def generate_falling_body(self):
        if self.block.solid and not self.block.fluid:
            self.body = pymunk.Body(10, float('inf'), body_type=pymunk.Body.DYNAMIC)
            self.body.position = [self.block.world_position[0] + BLOCK_SIZE // 2, self.block.world_position[1] + BLOCK_SIZE // 2]
            self.shape = pymunk.Poly.create_box(self.body, size=(BLOCK_SIZE, BLOCK_SIZE))
            self.shape.friction = self.block.properties[FRICTION]
            self.shape.elasticity = self.block.properties[ELASTICITY]
            space.space_instance.add(self.body, self.shape)

    def add_body_to_space(self):
        if self.body is not None and self.shape is not None and not self.body.space:
            space.space_instance.add(self.body, self.shape)

    def delete_body(self):
        self.remove_body_from_space()
        self.body = None
        self.shape = None

    def remove_body_from_space(self):
        if self.body is not None and self.shape is not None and self.body.space:
            space.space_instance.remove(self.body, self.shape)

    def check_point(self, point):
        self.rect.topleft = self.block.position
        return self.rect.collidepoint(point)
