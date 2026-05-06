import light_engine
import block_logic
import block_renderer
import block_hitbox
from block_base import BlockBase


class Block(BlockBase):

    GAMEMODE = None
    world = None

    def __init__(self, name, position):
        super().__init__(name, position)
        self.light_cell = light_engine.LightCell(self)
        self.logic = block_logic.BlockLogic(self)
        self.renderer = block_renderer.BlockRenderer(self)
        self.hitbox = block_hitbox.BlockHitbox(self)

    def get_item(self) -> dict:
        return self.dropped_items

    def change_block(self, name: str) -> None:

        if self.name == name:
            return

        self.set_properties(name)
        self.logic.change_logic()
        self.hitbox.change_hitbox()
        self.light_cell.change_cell()

    def generate_body(self) -> None:
        self.hitbox.generate_body()

    def generate_falling_body(self) -> None:
        self.hitbox.generate_falling_body()

    def add_body_to_space(self) -> None:
        self.hitbox.add_body_to_space()

    def delete_body(self) -> None:
        self.hitbox.delete_body()

    def remove_body_from_space(self) -> None:
        self.hitbox.remove_body_from_space()

    def reset_position(self) -> None:
        self.position = self.world_position[:]

    def visible(self, player_position: tuple) -> bool:
        return block_logic.is_visible(self.position[0], self.position[1], player_position)

    def get_sprites(self) -> list:
        return self.renderer.get_sprites()

    def check_point(self, point: tuple[int, int]) -> bool:
        return self.hitbox.check_point(point)

    def update(self, x: int, y: int, chunk: list, column: list, mouse_position: tuple[int, int]) -> None:
        self.logic.update(x, y, chunk, column, mouse_position)
        self.light_cell.update(x, y, chunk)

    def update_logic(self, x: int, y: int, chunk: list, column: list, mouse_position: tuple[[int, int]]) -> None:
        self.logic.update(x, y, chunk, column, mouse_position)

    def update_light(self, x: int, y: int, chunk: list) -> None:
        self.light_cell.update(x, y, chunk)
