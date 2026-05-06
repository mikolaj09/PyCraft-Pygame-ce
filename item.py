import pymunk
import display
import text
from item_types import ItemTypes
from constants import *


class Item:

    def __init__(self, name, amount, position=None):
        self.name = name
        self.properties = ItemTypes.ITEMS[self.name]
        self.sprite = self.properties[SURFACE]
        self.toughness = self.properties[TOUGHNESS]
        self.sounds = self.properties[SOUNDS]
        self.item_type = self.properties[ITEM_TYPE]
        self.amount = amount
        self.position = position
        self.position_in_eq = position
        self.dropped = False
        self.picked = False

        if self.position is not None:
            self.amount_text = text.Text((self.position[0], self.position[1] + ITEM_SIZE), 16, (255, 255, 255), text=self.amount)

    @property
    def visible(self):
        return self.name is not None and self.sprite is not None

    @property
    def in_eq(self):
        return not self.dropped and not self.picked

    def add_items(self, amount=1):
        self.amount = self.amount + amount if self.amount + amount <= MAXIMUM_NUMBER_OF_ITEMS_IN_SLOT else MAXIMUM_NUMBER_OF_ITEMS_IN_SLOT
        self.amount_text = text.Text((self.position[0], self.position[1] + ITEM_SIZE), 16, (255, 255, 255), text=self.amount)

    def remove_items(self, amount=1):
        self.amount = self.amount - amount if amount <= self.amount else 0
        self.amount_text = text.Text((self.position[0], self.position[1] + ITEM_SIZE), 16, (255, 255, 255), text=self.amount)

    def set_amount(self, amount: int):
        self.amount = amount
        self.amount_text = text.Text((self.position[0], self.position[1] + ITEM_SIZE), 16, (255, 255, 255), text=self.amount)

    def change_item(self, name, amount):
        self.name = name
        self.properties = ItemTypes.ITEMS[self.name]
        self.sprite = self.properties[SURFACE]
        self.toughness = self.properties[TOUGHNESS]
        self.sounds = self.properties[SOUNDS]
        self.item_type = self.properties[ITEM_TYPE]
        self.amount = amount
        self.amount_text = text.Text((self.position[0], self.position[1] + ITEM_SIZE), 16, (255, 255, 255), text=self.amount)

    def check_point(self, point):
        rect = self.sprite.get_rect(topleft=self.position)
        return rect.collidepoint(point)

    def drop_item(self, position):
        self.change_item(None, 0)
        self.position = self.position_in_eq

    def draw(self):
        if self.visible:
            display.display.blit(self.sprite, self.position)
            self.amount_text.draw('bottomleft')

    def draw_name(self):
        if self.visible and not self.picked and not self.dropped:
            name = text.Text((self.position[0] + self.sprite.get_width() / 2, self.position[1] - 30), 16, (255, 255, 255), text=self.name)
            name.draw(align='center')

    def __repr__(self):
        return f'{self.name} {self.amount}'
