import loader


class Sprites:

    UI = None
    BLOCKS = None
    ITEMS = None
    PLAYER = None
    ENTITIES = None

    LOADED = False

    @classmethod
    def load(cls, ui_sprites_loaded, blocks_sprites_loaded, items_sprites_loaded, player_sprites_loaded, entity_sprites_loaded):
        cls.UI = loader.check(ui_sprites_loaded)
        cls.BLOCKS = loader.check(blocks_sprites_loaded)
        cls.ITEMS = loader.check(items_sprites_loaded)
        cls.PLAYER = loader.check(player_sprites_loaded)
        cls.ENTITIES = loader.check(entity_sprites_loaded)
        cls.LOADED = True
