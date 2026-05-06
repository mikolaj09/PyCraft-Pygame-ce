import pygame
import threading
import configparser
from pathlib import Path
from constants import *


def load_settings(filename):
    config = configparser.ConfigParser()

    try:
        config.read(filename)
        return {
            VOLUME: int(config[SETTINGS].get(VOLUME, '50')),
            LANGUAGE: config[SETTINGS].get(LANGUAGE, ENGLISH),
        }
    except FileNotFoundError:
        return {VOLUME: 50, LANGUAGE: ENGLISH}


def load_graphics(sprites_loaded, folder, scale):
    graphics = Path(__file__).parent / folder
    sprites = []

    for image in graphics.iterdir():
        if image.is_file():
            surface = pygame.image.load(f'{folder}/{image.name}').convert_alpha()
            if scale != 1:
                size = surface.get_size()
                surface = pygame.transform.scale(surface, (size[0] * scale, size[1] * scale))
            sprite = {
                SURFACE: surface,
                NAME: image.name
            }
            print(f'loaded {sprite}')
            sprites.append(sprite)

    sprites_loaded.put(sprites)
    return sprites_loaded


def start_loading(sprites_loaded, folder, scale=1):
    graphics_thread = threading.Thread(target=load_graphics, args=(sprites_loaded, folder, scale), daemon=True)
    return graphics_thread


def check(sprites_loaded):
    if not sprites_loaded.empty():
        sprites = sprites_loaded.get()
    else:
        sprites = None
        print('Error occurred!')
        exit(-1)
    return sprites
