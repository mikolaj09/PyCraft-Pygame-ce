import blocks
import entity
import display
import camera
from tools import Singleton
from world_generator import WorldGenerator
from entity import get_entity_types
from sprites import *
from constants import *


class World(metaclass=Singleton):

    def __init__(self, world_type, seed, gamemode):
        blocks.Block.world = self
        self.gamemode = blocks.Block.GAMEMODE = gamemode
        self.world_type = world_type
        self.block_sprites = Sprites.BLOCKS
        self.world = []
        self.original_world = []
        self.original_world_starting_index = None
        self.chunk = []
        self.chunk_start_index = None
        self.entities = set()
        self.entity_types = get_entity_types(Sprites.ENTITIES)
        self.generator = WorldGenerator(seed, world_type)
        self.seed = seed
        self.camera = camera.camera

    def get_x_y_world(self, position: tuple, offset=None) -> tuple:
        x, y = self.get_x_y_chunk(position, offset)
        x += self.world.index(self.chunk[0])
        return x, y

    def get_block_world(self, position: tuple, offset=None) -> blocks.Block:
        x, y = self.get_x_y_world(position, offset)
        return self.world[x][y] if 0 <= x < len(self.world) and 0 <= y < len(self.world[0]) else self.world[0][0]

    def get_x_y_chunk(self, position: tuple, offset=None) -> tuple:
        if offset is None:
            offset = [0, 0]
        x = ((position[0] + offset[0] - self.world[0][0].position[0]) // BLOCK_SIZE) - self.world.index(self.chunk[0])
        y = (position[1] + offset[1]) // BLOCK_SIZE
        return x, y

    def get_block_chunk(self, position: tuple, offset=None) -> blocks.Block:
        if offset is None:
            offset = [0, 0]
        x = ((position[0] + offset[0] - self.world[0][0].position[0]) // BLOCK_SIZE) - self.world.index(self.chunk[0])
        y = (position[1] + offset[1]) // BLOCK_SIZE
        return self.chunk[x][y] if 0 <= x < len(self.chunk) and 0 <= y < len(self.chunk[0]) else self.chunk[0][0]

    def summon_entity(self, position, total_offset):
        entity1 = entity.Entity(self.entity_types, ZOMBIE)
        self.entities.add(entity1)
        entity1.set_position(position, total_offset)
        entity1.spawn()

    def generate_new_world(self):
        self.world, self.chunk = self.generator.generate_new_world()
        self.chunk_start_index = (ORIGINAL_WORLD_SIZE - CHUNK_SIZE) // 2
        self.original_world = self.world[:]

    def generate_new_chunk(self, player):
        self.world, direction = self.generator.generate_new_chunk(self.world, player)
        self.chunk_start_index = self.chunk_start_index + 1 if direction == -1 else self.chunk_start_index
        self.generator.change_biome()

    def change_chunk(self):

        while abs(self.camera.moved) > 0:
            if self.camera.moved > 0:
                added_chunk = self.world[self.chunk_start_index + CHUNK_SIZE]
                deleted_chunk = self.chunk.pop(0)
                self.chunk.append(added_chunk)
                for block in deleted_chunk:
                    block.delete_body()
            elif self.camera.moved < 0:
                added_chunk = self.world[self.chunk_start_index - 1]
                deleted_chunk = self.chunk.pop(-1)
                self.chunk.insert(0, added_chunk)
                for block in deleted_chunk:
                    block.delete_body()

            self.chunk_start_index += (self.camera.moved // abs(self.camera.moved))
            self.camera.moved -= 1 if self.camera.moved > 0 else -1

    def update_blocks(self, mouse_position):
        block: blocks.Block
        for x, column in enumerate(self.chunk):
            for y, block in enumerate(column):
                block.update(x, y, self.chunk, column, mouse_position)

    def update_entities(self, total_offset):
        for entity1 in self.entities:
            entity1.update(total_offset)

    def respawn(self):
        for entity1 in self.entities:
            entity1.kill()
        self.entities = set()
        for x, column in enumerate(self.world):
            for y, block in enumerate(column):
                block.reset_position()
        self.chunk = self.original_world[(ORIGINAL_WORLD_SIZE - CHUNK_SIZE) // 2:(ORIGINAL_WORLD_SIZE + CHUNK_SIZE) // 2]
        self.chunk_start_index = (ORIGINAL_WORLD_SIZE - CHUNK_SIZE) // 2
        self.camera.reset()
        for x, column in enumerate(self.world):
            for y, block in enumerate(column):
                block.delete_body()

    def draw(self, player_position, player_offset):

        x1, y1 = self.get_x_y_chunk(player_position, player_offset)

        min_y = max(0, y1 - 15)
        max_y = min(len(self.chunk[0]), y1 + 15)

        for entity1 in self.entities:
            display.display.add_sprites(entity1.get_sprites())

        for x, column in enumerate(self.chunk):
            for y in range(min_y, max_y):
                display.display.add_sprites(column[y].get_sprites())

    def update(self, player, mouse_position):
        self.camera.update(self.chunk, player.total_offset)
        if bool(self.camera.moved):
            self.generate_new_chunk(player)
            self.change_chunk()
        self.update_blocks(mouse_position)
        self.update_entities(player.total_offset)


world_instance = None
