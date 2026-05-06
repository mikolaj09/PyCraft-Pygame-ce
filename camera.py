from tools import Singleton
from constants import *


class Camera(metaclass=Singleton):

    def __init__(self):
        self.offset = [0, 0]
        self.last_displacement = [0, 0]
        self.x = 0
        self.dx = 0
        self.moved = None
        self.camera_needs_moving = False

    def reset(self):
        self.offset = [0, 0]
        self.last_displacement = [0, 0]
        self.moved = None
        self.camera_needs_moving = False

    def set_camera(self, column):
        for block in column:
            block.position = camera.update_position(block.world_position, self.offset)

    def update(self, chunk, offset):
        self.camera_needs_moving = abs(self.offset[0] - offset[0]) + abs(self.offset[1] - offset[1]) != 0
        self.offset = offset
        if self.camera_needs_moving:
            for x, chunk1 in enumerate(chunk):
                for y, block in enumerate(chunk1):
                    block.position = self.update_position(block.world_position, self.offset)

        self.dx = self.last_displacement[0] // BLOCK_SIZE - self.x

        self.x = self.last_displacement[0] // BLOCK_SIZE

        self.moved = self.dx
        self.last_displacement[0] = self.offset[0] if abs(self.last_displacement[0] - self.offset[0]) >= BLOCK_SIZE else self.last_displacement[0]
        self.last_displacement[1] = self.offset[1] if abs(self.last_displacement[1] - self.offset[1]) >= BLOCK_SIZE else self.last_displacement[1]

    @staticmethod
    def update_position(position, offset):
        return position[0] - offset[0], position[1] - offset[1]


camera = Camera()
