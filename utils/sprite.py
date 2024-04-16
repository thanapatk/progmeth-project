import os
from enum import Enum
import copy

from pygame import Surface, transform
from pygame.image import load
from pygame.sprite import Sprite


class RepeatType(Enum):
    REITERATE = "Reiterate"
    CYCLE = "Cycle"


class Sprites(Sprite):
    def __init__(self, *, sprite_name: str, images: Surface | list[Surface], sprite_size: tuple[int, int], sprite_count: int, scale: int, flipped: bool = False, repeat: bool = False, repeat_count: int = 1, repeat_type: RepeatType = RepeatType.CYCLE):
        super().__init__()

        self.sprite_name = sprite_name
        self.sprites_count = sprite_count
        if isinstance(images, list):
            self.images = images
        else:
            self.images = self.from_spritesheet(
                images, sprite_size, self.sprites_count, scale)
        if repeat:
            self.sprites_count *= repeat_count
            if repeat_type == RepeatType.CYCLE:
                self.images *= repeat_count
            else:
                self.images = [
                    image for image in self.images for _ in range(repeat_count)]

        self.counter = 0
        self.image = self.images[self.counter]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (-100, -100)

        self.flipped = flipped

    def update(self):
        self.counter = (self.counter + 1) % self.sprites_count

        if self.flipped:
            self.image = transform.flip(
                self.images[self.counter], self.flipped, False).convert_alpha()
        else:
            self.image = self.images[self.counter]
        # self.rect = self.image.get_rect()

    def __getitem__(self, index: int) -> Surface:
        return self.images[index]

    @staticmethod
    def from_spritesheet(images: Surface, size: tuple[int, int], sprite_count: int, scale: int, key_color: tuple[int, int, int] = (255, 0, 255)) -> list[Surface]:
        width, height = size

        output = []
        for i in range(sprite_count):
            output_image = Surface(size).convert_alpha()
            output_image.fill(key_color)
            output_image.blit(
                images, (0, 0), (i * width, 0, width, height))
            if scale != 1:
                output_image = transform.scale(
                    output_image, (width * scale, height * scale))
            output_image.set_colorkey(key_color)

            output.append(output_image)

        return output

    def copy(self):
        copied = self.__class__(
            sprite_name=self.sprite_name,
            images=[image.copy()
                    for image in self.images],  # Deep copy each image
            sprite_size=(self.rect.width, self.rect.height),
            sprite_count=self.sprites_count,
            scale=1,  # assuming scale doesn't need to be deep copied
            flipped=self.flipped
        )
        copied.counter = self.counter
        copied.image = copied.images[self.counter]
        copied.rect = copied.image.get_rect()
        copied.rect.x, copied.rect.y = (-100, -100)
        return copied


class SpriteLoader:
    @staticmethod
    def load_sprites(path: str, sprite_size: tuple[int, int] | None = None, scale: int = 1, repeat: bool = False, repeat_count: int = 1, repeat_type: RepeatType = RepeatType.CYCLE) -> dict[str, Sprites]:
        sprite_paths = os.listdir(path)

        output = dict()

        for sprite_path in sprite_paths:
            img = load(f'{path}/{sprite_path}').convert_alpha()

            if sprite_size is None:
                _sprite_size = img.get_size()
            else:
                _sprite_size = sprite_size

            sprite_count = img.get_size()[0] // _sprite_size[0]
            sprite_name = sprite_path.split('.')[0]

            if sprite_count <= 1:
                _sprite_size = img.get_size()
                sprite_count = 1

            output[sprite_name] = Sprites(sprite_name=sprite_name, images=img, sprite_size=_sprite_size, sprite_count=sprite_count,
                                          scale=scale, repeat=repeat, repeat_count=repeat_count, repeat_type=repeat_type)

        return output

    @staticmethod
    def copy_sprites(d: dict[str, Sprites]) -> dict[str, Sprites]:
        return {k: v.copy() for k, v in d.items()}
