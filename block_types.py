import pygame
import json
import os
import light_engine
from constants import *


class BlockTypes:

    sprite_not_visible1 = None
    sprite_not_visible2 = None

    damaged_sprites = []
    brightness_effect = []
    number_of_shades = light_engine.MAX_LIGHT

    BLOCKS = {}

    @classmethod
    def load_from_json(cls):
        with open('blocks.json', "r", encoding="utf-8") as file:
            data = json.load(file)

        for name, props in data.items():
            cls.BLOCKS[name] = {
                SURFACE: None,
                DESTROYABLE: props[DESTROYABLE],
                TOUGHNESS: props[TOUGHNESS],
                SOUNDS: None,
                FRICTION: props[FRICTION],
                ELASTICITY: props[ELASTICITY],
                BLOCK_TYPE: globals().get(props[BLOCK_TYPE], RIGID),
                SOLID: props[SOLID],
                RESISTANCE: float('inf') if props[RESISTANCE] == "inf" else props[RESISTANCE],
                TRANSPARENT: props[TRANSPARENT],
                LIGHT_EMISSION: props[LIGHT_EMISSION],
                DROPPED_ITEMS: (lambda d: {NONE_TYPE: 0} if "none" in d else d)(props.get(DROPPED_ITEMS, {}))
            }

    @classmethod
    def load(cls, sprites):

        cls.brightness_effect.clear()
        cls.damaged_sprites.clear()

        surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        for i in range(cls.number_of_shades + 1):
            surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            surf.fill((0, 0, 0, int(255 * (1 - i / cls.number_of_shades))))
            surf = surf.convert_alpha()
            cls.brightness_effect.append(surf)

        cls.BLOCKS[AIR][SURFACE] = surface

        for i in sprites:
            name = os.path.splitext(i[NAME])[0]
            if name == 'not_visible':
                cls.sprite_not_visible1 = i[SURFACE]
            elif name == 'not_visible2':
                cls.sprite_not_visible2 = i[SURFACE]
            elif 'damaged' in name:
                cls.damaged_sprites.append(i[SURFACE])
            elif name in cls.BLOCKS:
                cls.BLOCKS[name][SURFACE] = i[SURFACE]
