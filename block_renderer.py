from constants import *
from block_types import BlockTypes


class BlockRenderer:

    def __init__(self, block):
        self.block = block
        self.sprite = block.sprite
        self.damaged_sprites = BlockTypes.damaged_sprites

    def change_sprites(self):
        self.sprite = BlockTypes.BLOCKS[self.block.name][SURFACE]

    def get_sprites(self) -> list:
        sprites = []
        if self.block.name != AIR:
            sprites.append((self.block.sprite, self.block.position))
            if self.block.logic.dug:
                damage = self.block.logic.digging_stage / self.block.toughness
                if damage <= 1 / 3:
                    sprites.append((self.damaged_sprites[0], self.block.position))
                elif damage <= 2 / 3:
                    sprites.append((self.damaged_sprites[1], self.block.position))
                else:
                    sprites.append((self.damaged_sprites[2], self.block.position))
        sprites.append((BlockTypes.brightness_effect[self.block.light_cell.lightness], self.block.position))
        return sprites
