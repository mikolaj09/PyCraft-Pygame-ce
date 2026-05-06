import pygame
import item
import display
from constants import ITEM_SIZE, MAXIMUM_NUMBER_OF_ITEMS_IN_SLOT
from sprites import *


class Inventory:

    def __init__(self, player):
        self.visible = False
        self.player = player
        self.game_mode = self.player.gamemode

        self.equipment = [item.Item(None, 0,
                                    position=[int(display.display.width / 2 - 92 * 4 + 16 + i * 80), display.display.height - 200 + 16]) for i in range(9)] + \
                         [item.Item(None, 0, position=[int(display.display.width / 2 - 92 * 4 + 16 + 80 * (i % 9)),
                                                       display.display.height - 800 + 16 + 96 * (i // 9)]) for i in range(36)]

        self.selected_slot = 0

        self.blocks_sprites = Sprites.BLOCKS
        self.player_sprites = Sprites.PLAYER

        for file in self.player_sprites:
            if file['name'] == 'usable_equipment.png':
                self.us_eq_sprite = pygame.transform.scale(file['surface'], (92 * 8, 12 * 8))
            elif file['name'] == 'equipment.png':
                self.eq_sprite = pygame.transform.scale(file['surface'], (92 * 8, 48 * 8))

        self.picked_item = None

    def select_slot(self, key):
        if pygame.key.name(key).isdigit() and pygame.key.name(key) != '' and pygame.key.name(key) != '0':
            self.selected_slot = int(pygame.key.name(key)) - 1

    def find_available_slot(self, name):
        for item1 in self.equipment:
            if item1.name == name and item1.amount < MAXIMUM_NUMBER_OF_ITEMS_IN_SLOT:
                return self.equipment.index(item1)
        return None

    def check_item(self, name):
        return True if self.find_available_slot(name) is not None else False

    def add_item(self, item_name, amount=1):

        while amount > 0:
            slot = self.find_available_slot(item_name)
            if slot is not None and self.equipment[slot].amount < MAXIMUM_NUMBER_OF_ITEMS_IN_SLOT:
                self.equipment[slot].add_items(1)
            else:
                empty_slot = self.find_available_slot(None)
                if empty_slot is not None:
                    self.equipment[empty_slot].change_item(name=item_name, amount=1)

            amount -= 1

    def remove_item(self, slot, amount=1):
        while amount > 0:
            self.equipment[slot].remove_items(1)
            if self.equipment[slot].amount == 0:
                self.equipment[slot].change_item(name=None, amount=0)
            amount -= 1

    def move_item(self, mouse_buttons, mouse_position):
        if self.visible and mouse_buttons[0] and self.picked_item is None:
            for player_item in self.equipment:
                if player_item.name is not None and player_item.check_point(mouse_position):
                    self.picked_item = player_item
                    self.picked_item.picked = True
                    break
        if self.visible and mouse_buttons[0] and self.picked_item is not None:
            self.picked_item.position = (mouse_position[0] - ITEM_SIZE // 2, mouse_position[1] - ITEM_SIZE // 2)
            self.picked_item.amount_text.position = (self.picked_item.position[0], self.picked_item.position[1] + ITEM_SIZE)
        if self.visible and not mouse_buttons[0] and self.picked_item is not None:
            for player_item in self.equipment:
                if (player_item.position_in_eq[0] - self.picked_item.position[0]) ** 20 + \
                        (player_item.position_in_eq[1] - self.picked_item.position[1]) ** 20 <= ITEM_SIZE ** 20 and \
                        (player_item.name is None or player_item.name == self.picked_item.name and player_item.amount
                         + self.picked_item.amount <= MAXIMUM_NUMBER_OF_ITEMS_IN_SLOT):
                    player_item.change_item(self.picked_item.name, self.picked_item.amount + player_item.amount)
                    self.picked_item.change_item(None, 0)
                    self.picked_item.position = self.picked_item.position_in_eq
                    break
            else:
                self.picked_item.drop_item(self.picked_item.position)
            self.picked_item.picked = False
            self.picked_item = None

    def draw(self):

        if self.visible:
            display.display.blit(self.eq_sprite, (display.display.width / 2 - 92 * 4, display.display.height - 800))
            for item1 in self.equipment[9:]:
                item1.draw()

        if self.game_mode != 'SPECTATOR':
            display.display.blit(self.us_eq_sprite, (display.display.width / 2 - 92 * 4, display.display.height - 200))
            for item1 in self.equipment[:9]:
                item1.draw()
                if self.selected_slot == self.equipment.index(item1) and item1.in_eq:
                    item1.draw_name()
