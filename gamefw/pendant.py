"""
gamefw.pendant
"""

import pygame.surface
from typing_extensions import override
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



