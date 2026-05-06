import pygame
import display
import text
from constants import *
from sprites import Sprites


class PlayerUI:

    def __init__(self, player):
        for file in Sprites.PLAYER:
            match file['name']:
                case 'player_ui_armor.png':
                    self.player_ui_armor = pygame.transform.scale(file['surface'], (16 * 8, 12 * 8))
                    self.armor_rect = self.player_ui_armor.get_rect(topleft=(display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_ARMOR))
                case 'player_ui_inventory.png':
                    self.player_ui_inventory = pygame.transform.scale(file['surface'], (16 * 8, 12 * 8))
                    self.inventory_rect = self.player_ui_inventory.get_rect(topleft=(display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_INVENTORY))
                case 'player_ui_stats.png':
                    self.player_ui_stats = pygame.transform.scale(file['surface'], (16 * 8, 12 * 8))
                    self.stats_rect = self.player_ui_stats.get_rect(topleft=(display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_STATS))
                case 'player_ui_tree.png':
                    self.player_ui_tree = pygame.transform.scale(file['surface'], (16 * 8, 12 * 8))
                    self.tree_rect = self.player_ui_tree.get_rect(topleft=(display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_TREE))
        self.player = player
        self.selected_ui = UI_STATS
        self.visible = False

    def draw(self):
        if self.visible:
            display.display.blit(self.player_ui_stats, (display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_STATS))
            display.display.blit(self.player_ui_tree, (display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_TREE))
            display.display.blit(self.player_ui_armor, (display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_ARMOR))
            display.display.blit(self.player_ui_inventory, (display.display.width / 2 - 92 * 4 - 128, display.display.height - 800 + 96 * UI_INVENTORY))
            self.player.inventory.visible = self.selected_ui == UI_INVENTORY
            self.player.player_stats.visible = self.selected_ui == UI_STATS

        self.player.inventory.draw()
        self.player.player_stats.draw()
        self.player.draw_player_health()

    def show(self, keys_pressed, keys_event, mouse_position, mouse_button_event, mouse_button_pressed):
        if keys_event == pygame.K_e:
            self.visible = not self.visible
            self.selected_ui = UI_STATS
        if not self.visible:
            self.player.inventory.visible = False
            self.player.player_stats.visible = False
        if self.armor_rect.collidepoint(mouse_position) and mouse_button_event[0]:
            self.selected_ui = UI_ARMOR
        if self.inventory_rect.collidepoint(mouse_position) and mouse_button_event[0]:
            self.selected_ui = UI_INVENTORY
        if self.stats_rect.collidepoint(mouse_position) and mouse_button_event[0]:
            self.selected_ui = UI_STATS
        if self.tree_rect.collidepoint(mouse_position) and mouse_button_event[0]:
            self.selected_ui = UI_TREE
