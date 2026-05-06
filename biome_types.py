from constants import *


class BiomeTypes:

    def __init__(self):
        self.plains = {LAYERS: [(AIR, 30, 1), (GRASS, 1, 0), (DIRT, 7, 1), (STONE, 38, 1), (DARKSTONE, 40, 1)], MAX_DELTA: 5, FLATNESS: 4}
        self.mountains = {LAYERS: [(AIR, 25, 1), (GRASS, 1, 0), (DIRT, 3, 1), (STONE, 38, 1), (DARKSTONE, 40, 1)], MAX_DELTA: 30, FLATNESS: 2}
        self.desert = {LAYERS: [(AIR, 30, 1), (SAND, 10, 0), (STONE, 36, 1), (DARKSTONE, 40, 1)], MAX_DELTA: 3, FLATNESS: 6}
        self.ice_plains = {LAYERS: [(AIR, 30, 1), (SNOW, 1, 0), (SNOWY_GRASS, 1, 0), (DIRT, 7, 1), (STONE, 37, 1), (DARKSTONE, 40, 1)], MAX_DELTA: 5, FLATNESS: 8}
        self.ocean = {LAYERS: [(AIR, 40, 0), (WATER, 20, 1), (SAND, 2, 1), (STONE, 37, 1), (DARKSTONE, 40, 1)], MAX_DELTA: 3, FLATNESS: 8}
        self.biomes = {PLAINS: self.plains, MOUNTAINS: self.mountains, DESERT: self.desert, ICE_PLAINS: self.ice_plains, OCEAN: self.ocean}

    def get_biome_properties(self, name):
        if name in self.biomes:
            return self.biomes[name]
        raise ValueError('Inappropriate biome type')
