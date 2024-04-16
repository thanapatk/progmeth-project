from enum import Enum
from utils.entities.entity import Entity, Facing
from utils.sprite import Sprites


class EnemyAction(Enum):
    IDLE = 'idle'
    WALK = 'walk'
    RUN = 'run'
    ATTACK = 'attack'
    KNOCK_BACK = 'knock_back'


class Enemy(Entity):
    def __init__(self, sprites: dict[str, Sprites], loc: tuple[int, int], facing: Facing) -> None:
        super().__init__(sprites)
        self.current_action = EnemyAction.WALK
        self.facing = facing
        self.loc = loc

        current_sprite = self.get_sprite()
        self.prev_sprite = current_sprite
        current_sprite.rect.x, current_sprite.rect.y = self.loc

        self.counter = 0

    def update(self):
        match self.current_action:
            # TODO: figure out enemy walk, run speed
            case EnemyAction.WALK:
                self.a = 0
                self.v = 2
            case EnemyAction.RUN:
                self.a = 0
                self.v = 5
            case EnemyAction.KNOCK_BACK:
                # TODO: Enemy Knock back
                pass
            case _:
                self.a = 0
                self.v = 0

                self.frame_time = self.get_sprite().sprites_count

                if self.counter == self.frame_time:
                    self.current_action = EnemyAction.WALK
                    self.counter = 0
                else:
                    self.counter += 1

        current_sprite = self.get_sprite()
        current_sprite.flipped = self.facing == Facing.RIGHT

        if self.prev_sprite != current_sprite:
            current_sprite.rect.x, current_sprite.rect.y = self.loc
            self.prev_sprite.rect.x, self.prev_sprite.rect.y = (-100, -100)
            self.prev_sprite = current_sprite

        current_sprite.rect.move_ip(self.v * self.facing.value, 0)
        self.loc = (current_sprite.rect.x, current_sprite.rect.y)

    def get_sprite(self) -> Sprites:
        match self.current_action:
            case EnemyAction.ATTACK | EnemyAction.WALK:
                sprite_name = f'{self.current_action.value}_{
                    "rl"[self.facing == Facing.LEFT]}'
            case _:
                sprite_name = self.current_action.value

        return self.sprites[sprite_name]

    def get_all_sprites(self):
        return self.sprites.values()
