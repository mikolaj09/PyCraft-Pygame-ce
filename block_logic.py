from random import randint
from functools import cache
from constants import *


class BlockLogic:

    def __init__(self, block):
        self.block = block
        self.block_type = block.block_type
        self.rigid = self.block_type == RIGID
        self.fluid = self.block_type == FLUID
        self.able_to_fall = self.block_type == FALLING
        self.on_edge = False
        self.dug = False
        self.digging_stage = 0

        if self.rigid:
            self.update = self.rigid_block_update
        elif self.fluid:
            self.update = self.fluid_update
        elif self.able_to_fall:
            self.update = self.falling_block_update
        else:
            raise ValueError()

    def change_logic(self):
        self.block_type = self.block.block_type
        self.rigid = self.block_type == RIGID
        self.fluid = self.block_type == FLUID
        self.able_to_fall = self.block_type == FALLING

        if self.rigid:
            self.update = self.rigid_block_update
        elif self.fluid:
            self.update = self.fluid_update
        elif self.able_to_fall:
            self.update = self.falling_block_update
        else:
            raise ValueError()

    def liquid_update(self, x, y, chunk, chunk1, mouse_position):
        if y + 1 < len(chunk1):
            if chunk1[y + 1].name == AIR:
                chunk1[y + 1].change_block(self.block.name)
            if x + 1 < len(chunk):
                if chunk[x + 1][y].name == AIR and not chunk1[y + 1].fluid:
                    chunk[x + 1][y].change_block(self.block.name)
            if x > 0:
                if chunk[x - 1][y].name == AIR and not chunk1[y + 1].fluid:
                    chunk[x - 1][y].change_block(self.block.name)

    def fluid_update(self, x, y, chunk, chunk1, mouse_position):
        if chunk1[y].name != AIR and self.block.liquid:
            self.liquid_update(x, y, chunk, chunk1, mouse_position)

    def bedrock_update(self, x, y, chunk, chunk1, mouse_position):
        self.on_edge = BlockLogic.check_on_edge(x, y, chunk)
        self.block.generate_body()

    def rigid_block_update(self, x, y, chunk, chunk1, mouse_position):

        self.on_edge = BlockLogic.check_on_edge(x, y, chunk)

        if self.digging_stage > 0:
            if not self.block.check_point(mouse_position):
                self.digging_stage = 0
                self.dug = False

        if self.on_edge:
            if self.block.name == GRASS:
                if randint(0, 5000) == 0 and chunk1[y - 1].name == AIR:
                    chunk1[y - 1].change_block(SHORT_GRASS)
            if self.block.name == DIRT:
                if randint(0, 1000) == 0 and chunk1[y - 1].name == AIR:
                    self.block.change_block(GRASS)
            if self.block.name == SHORT_GRASS:
                if chunk1[y + 1].name == AIR:
                    self.block.change_block(AIR)

            if self.block.hitbox.body is None:
                self.block.generate_body()
            else:
                self.block.add_body_to_space()
        else:
            self.block.remove_body_from_space()

    def falling_block_update(self, x, y, chunk, chunk1, mouse_position):

        self.on_edge = BlockLogic.check_on_edge(x, y, chunk)

        if self.digging_stage > 0:
            if not self.block.check_point(mouse_position):
                self.digging_stage = 0
                self.dug = False

        if self.on_edge:
            if self.block.name == GRASS:
                if randint(0, 5000) == 0 and chunk1[y - 1].name == AIR:
                    chunk1[y - 1].change_block(SHORT_GRASS)
            if self.block.name == DIRT:
                if randint(0, 1000) == 0 and chunk1[y - 1].name == AIR:
                    self.block.change_block(GRASS)
            if self.block.name == SHORT_GRASS:
                if chunk1[y + 1].name == AIR:
                    self.block.change_block(AIR)

            if self.block.hitbox.body is None:
                self.block.generate_body()
            else:
                self.block.add_body_to_space()
        else:
            self.block.remove_body_from_space()

    @staticmethod
    def check_on_edge(x: int, y: int, chunk) -> bool:
        if x + 1 < CHUNK_SIZE and not chunk[x + 1][y].solid:
            return True
        if x > 0 and not chunk[x - 1][y].solid:
            return True
        if y + 1 < WORLD_HEIGHT and not chunk[x][y + 1].solid:
            return True
        if y > 0 and not chunk[x][y - 1].solid:
            return True
        if y + 1 == WORLD_HEIGHT or y == 0:
            return True
        return False


@cache
def is_visible(x: int, y: int, player_position: tuple) -> bool:
    dx = x + BLOCK_SIZE // 2 - player_position[0]
    dy = y + BLOCK_SIZE // 2 - player_position[1]
    return dx * dx + dy * dy <= 250000
