from enum import Enum

from utils.entities.entity import Entity, Facing
from utils.sprite import Sprites


class EnemyAction(Enum):
    ATTACK = 'attack'
    DEATH = 'death'
    GET_UP = 'get_up'
    IDLE = 'idle'
    KNOCK_BACK = 'knock_back'
    RUN = 'run'
    WALK = 'walk'


class Enemy(Entity):
    __LOOP_ACTION = (EnemyAction.WALK, EnemyAction.RUN)

    def __init__(self, sprites: dict[str, Sprites], loc: tuple[int, int], facing: Facing) -> None:
        self.current_action = EnemyAction.WALK

        super().__init__(sprites, loc, facing)

    def update(self) -> None:
        self.a, self.v = self._ENTITY_MOVEMENT.get(
            self.current_action.value, self._ENTITY_MOVEMENT['idle'])

        if self.current_action not in self.__LOOP_ACTION:
            frame_time = self.get_sprite().sprites_count

            if self._counter == frame_time:
                self.current_action = EnemyAction.WALK
                self._counter = 0
            else:
                self._counter += 1

        current_sprite = self.get_sprite()
        current_sprite.flipped = self.facing == Facing.RIGHT

        if self.prev_sprite != current_sprite:
            current_sprite.rect.x, current_sprite.rect.y = self.loc
            # hide sprite off scene
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
