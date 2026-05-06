import pygame
import display
import text
from functools import cache
from constants import *
from sprites import *


class PlayerStats:

    def __init__(self, player):
        self.player = player
        self.max_health = PLAYER_MAX_LIFE
        self.regeneration = PLAYER_REGENERATION
        self.defense = PLAYER_DEFENSE
        self.damage = PLAYER_DAMAGE
        self.experience = 0
        self._used_upgrade_points = 0
        self.visible = False

        for file in Sprites.PLAYER:
            match file['name']:
                case 'player_stats.png':
                    self.player_stats_sprite = pygame.transform.scale(file['surface'], (92 * 8, 48 * 8))
                case 'upgrade_button.png':
                    self.upgrade_button_sprite = pygame.transform.scale(file['surface'], (16 * 2, 16 * 2))

        self.upgrade_button_rect1 = self.upgrade_button_sprite.get_rect(topleft=(display.display.width / 2 - 92 * 4 + 10 + 400 + 100, display.display.height - 800 + 10 + 96))
        self.upgrade_button_rect2 = self.upgrade_button_sprite.get_rect(topleft=(display.display.width / 2 - 92 * 4 + 10 + 400 + 100, display.display.height - 800 + 10 + 144))
        self.upgrade_button_rect3 = self.upgrade_button_sprite.get_rect(topleft=(display.display.width / 2 - 92 * 4 + 10 + 400 + 100, display.display.height - 800 + 10 + 192))
        self.upgrade_button_rect4 = self.upgrade_button_sprite.get_rect(topleft=(display.display.width / 2 - 92 * 4 + 10 + 400 + 100, display.display.height - 800 + 10 + 240))

        self.level_text = text.Text((display.display.width / 2, display.display.height - 200 - 70), 48, (255, 255, 255), text=self.level)
        self.upgrade_points_text = text.Text((display.display.width / 2 - 92 * 4 + 10, display.display.height - 800 + 10), 24, (0, 0, 0), text='upgrade points:')
        self.experience_text = text.Text((display.display.width / 2 - 92 * 4 + 10, display.display.height - 800 + 10 + 48), 24, (0, 0, 0), text='experience:')
        self.max_health_text = text.Text((display.display.width / 2 - 92 * 4 + 10, display.display.height - 800 + 10 + 96), 24, (0, 0, 0), text='max health:')
        self.regeneration_text = text.Text((display.display.width / 2 - 92 * 4 + 10, display.display.height - 800 + 10 + 144), 24, (0, 0, 0), text='regeneration:')
        self.damage_text = text.Text((display.display.width / 2 - 92 * 4 + 10, display.display.height - 800 + 10 + 192), 24, (0, 0, 0), text='damage:')
        self.defense_text = text.Text((display.display.width / 2 - 92 * 4 + 10, display.display.height - 800 + 10 + 240), 24, (0, 0, 0), text='defense:')

        self.upgrade_points_value_text = text.Text((display.display.width / 2 - 92 * 4 + 10 + 400, display.display.height - 800 + 10), 24, (0, 0, 0), text=self.upgrade_points)
        self.experience_value_text = text.Text((display.display.width / 2 - 92 * 4 + 10 + 400, display.display.height - 800 + 10 + 48), 24, (0, 0, 0), text=self.experience)
        self.max_health_value_text = text.Text((display.display.width / 2 - 92 * 4 + 10 + 400, display.display.height - 800 + 10 + 96), 24, (0, 0, 0), text=self.max_health)
        self.regeneration_value_text = text.Text((display.display.width / 2 - 92 * 4 + 10 + 400, display.display.height - 800 + 10 + 144), 24, (0, 0, 0), text=self.regeneration)
        self.damage_value_text = text.Text((display.display.width / 2 - 92 * 4 + 10 + 400, display.display.height - 800 + 10 + 192), 24, (0, 0, 0), text=self.damage)
        self.defense_value_text = text.Text((display.display.width / 2 - 92 * 4 + 10 + 400, display.display.height - 800 + 10 + 240), 24, (0, 0, 0), text=self.defense)

    @property
    def damage_factor(self):
        return 1 - self.defense * 0.009

    @property
    def upgrade_points(self):
        return self.level - self._used_upgrade_points

    @upgrade_points.setter
    def upgrade_points(self, value):
        self._used_upgrade_points = self.level - value

    @property
    def level(self):
        return level(self.experience)

    @level.setter
    def level(self, value):
        exp = 0
        for lvl in range(1, value + 1):
            exp += 2 * lvl ** 2

        self.experience = exp

    def update(self, keys_pressed, keys_event, mouse_position, mouse_button_event, mouse_button_pressed):
        if self.upgrade_points > 0:
            if self.upgrade_button_rect1.collidepoint(mouse_position) and mouse_button_event[0]:
                self.max_health += PLAYER_MAX_LIFE_UPGRADE
                self.max_health = round(self.max_health, 3)
                self.upgrade_points -= 1
            if self.upgrade_button_rect2.collidepoint(mouse_position) and mouse_button_event[0]:
                self.regeneration += PLAYER_REGENERATION_UPGRADE
                self.regeneration = round(self.regeneration, 3)
                self.upgrade_points -= 1
            if self.upgrade_button_rect3.collidepoint(mouse_position) and mouse_button_event[0]:
                self.damage += PLAYER_DAMAGE_UPGRADE
                self.damage = round(self.damage, 3)
                self.upgrade_points -= 1
            if self.upgrade_button_rect4.collidepoint(mouse_position) and mouse_button_event[0]:
                self.defense += PLAYER_DEFENSE_UPGRADE
                self.defense = round(self.defense, 3)
                self.upgrade_points -= 1

        self.level_text.change_text(str(self.level))
        self.upgrade_points_value_text.change_text(str(self.upgrade_points))
        self.experience_value_text.change_text(str(self.experience))
        self.max_health_value_text.change_text(str(self.max_health))
        self.regeneration_value_text.change_text(str(self.regeneration))
        self.damage_value_text.change_text(str(self.damage))
        self.defense_value_text.change_text(str(self.defense))

    def draw(self):
        if self.visible:
            display.display.blit(self.player_stats_sprite, (display.display.width / 2 - 92 * 4, display.display.height - 800))
            for i in range(4):
                display.display.blit(self.upgrade_button_sprite, (display.display.width / 2 - 92 * 4 + 10 + 400 + 100, display.display.height - 800 + 10 + 96 + 48 * i))
            self.upgrade_points_text.draw()
            self.experience_text.draw()
            self.max_health_text.draw()
            self.regeneration_text.draw()
            self.damage_text.draw()
            self.defense_text.draw()
            self.upgrade_points_value_text.draw()
            self.experience_value_text.draw()
            self.max_health_value_text.draw()
            self.regeneration_value_text.draw()
            self.damage_value_text.draw()
            self.defense_value_text.draw()

        self.level_text.draw(align='center')


@cache
def level(experience):
    lvl = 0
    while experience >= 2 * (lvl + 1) ** 2:
        lvl += 1
        experience -= 2 * lvl ** 2
    return lvl
