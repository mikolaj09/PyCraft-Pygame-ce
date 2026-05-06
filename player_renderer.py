import pygame
import display
from sprites import *
from constants import *


class PlayerRenderer:

    def __init__(self, player):

        for file in Sprites.PLAYER:
            match file['name']:
                case 'player_front.png':
                    self.player_front_sprite = pygame.transform.scale(file['surface'], (PLAYER_WIDTH * BLOCK_SIZE // DEFAULT_BLOCK_SIZE,
                                                                                          PLAYER_HEIGHT * BLOCK_SIZE // DEFAULT_BLOCK_SIZE))
                case 'player_walking1.png':
                    self.player_walking1_sprite = pygame.transform.scale(file['surface'], (PLAYER_WIDTH * BLOCK_SIZE // DEFAULT_BLOCK_SIZE,
                                                                                          PLAYER_HEIGHT * BLOCK_SIZE // DEFAULT_BLOCK_SIZE))
                case 'player_walking2.png':
                    self.player_walking2_sprite = pygame.transform.scale(file['surface'], (PLAYER_WIDTH * BLOCK_SIZE // DEFAULT_BLOCK_SIZE,
                                                                                          PLAYER_HEIGHT * BLOCK_SIZE // DEFAULT_BLOCK_SIZE))
                case 'player_jumping.png':
                    self.player_jumping_sprite = pygame.transform.scale(file['surface'], (PLAYER_WIDTH * BLOCK_SIZE // DEFAULT_BLOCK_SIZE,
                                                                                          PLAYER_HEIGHT * BLOCK_SIZE // DEFAULT_BLOCK_SIZE))
        self.player_current_sprite = self.player_front_sprite
        self.player = player
        self.player_rect = self.player_current_sprite.get_rect(center=(display.display.width // 2, display.display.height // 2))
        self.gamemode = self.player.gamemode

    def update(self, keys1, keys2, mouse_position, mouse_button, mouse_button2):
        if self.player.alive:
            if self.player.hitbox.jumping:
                self.player_current_sprite = self.player_jumping_sprite
            elif self.player.hitbox.moving:
                if self.player.hitbox.direction == RIGHT:
                    self.player_current_sprite = self.player_walking1_sprite
                elif self.player.hitbox.direction == LEFT:
                    self.player_current_sprite = pygame.transform.flip(self.player_walking1_sprite, True, False)
            elif not self.player.hitbox.moving:
                self.player_current_sprite = self.player_front_sprite

    def draw(self):
        if self.player.alive:
            display.display.blit(self.player_current_sprite, self.player_rect.topleft)
