from constant import Constant as Const


"""
A module containing constants that are to remain unchanged.
NOTE: Don't even think about changing them without proper knowledge.
"""

# some information about engine
APPLICATION_NAME = 'PyCave'
VERSION = '0.8.4'


# some important stuff
SURFACE = 'surface'
SOUNDS = 'sounds'
NAME = 'name'
VOLUME = 'volume'
LANGUAGE = 'language'
ENGLISH = 'ENGLISH'
POLISH = 'POLISH'
SETTINGS = 'SETTINGS'
WORLD_TYPE = 'world type'
DIFFICULTY = 'difficulty'
GENERATE_STRUCTURES = 'generate structures'
GAME_MODE = 'game mode'
FPS = 60
SURVIVAL = 'SURVIVAL'
CREATIVE = 'CREATIVE'
SPECTATOR = 'SPECTATOR'
HEALTH = 'health'
SPEED = 'speed'

# world
FALL_DAMAGE_FACTOR = 0.5
CHUNK_SIZE = 75
WORLD_HEIGHT = 100
ORIGINAL_WORLD_SIZE = 275
NEW_WORLD = 0
RESTART_WORLD = 1
OLD_WORLD = 2

# player
PLAYER_MAX_LIFE = 20
PLAYER_REGENERATION = 0.2
PLAYER_DEFENSE = 0
PLAYER_DAMAGE = 1
PLAYER_MAX_LIFE_UPGRADE = 0.25
PLAYER_REGENERATION_UPGRADE = 0.1
PLAYER_DAMAGE_UPGRADE = 0.1
PLAYER_DEFENSE_UPGRADE = 1
PLAYER_HEIGHT = 90
PLAYER_WIDTH = 30
PLAYER_SPEED = 300
PLAYER_RUNNING_SPEED = 400
PLAYER_MOVEMENT_FORCE = 200000
PLAYER_RUNNING_MOVEMENT_FORCE = 300000
PLAYER_JUMP_FORCE = 66000
PLAYER_RUNNING_JUMP_FORCE = 80000
PLAYER_SWIMMING_FORCE = 400000
PLAYER_RUNNING_SWIMMING_FORCE = 500000

# player UI
UI_ARMOR = 2
UI_INVENTORY = 3
UI_STATS = 0
UI_TREE = 1

# blocks
AIR = 'air'
DIRT = 'dirt'
STONE = 'stone'
DARKSTONE = 'darkstone'
SAND = 'sand'
WATER = 'water'
LAVA = 'lava'
BEDROCK = 'bedrock'
GRASS = 'grass'
SNOWY_GRASS = 'snowy grass'
SNOW = 'snow'
GLOWSTONE = 'glowstone'
SHORT_GRASS = 'short grass'
BLOCK_SIZE = 50
DEFAULT_BLOCK_SIZE = 50

# items
ITEM_NONE = None
ITEM_DIRT = 'dirt'
ITEM_STONE = 'stone'
ITEM_DARKSTONE = 'darkstone'
ITEM_SAND = 'sand'
ITEM_BEDROCK = 'bedrock'
ITEM_GRASS = 'grass'
ITEM_SNOWY_GRASS = 'snowy grass'
ITEM_SNOW = 'snow'
ITEM_GLOWSTONE = 'glowstone'
ITEM_SIZE = 64
MAXIMUM_NUMBER_OF_ITEMS_IN_SLOT = 64

# block and items.json attributes
SOLID = 'solid'
TOUGHNESS = 'toughness'
DESTROYABLE = 'destroyable'
FRICTION = 'friction'
ELASTICITY = 'elasticity'
RESISTANCE = 'resistance'
TRANSPARENT = 'transparent'
LIGHT_EMISSION = 'light emission'
DROPPED_ITEMS = 'dropped items'

# block types
BLOCK_TYPE = 'type'
RIGID = 11
FALLING = 12
FLUID = 13

# item types
ITEM_TYPE = 'item_type'
NONE_TYPE = 16
BLOCK = 17
TOOL = 18
WEAPON = 19
ARMOR = 20

# world types
FLAT = 'FLAT'
NORMAL = 'NORMAL'

# biome properties
FLATNESS = 'flatness'
LAYERS = 'layers'
MAX_DELTA = 'max delta'

# biome types
PLAINS = 'PLAINS'
MOUNTAINS = 'MOUNTAINS'
DESERT = 'DESERT'
ICE_PLAINS = 'ICE PLAINS'
OCEAN = 'OCEAN'

# entities
PLAYER = 'player'
ZOMBIE = 'zombie'
PIG = 'pig'

# directions
RIGHT = 'RIGHT'
LEFT = 'LEFT'
UP = 'UP'
DOWN = 'DOWN'
