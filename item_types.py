import json
import os
from constants import *


class ItemTypes:

    ITEMS = {}

    @classmethod
    def load_from_json(cls):
        with open("items.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for name, props in data.items():
            cls.ITEMS[name] = {
                SURFACE: None,
                TOUGHNESS: props.get(TOUGHNESS, 0),
                SOUNDS: props.get(SOUNDS, None),
                ITEM_TYPE: globals().get(props.get(ITEM_TYPE, BLOCK), BLOCK)
            }

        cls.ITEMS[ITEM_NONE] = cls.ITEMS.pop('none')

    @classmethod
    def load(cls, sprites):
        for i in sprites:
            name = os.path.splitext(i[NAME])[0]
            if name in cls.ITEMS:
                cls.ITEMS[name][SURFACE] = i[SURFACE]
