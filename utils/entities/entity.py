from abc import abstractmethod
from enum import Enum

from utils.sprite import Sprites


class Facing(Enum):
    LEFT = 1
    RIGHT = -1


class Entity:
    def __init__(self, sprites: dict[str, Sprites], loc: tuple[int, int], facing: Facing) -> None:
        self.sprites = sprites
        self.facing = facing
        self.loc = loc

        current_sprite = self.get_sprite()
        self.prev_sprite = current_sprite
        current_sprite.rect.x, current_sprite.rect.y = self.loc

        self._counter = 0

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def get_sprite(self) -> Sprites:
        pass

    def get_all_sprites(self):
        return self.sprites.values()
