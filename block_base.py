from abc import ABC, abstractmethod
from block_types import BlockTypes
from constants import *


class BlockBase(ABC):

    def __init__(self, name, position):

        self.set_properties(name)
        self.position = position
        self.world_position = position[:]

    # noinspection PyAttributeOutsideInit
    def set_properties(self, name):
        self.name = name
        self.properties = BlockTypes.BLOCKS[self.name]
        self.sprite = self.properties[SURFACE]
        self.destroyable = self.properties[DESTROYABLE]
        self.toughness = self.properties[TOUGHNESS] * 10
        self.sounds = self.properties[SOUNDS]
        self.block_type = self.properties[BLOCK_TYPE]
        self.rigid = self.block_type == RIGID
        self.fluid = self.block_type == FLUID
        self.liquid = self.fluid and self.name != AIR
        self.able_to_fall = self.block_type == FALLING
        self.solid = self.properties[SOLID]
        self.resistance = self.properties[RESISTANCE]
        self.transparent = self.properties[TRANSPARENT]
        self.light_emmision = self.properties[LIGHT_EMISSION]
        self.dropped_items = self.properties[DROPPED_ITEMS]

    @abstractmethod
    def change_block(self, name: str) -> None:
        """Changes to another block"""
        pass

    @abstractmethod
    def generate_body(self):
        """Generates a body"""
        pass

    def generate_falling_body(self):
        """Generates falling body"""
        pass

    @abstractmethod
    def delete_body(self):
        """Deletes a body"""
        pass

    @abstractmethod
    def get_sprites(self) -> list:
        """Returns a list of sprites"""
        pass

    @abstractmethod
    def check_point(self, point) -> bool:
        """Checks whether the point collides with the block"""
        pass

    @abstractmethod
    def update(self, x, y, chunk, column, mouse_pos):
        """Updates a block"""
        pass
