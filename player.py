import pygame
import world
import player_ui
import player_hitbox
import player_renderer
import inventory
import player_stats
import player_health
import display
from constants import *


class Player:

    def __init__(self, gamemode):
        self.total_offset = None
        self.gamemode = gamemode
        self.player_ui = player_ui.PlayerUI(self)
        self.hitbox = player_hitbox.PlayerHitBox(self)
        self.renderer = player_renderer.PlayerRenderer(self)
        self.inventory = inventory.Inventory(self)
        self.player_stats = player_stats.PlayerStats(self)
        self.player_health = player_health.PlayerHealth(self)
        self.hitbox.generate_new_body()

    @property
    def alive(self):
        return self.player_health.alive

    def kill(self):
        self.player_health.kill()
        self.hitbox.delete_body_from_space()

    def spawn(self):
        if not self.alive:
            self.player_health.set_health_points()
            self.total_offset = [0, 0]
            self.hitbox.add_body_to_space()
            if world.world_instance.world_type == 'FLAT':
                self.hitbox.body.position = (display.display.width // 2, display.display.height // 2 + 3100)

    def summon_entity(self, position):
        world.world_instance.summon_entity(position, self.total_offset)

    def locate_player_in_fluid(self, offset=None):
        offset = (0, 0) if offset is None else offset
        return world.world_instance.get_block_chunk([self.renderer.player_rect.center[0] + offset[0], self.renderer.player_rect.center[1] + offset[1]], self.total_offset)

    def give_item(self, item_name, amount):
        self.inventory.add_item(item_name, amount)

    def build(self, mouse_pos, mouse_button1):
        if mouse_button1[2] and self.inventory.equipment[self.inventory.selected_slot] is not None and \
                len(world.world_instance.chunk[0]) > (mouse_pos[1] + self.total_offset[1]) // BLOCK_SIZE >= 0 and not self.inventory.visible:
            if self.inventory.equipment[self.inventory.selected_slot].amount > 0:
                block = world.world_instance.get_block_chunk(mouse_pos, self.total_offset)
                if not block.solid and block.visible(self.renderer.player_rect.center):
                    block.change_block(self.inventory.equipment[self.inventory.selected_slot].name)
                    if self.gamemode == SURVIVAL:
                        self.inventory.remove_item(self.inventory.selected_slot)

    def dig(self, mouse_pos, mouse_button2):
        block = world.world_instance.get_block_chunk(mouse_pos, self.total_offset)
        if block.destroyable and block.visible(self.renderer.player_rect.center) and block.logic.on_edge and not self.inventory.visible:
            if mouse_button2[0]:
                block.logic.digging_stage += 1
                block.logic.dug = True
            else:
                block.logic.dug = False
                block.logic.digging_stage = 0
            if block.logic.digging_stage >= block.toughness or (self.gamemode == CREATIVE and block.logic.dug):
                if self.gamemode == SURVIVAL:
                    for item_name, amount in block.get_item().items():
                        self.inventory.add_item(item_name, amount=amount)
                block.change_block(AIR)
                block.digging_stage = 0
                block.logic.dug = False

    def update(self, keys_pressed, keys_event, mouse_position, mouse_button_event, mouse_button_pressed):

        if self.alive:

            self.player_stats.update(keys_pressed, keys_event, mouse_position, mouse_button_event, mouse_button_pressed)

            if keys_event == pygame.K_f:
                self.summon_entity((display.display.width // 2, display.display.height // 2))

            if self.gamemode != SPECTATOR:
                self.dig(mouse_position, mouse_button_pressed)
                self.build(mouse_position, mouse_button_event)

            self.player_ui.show(keys_pressed, keys_event, mouse_position, mouse_button_event, mouse_button_pressed)

            self.hitbox.update(keys_pressed, keys_event)
            self.renderer.update(keys_pressed, keys_event, mouse_position, mouse_button_event, mouse_button_pressed)
            self.inventory.move_item(mouse_button_pressed, mouse_position)
            self.inventory.select_slot(keys_event)

            self.total_offset = [round(self.hitbox.body.position[0] - (display.display.width // 2)),
                                 round(self.hitbox.body.position[1] - (display.display.height // 2))]

            self.player_health.update()

    def draw(self):
        self.renderer.draw()

    def draw_player_health(self):
        self.player_health.draw()
