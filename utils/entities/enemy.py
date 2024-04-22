from collections import deque
from enum import Enum
from typing import Literal

from utils.camera.camera import Camera
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
    _ENTITY_MOVEMENT: dict[str, tuple[int, int]] = {
        'idle': (0, 0),
        'walk': (0, 3),
        'run': (0, 7),
        'knock_back': (0, -10),
        'death': (2, -10)
    }

    def __init__(self, enemy_type: str, sprites: dict[str, Sprites], loc: tuple[int, int], facing: Facing) -> None:
        self.is_dead = False
        self.current_action = EnemyAction.WALK
        self.enemy_type = enemy_type

        self.__action_queue = deque()

        super().__init__(sprites, loc, facing)

    def attack(self):
        self.current_action = EnemyAction.ATTACK

    def knock_back(self, length: int = 1, action: EnemyAction = EnemyAction.GET_UP):
        self.current_action = EnemyAction.KNOCK_BACK
        self.__action_queue.append(action)

    def take_damage(self):
        self.current_action = EnemyAction.DEATH
        # self.is_dead = True

    def update(self, camera: Camera) -> None:
        super().update(camera)

        if self.rect.y > 720:
            self.is_dead = True

        self.a, self.v = self._ENTITY_MOVEMENT.get(
            self.current_action.value, self._ENTITY_MOVEMENT['idle'])

        if self.current_action not in self.__LOOP_ACTION:
            frame_time = self.get_sprite().sprites_count

            if self._counter >= frame_time:
                if self.current_action == EnemyAction.DEATH:
                    pass
                #     self.is_dead = True
                elif len(self.__action_queue) != 0:
                    self.current_action = self.__action_queue.popleft()
                else:
                    self.current_action = EnemyAction.WALK
                    self._counter = 0
            else:
                self._counter += 1

        current_sprite = self.get_sprite()
        current_sprite.flipped = self.facing == Facing.LEFT

        if self.prev_sprite != current_sprite:
            current_sprite.rect.x, current_sprite.rect.y = self.loc
            # hide sprite off scene
            self.prev_sprite.rect.x, self.prev_sprite.rect.y = (-100, -100)
            self.prev_sprite = current_sprite

        if self.current_action == EnemyAction.DEATH:
            current_sprite.rect.move_ip(0, self.v + self.a * self._counter)
        else:
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
