import pygame
import display


class TextBase:

    def __init__(self, position: tuple or list, size: int, color: tuple or list, text='', antialias=False):
        self.display = display.display
        self.position = position
        self.size = size
        self.color = color
        self.text = str(text)
        self.antialias = antialias
        self.font = pygame.font.Font('fonts/Press_Start_2P/PressStart2P-Regular.ttf', self.size)
        self._render_text()

    def change_text(self, *args: str, sep=' ') -> None:
        self.text = sep.join(args)
        self._render_text()

    def change_color(self, new_color: tuple[int, int, int] | list[int, int, int]) -> None:
        self.color = new_color
        self._render_text()

    def change_position(self, new_position: tuple | list) -> None:
        self.position = new_position

    def change_size(self, new_size: int) -> None:
        self.size = new_size
        self.font = pygame.font.Font('fonts/Press_Start_2P/PressStart2P-Regular.ttf', self.size)
        self._render_text()

    def _render_text(self) -> None:
        self.rendered_text = self.font.render(self.text, self.antialias, self.color)

    def draw(self, align="topleft"):
        rect = self.rendered_text.get_rect(**{align: self.position})
        self.display.blit(self.rendered_text, rect)


class Text(TextBase):
    pass


class TextAlpha(TextBase):

    def __init__(self, position: tuple or list, size: int, color: tuple or list, text='', antialias=False):
        self.alpha = 255
        super().__init__(position, size, color, text, antialias)

    def change_alpha(self, new_alpha: int) -> None:
        self.alpha = new_alpha
        self._render_text()

    def _render_text(self) -> None:
        self.rendered_text = self.font.render(self.text, self.antialias, self.color).convert_alpha()
        self.rendered_text.set_alpha(self.alpha)
