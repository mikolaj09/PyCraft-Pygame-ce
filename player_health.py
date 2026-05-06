import pygame
import display
import text
from constants import *
from sprites import Sprites


class PlayerHealth:

    def __init__(self, player):
        for file in Sprites.PLAYER:
            match file['name']:
                case 'health_bar.png':
                    self.health_bar_sprite = pygame.transform.scale(file['surface'], (13 * 10, 14 * 10))
        self.player = player
        self.gamemode = player.gamemode
        self.health_points = 0
        self.health_points_text = text.Text((display.display.width - (display.display.width // 2 - 92 * 4 - 30 - self.health_bar_sprite.get_width() / 2),
                                             display.display.height - 200 - 30 + self.health_bar_sprite.get_height() / 2 - 10),  24, (0, 0, 0), text=self.health_points)

        self.running = False
        self.falling_height = 0
        self.last_falling_height = 0

    @property
    def alive(self):
        return self.health_points > 0

    def set_health_points(self):
        self.health_points = self.player.player_stats.max_health

    def kill(self):
        self.health_points = 0

    def draw(self):
        if self.gamemode == SURVIVAL:
            display.display.blit(self.health_bar_sprite, (display.display.width - (display.display.width // 2 - 92 * 4 - 30), display.display.height - 200 - 30))
            self.health_points_text.draw(align='center')

    def falling_height_update(self):
        self.last_falling_height = self.falling_height
        if self.player.hitbox.body.velocity[1] > 0:
            self.falling_height += self.player.hitbox.body.velocity[1] / BLOCK_SIZE / FPS
        else:
            self.falling_height = 0

    def health_update(self):
        if round(self.falling_height) == 0 and self.last_falling_height > 3 and self.player.locate_player_in_fluid().name == 'air':
            self.health_points -= self.player.player_stats.damage_factor * FALL_DAMAGE_FACTOR * round(self.last_falling_height)
        if self.health_points < self.player.player_stats.max_health and self.alive:
            self.health_points += self.player.player_stats.regeneration / 60
        elif self.alive:
            self.health_points = self.player.player_stats.max_health
        self.health_points = round(self.health_points, 4)
        self.health_points_text.change_text(f'{int((self.health_points / self.player.player_stats.max_health) * 100)}%')

    def update(self):
        if self.gamemode == SURVIVAL:
            self.falling_height_update()
            self.health_update()
