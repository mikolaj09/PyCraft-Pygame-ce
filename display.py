import pygame
import pyautogui
from tools import Singleton


class Display(metaclass=Singleton):

    def __init__(self):

        self.screen = None
        self.width, self.height = pyautogui.size()
        self.size = (self.width, self.height)
        self.set_screen()
        self.color = (0, 0, 0)
        self.sprites = []

    def set_screen_color(self, color: tuple[int, int, int]):
        self.color = color

    def set_screen(self):
        if pygame.display.get_init():
            self.screen = pygame.display.set_mode(self.size, flags=pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            raise ValueError('display not initialized')

    def add_sprites(self, sprites):
        self.sprites.extend(sprites)

    def blit(self, *args, **kwargs):
        self.screen.blit(*args, **kwargs)

    def draw(self, player, world):
        self.screen.fill((26, 163, 255))
        world.draw(player.renderer.player_rect.center, player.total_offset)
        player.draw()
        self.screen.fblits(self.sprites)
        self.sprites.clear()
        player.player_ui.draw()

    def fill(self, color: tuple[int, int, int]):
        self.screen.fill(color)


display = None
