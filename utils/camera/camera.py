from __future__ import annotations

from pygame.math import Vector2
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.camera.scroll_method import ScrollMethod
    from utils.entities.entity import Entity


class Camera:
    def __init__(self, tracked_entity: Entity,  display_size: tuple[int, int]):
        self.entity = tracked_entity
        self.offset = Vector2(0, 0)
        self.offset_float = Vector2(0, 0)
        self.DISPLAY_SIZE = Vector2(display_size)

    @property
    def CONST(self):
        return Vector2(
            (self.entity.rect.w -
             self.DISPLAY_SIZE.x) // 2, (self.entity.rect.h - self.DISPLAY_SIZE.y) // 2 + 180)

    @property
    def scroll_method(self):
        return self.__scroll_method

    @scroll_method.setter
    def scroll_method(self, method: ScrollMethod):
        self.__scroll_method = method

    def scroll(self):
        self.scroll_method.scroll()
