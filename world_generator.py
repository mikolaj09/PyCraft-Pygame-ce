import random
import display
from blocks import Block
from biome_types import BiomeTypes
from constants import *


class WorldGenerator:
    def __init__(self, seed, world_type):
        self.seed = seed
        self.world_type = world_type
        self.left_surface_level = 0
        self.left_total_delta_height = 0
        self.right_total_delta_height = 0
        self.right_surface_level = 0
        self.biome_types = BiomeTypes()
        self.current_biome = None
        self.current_biome_name = ''
        self.current_biome_length = 0

    def generate_new_world(self):
        x = int(-ORIGINAL_WORLD_SIZE / 2 * BLOCK_SIZE + display.display.width // 2)
        y = 0
        world = []
        random.seed(self.seed)
        while self.current_biome_name == '' or self.current_biome_name == OCEAN:
            self.current_biome_name = random.choice(tuple(self.biome_types.biomes.keys()))
        self.current_biome = self.biome_types.get_biome_properties(self.current_biome_name)
        if self.world_type == FLAT:
            for i in range(ORIGINAL_WORLD_SIZE):
                world.append(self._generate_column(x, y, RIGHT)[0])
                x += BLOCK_SIZE

        elif self.world_type == NORMAL:
            height = random.randint(30, 40)
            self.left_surface_level = height
            self.right_surface_level = height
            for i in range(ORIGINAL_WORLD_SIZE):
                generator = self._generate_column(x, y, RIGHT)
                world.append(generator[0])
                self.right_surface_level = generator[1]
                x += BLOCK_SIZE
            self.current_biome_length = ORIGINAL_WORLD_SIZE

        chunk = world[(ORIGINAL_WORLD_SIZE - CHUNK_SIZE) // 2:(ORIGINAL_WORLD_SIZE + CHUNK_SIZE) // 2]

        return world, chunk

    def change_biome(self):
        if self.current_biome_length >= 500 + random.randint(-50, 50):
            self.current_biome_name = random.choice(tuple(self.biome_types.biomes.keys()))
            self.current_biome = self.biome_types.get_biome_properties(self.current_biome_name)
            self.current_biome_length = 0

    def generate_new_chunk(self, world, player):

        chunk_length = BLOCK_SIZE * CHUNK_SIZE
        left_distance = abs(world[0][0].world_position[0] - player.total_offset[0] - player.renderer.player_rect.centerx)
        right_distance = abs(world[-1][0].world_position[0] + BLOCK_SIZE - player.total_offset[0] - player.renderer.player_rect.centerx)
        direction = 0
        if right_distance < chunk_length:
            x = world[-1][0].position[0] + BLOCK_SIZE
            y = world[0][0].position[1]
            world_y, height = self._generate_column(x, y, RIGHT)
            if height != -1:
                self.right_surface_level = height
            world.append(world_y)
            direction = 1
        elif left_distance < chunk_length:
            x = world[0][0].position[0] - BLOCK_SIZE
            y = world[0][0].position[1]
            world_y, height = self._generate_column(x, y, LEFT)
            if height != -1:
                self.left_surface_level = height
            world.insert(0, world_y)
            direction = -1
        return world, direction

    def _generate_column(self, x, y1, side=''):
        self.current_biome_length += 1
        world_y = []
        if self.world_type == FLAT:
            for y in range(0, BLOCK_SIZE * WORLD_HEIGHT, BLOCK_SIZE):
                if y // BLOCK_SIZE <= 93:
                    world_y.append(Block(AIR, (x, y + y1)))
                elif y // BLOCK_SIZE == 94:
                    world_y.append(Block(GRASS, (x, y + y1)))
                elif y // BLOCK_SIZE <= 96:
                    world_y.append(Block(DIRT, (x, y + y1)))
                elif y // BLOCK_SIZE <= 98:
                    world_y.append(Block(STONE, (x, y + y1)))
                elif y // BLOCK_SIZE == 99:
                    world_y.append(Block(BEDROCK, (x, y + y1)))
            return world_y, -1

        elif self.world_type == NORMAL:
            delta_height = random.choice([-1, 1] + [0] * self.current_biome[FLATNESS])
            if side == RIGHT:
                height = self.right_surface_level
                if abs(self.right_total_delta_height + delta_height) < self.current_biome[MAX_DELTA]:
                    self.right_total_delta_height += delta_height
                total_delta_height = self.right_total_delta_height
            elif side == LEFT:
                height = self.left_surface_level
                if abs(self.left_total_delta_height + delta_height) < self.current_biome[MAX_DELTA]:
                    self.left_total_delta_height += delta_height
                total_delta_height = self.left_total_delta_height
            else:
                height = 0
                total_delta_height = 0
            if 20 < height + delta_height < 50:
                height += delta_height
            current_layer = 0
            i = 0
            for y in range(0, BLOCK_SIZE * WORLD_HEIGHT, BLOCK_SIZE):
                if y // BLOCK_SIZE != 99:
                    world_y.append(Block(self.current_biome[LAYERS][current_layer][0], (x, y + y1)))
                else:
                    world_y.append(Block(BEDROCK, (x, y + y1)))
                i += 1
                if self.current_biome[LAYERS][current_layer][2]:
                    if i >= self.current_biome[LAYERS][current_layer][1] + total_delta_height:
                        current_layer += 1
                        if current_layer == len(self.current_biome[LAYERS]):
                            current_layer -= 1
                        i = 0
                else:
                    if i >= self.current_biome[LAYERS][current_layer][1]:
                        current_layer += 1
                        if current_layer == len(self.current_biome[LAYERS]):
                            current_layer -= 1
                        i = 0
            return world_y, height
        raise ValueError('Inappropriate world type')
