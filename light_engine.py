from functools import cache
from constants import *


MAX_LIGHT = 15
BLOCK_DECAY = 1
RANGE = 30


class LightCell:

    day_light = MAX_LIGHT

    def __init__(self, block, lightness=0):
        self.block = block
        self.lightness = lightness
        self.transparent = block.transparent
        self.light_emmision = block.light_emmision
        self.connected_to_sun = False

    @property
    def on_edge(self):
        return self.block.logic.on_edge

    def change_cell(self):
        self.transparent = self.block.transparent
        self.light_emmision = self.block.light_emmision

    def update(self, x, y, chunk):
        if not self.on_edge and not self.transparent:
            neighbours_brightness = max(get_neighbours_light(x, y, chunk))
            self.lightness = self.light_emmision if self.light_emmision > neighbours_brightness else neighbours_brightness
            return
        above = chunk[x][y - 1].light_cell if y > 0 else None
        if y == 0 or (above.connected_to_sun and above.transparent):
            sky_brightness = LightCell.day_light
            self.connected_to_sun = True
        else:
            sky_brightness = 0
            self.connected_to_sun = False

        neighbours_brightness = get_neighbours_light(x, y, chunk)

        self.lightness = max(sky_brightness, self.light_emmision, *neighbours_brightness)


@cache
def get_neighbours_x_y(x, y):
    neigbours = []
    if y > 0:
        neigbours.append((x, y - 1))
    if y < WORLD_HEIGHT - 1:
        neigbours.append((x, y + 1))
    if x > 0:
        neigbours.append((x - 1, y))
    if x < CHUNK_SIZE - 1:
        neigbours.append((x + 1, y))
    return neigbours


def get_neighbours_light(x, y, chunk):
    result = []
    for x2, y2 in get_neighbours_x_y(x, y):
        cell = chunk[x2][y2].light_cell
        result.append(cell.lightness - BLOCK_DECAY if cell.transparent and cell.lightness - BLOCK_DECAY > cell.light_emmision else cell.light_emmision)
    return result

