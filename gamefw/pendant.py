"""gamefw.pendant"""

from pygame import Rect
from pygame import Surface
# from typing import Literal

from typing_extensions import override

# Anchor = Literal['top-left', 'top-right', 'center', 'bottom-left', 'bottom-right']

class Pendant:
    def __init__(self):
        self.rect: Rect = Rect()
        # self.anchor: Anchor = 'top-left'
        self._cache: Surface | None = None

    def add_subpendant(self, pendant: 'Pendant') -> None:
        raise NotImplementedError()

    def render_only(self) -> Surface:
        """重新绘制Pendant并缓存"""
        self._cache = Surface(self.rect.size).convert_alpha()
        return self._cache

    def render(self, screen: Surface) -> Surface:
        if not self._cache:
            self._cache = self.render_only()
        screen.blit(self._cache, self.rect.topleft)
        return screen

class Widget(Pendant):
    def __init__(self):
        super().__init__()
        self.subnodes: list[Pendant] = list()

    @override
    def add_subpendant(self, pendant: Pendant) -> None:
        self.subnodes.append(pendant)

    @override
    def render_only(self) -> Surface:
        c = super().render_only()
        for n in self.subnodes:
            n.render(c)
        return c

class TextPendant(Pendant):
    def __init__(self):
        super().__init__()
        self.text: str = ''

    @override
    def render_only(self) -> Surface:
        c = super().render_only()
        # TODO: Load Font and Render Text.
        return c


