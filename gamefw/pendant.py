"""
gamefw.pendant
"""

from typing import Self
from typing import Literal

import pygame as pyg
from pygame import Surface
from pygame import Rect

Anchor = Literal["left-top", "right-top", "center", "left-bottom", "right-bottom"]

_ANCHOR_OFFSET: dict[Anchor, tuple[float, float]] = {
    "left-top": (0.0, 0.0),
    "center": (0.5, 0.5),
    "left-bottom": (0.0, 1.0),
    "right-top": (1.0, 0.0),
    "right-bottom": (1.0, 1.0),
}


def apply_anchor(anchor: Anchor, pendant_rect: Rect, widget_rect: Rect) -> Rect:
    x = pendant_rect.x
    y = pendant_rect.y
    dx, dy = _ANCHOR_OFFSET[anchor]
    cw = widget_rect.w
    ch = widget_rect.h
    return Rect(int(cw * dx + x), int(ch * dy + y), pendant_rect.w, pendant_rect.h)


class Pendant:
    def render(self, cloth: Surface) -> Surface:
        return cloth


class Widget:
    def __init__(
        self, name: str, anchor: Anchor, rect: Rect, show: bool = True, z: int = -1
    ) -> None:
        self.name = name
        self.anchor = anchor
        self.rect = rect
        self.show = show
        self.z = z
        self.pendant_map: dict[str, int] = dict()
        self.pendants: list[Pendant] = list()

        self._pendant_namecount: int = 0

    def _gen_pendant_name(self) -> str:
        self._pendant_namecount += 1
        return f"pendant-{self._pendant_namecount}"

    def add_pendant(self, pendant: Pendant, name: str | None = None) -> Self:
        if name is None:
            name = self._gen_pendant_name()
        if name in self.pendant_map:
            raise Exception

        idx: int = len(self.pendants)
        self.pendant_map[name] = idx
        self.pendants.append(pendant)
        return self

    def set_pendant(self, name: str, pendant: Pendant) -> None:
        if name not in self.pendant_map:
            raise Exception

        self.pendants[self.pendant_map[name]] = pendant

    def query_pendant(self, name: str) -> Pendant | None:
        if name not in self.pendant_map:
            return None
        return self.pendants[self.pendant_map[name]]

    def render(self, cloth: Surface) -> Surface:
        widget_cloth: Surface = Surface(self.rect.size, pyg.SRCALPHA)
        for p in self.pendants:
            p.render(widget_cloth)
        cloth.blit(widget_cloth, apply_anchor(self.anchor, self.rect, cloth.get_rect()))
        return cloth


class WidgetManager:
    def __init__(self) -> None:
        self.uis: dict[str, Widget] = dict()

    def add_widget(self, widget: Widget) -> Self:
        name: str = widget.name
        if name in self.uis:
            raise Exception
        self.uis[name] = widget
        return self

    def query_widget(self, name: str) -> Widget | None:
        return self.uis.get(name)

    def render(self, screen: Surface) -> Surface:
        for w in sorted(self.uis.values(), key=lambda w: w.z):
            w.render(screen)
        return screen
