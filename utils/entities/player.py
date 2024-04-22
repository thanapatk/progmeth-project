from enum import Enum
import random
from typing import Literal

from pygame import Rect
from pygame.mixer import Sound

from utils.camera.camera import Camera
from utils.entities.enemy import Enemy
from utils.entities.entity import Entity, Facing
from utils.sprite import Sprites
from collections import deque


class PlayerAction(Enum):
    CHEER = 'cheer'
    DEATH = 'death'
    DUCK = 'duck'
    GET_UP = 'get_up'
    IDLE = 'idle'
    KICK = 'kick'
    KNOCK_BACK = 'knock_back'
    PUNCH = 'punch'
    RUN = 'run'
    WALK = 'walk'


class Player(Entity):
    __LOOP_ACTION = (PlayerAction.WALK, PlayerAction.RUN)
    __ATTACK_ACTION = (PlayerAction.PUNCH,
                       PlayerAction.KICK, PlayerAction.DUCK)
    _ENTITY_MOVEMENT: dict[str, tuple[int, int]] = {
        'idle': (0, 0),
        'walk': (0, 2),
        'run': (0, 6),
        'knock_back': (0, -5),
        'death': (2, -10)
    }

    def __init__(self, sprites: dict[str, Sprites], loc: tuple[int, int], facing: Facing, key_binding: dict[str, int], sfx: dict[str, Sound]) -> None:
        self.current_action = PlayerAction.IDLE
        self.__action_queue = deque()

        super().__init__(sprites, loc, facing)

        self.key_binding = key_binding
        self.inv_key_binding = {v: k for k, v in self.key_binding.items()}

        self.__is_running = True

        self.health = 3

        self.sfx = sfx
        self.sfx_mapping = {
            PlayerAction.PUNCH: (self.sfx['punch_1'], self.sfx['punch_2']),
            PlayerAction.KICK: (self.sfx['kick_1'], self.sfx['kick_2']),
            PlayerAction.DUCK: (self.sfx['duck_1'], self.sfx['duck_2']),
        }

    @property
    def is_running(self):
        return self.__is_running

    @is_running.setter
    def is_running(self, value: bool):
        self.__is_running_changed = self.__is_running != value
        self.__is_running = value

    def __knock_back(self, action: PlayerAction = PlayerAction.GET_UP):
        self.current_action = PlayerAction.KNOCK_BACK
        self.__action_queue.append(action)

    def __take_damage(self):
        self.sfx['take_damage'].play()
        self.health -= 1

        self.current_action = PlayerAction.KNOCK_BACK
        self.__action_queue.append(
            PlayerAction.GET_UP if self.health != 0 else PlayerAction.DEATH)

    def handle_attack(self, enemy: Enemy):
        self.facing = Facing.LEFT if enemy.facing == Facing.RIGHT else Facing.RIGHT

        if self.current_action not in self.__ATTACK_ACTION:
            self.__take_damage()

        # win
        elif self._WIN_CONDITION[self.current_action.value] == enemy.enemy_type:
            enemy.take_damage()

        # draw
        elif self.current_action.value == enemy.enemy_type:
            enemy.knock_back()
            self.__knock_back()

    def handle_action(self, pressed_key: int):
        if self._counter != 0:  # during animation
            return

        actions = self.inv_key_binding.get(
            pressed_key, self.current_action.name).split('_')
        if len(actions) != 2:
            return

        action, direction = actions
        facing = Facing.LEFT if direction == 'l' else Facing.RIGHT

        self.current_action = PlayerAction(action)
        self.facing = facing

    def update(self, camera: Camera) -> None:
        super().update(camera)

        if self.current_action == PlayerAction.DEATH:
            return

        self.a, self.v = self._ENTITY_MOVEMENT.get(
            self.current_action.value, self._ENTITY_MOVEMENT['idle'])

        if self.__is_running_changed and self._counter == 0:
            if self.is_running:
                self.current_action = PlayerAction.RUN
                self.facing = Facing.RIGHT
            else:
                self.current_action = PlayerAction.WALK
            self.__is_running_changed = False

        if self.current_action not in self.__LOOP_ACTION:
            frame_time = self.get_sprite().sprites_count

            if self._counter == 0 and self.current_action in self.sfx_mapping.keys():
                random.choice(self.sfx_mapping[self.current_action]).play()

            if self._counter == frame_time:
                if len(self.__action_queue) != 0:
                    self.current_action = self.__action_queue.popleft()
                elif self.is_running:
                    self.current_action = PlayerAction.RUN
                    self.facing = Facing.RIGHT
                else:
                    self.current_action = PlayerAction.WALK

                self._counter = 0
            else:
                self._counter += 1

        current_sprite = self.get_sprite()
        if self.current_action == PlayerAction.KNOCK_BACK and self.facing == Facing.LEFT:
            current_sprite.rect.move_ip(-self.v, 0)
        else:
            current_sprite.rect.move_ip(self.v, 0)
        current_sprite.flipped = self.facing == Facing.LEFT

        if self.prev_sprite != current_sprite:
            if current_sprite.flipped or (self.current_action == PlayerAction.RUN and self.prev_sprite.flipped):
                current_sprite.rect.topleft = (
                    self.loc[0] + (self.prev_sprite.image.get_size()[0] - current_sprite.image.get_size()[0]), self.loc[1])
            else:
                current_sprite.rect.topleft = self.loc

            # hide sprite off scene
            self.prev_sprite.rect.center = (-100, -100)
            self.prev_sprite = current_sprite

        # current_sprite.rect.move_ip(self.v, 0)
        # super().update(camera)
        self.loc = current_sprite.rect.topleft

    def get_sprite(self) -> Sprites:
        match self.current_action:
            case PlayerAction.KICK | PlayerAction.PUNCH | PlayerAction.WALK:
                sprite_name = f'{self.current_action.value}_{
                    "rl"[self.facing == Facing.LEFT]}'
            case _:
                sprite_name = self.current_action.value

        return self.sprites[sprite_name]
