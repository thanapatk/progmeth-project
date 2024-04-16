from _collections_abc import dict_values
from abc import abstractmethod
from enum import Enum, auto
from pygame.transform import flip

from utils.sprite import Sprites


class Entity:
    def __init__(self, sprites: dict[str, Sprites]) -> None:
        self.sprites = sprites

    @abstractmethod
    def update(self) -> None:
        pass


class Facing(Enum):
    LEFT = 1
    RIGHT = -1
