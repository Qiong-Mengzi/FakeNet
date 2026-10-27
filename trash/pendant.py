"""gamefw.pendant"""

import pygame as pyg
from pygame import Rect
from pygame import Surface
from typing import Literal

from typing_extensions import override

Anchor = Literal["top-left", "top-right", "center", "bottom-left", "bottom-right"]

_ANCHOR_RATIO: dict[Anchor, tuple[float, float]] = {
    "top-left":     (0.0, 0.0),
    "top-right":    (1.0, 0.0),
    "center":       (0.5, 0.5),
    "bottom-left":  (0.0, 1.0),
    "bottom-right": (1.0, 1.0),
}

def apply_anchor(anchor: Anchor, o: Rect, dst: Rect) -> Rect:
    rx, ry = _ANCHOR_RATIO[anchor]
    return Rect(
        int((dst.w - o.w) * rx) + o.x,
        int((dst.h - o.h) * ry) + o.y,
        o.w, o.h,
    )

class Pendant:
    def __init__(self):
        self.rect: Rect = Rect()
        self.anchor: Anchor = "top-left"
        self._cache: Surface | None = None
        self.parent: Pendant | None = None

    def add_subpendant(self, pendant: "Pendant") -> None:
        raise NotImplementedError()

    def render_only(self) -> Surface:
        """重新绘制Pendant并缓存"""
        self._cache = Surface(self.rect.size, pyg.SRCALPHA)
        return self._cache

    def render(self, screen: Surface) -> Surface:
        if self._cache is None:
            self._cache = self.render_only()
        screen.blit(self._cache, apply_anchor(self.anchor, self.rect, screen.get_rect()))
        return screen

    def mark_dirty(self):
        self._cache = None
        if self.parent is not None:
            self.parent.mark_dirty()


class Widget(Pendant):
    def __init__(self):
        super().__init__()
        self.subnodes: list[Pendant] = list()

    @override
    def add_subpendant(self, pendant: Pendant) -> None:
        self.subnodes.append(pendant)
        pendant.parent = self

    @override
    def render_only(self) -> Surface:
        c = super().render_only()
        for n in self.subnodes:
            n.render(c)
        return c


class PendantManager:
    def __init__(self, screen: Surface):
        self.screen = screen
        w = Widget()
        w.rect = screen.get_rect()
        self.root_pendant: Pendant = w
        self.tags: dict[str, Pendant] = dict()

    def add_pendant(self, pendant: Pendant, tag: str | None = None):
        self.add_pendant(pendant)

        if tag is None:
            return
        if tag in self.tags:
            raise Exception
        self.tags[tag] = pendant

    # def render
