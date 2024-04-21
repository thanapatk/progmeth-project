from abc import abstractmethod
from enum import Enum

from utils.camera.camera import Camera
from utils.sprite import Sprites


class Facing(Enum):
    LEFT = -1
    RIGHT = 1


class Entity:
    _ENTITY_MOVEMENT: dict[str, tuple[int, int]] = {
        'idle': (0, 0),
        'walk': (0, 2),
        'run': (0, 6)
    }

    def __init__(self, sprites: dict[str, Sprites], loc: tuple[int, int], facing: Facing) -> None:
        self.sprites = sprites
        self.facing = facing
        self.loc = loc

        current_sprite = self.get_sprite()
        self.prev_sprite = current_sprite
        current_sprite.rect.x, current_sprite.rect.y = self.loc

        self._counter = 0

        self.a, self.v = 0, 0

    @property
    def rect(self):
        return self.get_sprite().rect

    def update(self, camera: Camera) -> None:
        self.rect.move_ip(-camera.offset.x, -camera.offset.y)

    @abstractmethod
    def get_sprite(self) -> Sprites:
        pass

    def get_all_sprites(self):
        return self.sprites.values()
