import math
import random
from typing import Literal
from pygame import Rect
import pygame
from pygame.time import Clock
from pygame.sprite import Group
from utils.camera.camera import Camera
from utils.entities.enemy import Enemy, EnemyAction
from utils.data_structure.llist import DoublyLinkedList as DLList
from utils.entities.entity import Facing
from utils.entities.player import Player, PlayerAction
from utils.sprite import SpriteLoader, Sprites


class EnemyManager:
    def __init__(self, player: Player, window_width: int, enemy_sprites: dict[str, dict[str, Sprites]], clock: Clock) -> None:
        self.enemies: DLList[Enemy] = DLList()
        self.enemy_sprites = enemy_sprites
        self.enemy_types = list(self.enemy_sprites.keys())
        self.player = player
        self.window_width = window_width

        self.clock = clock
        self.started = False
        self.__started_time = 0

        self.last_enemy_spawn_time = self.__started_time
        self.prob, self.cool_down = self.get_spawn_rates()

    def clear(self):
        for enemy in self.enemies.iter_node():
            self.enemies.delete(node=enemy)

        print(self.enemies)

    @property
    def started(self):
        return self.__started_level

    def get_spawn_rates(self):
        t = self.elapsed_time

        prob = min(1, 55 * math.log(t / 5 + 1))
        cool_down = max(2, -.06 * t + 4.08)

        return prob, cool_down

    @started.setter
    def started(self, value: bool):
        self.__started_level = value
        if self.__started_level:
            self.__started_time = self.clock.get_time()

    @property
    def elapsed_time(self):
        return (pygame.time.get_ticks() - self.__started_time) / 1000

    def add_enemy(self, enemy: Enemy, sprite_group: Group):
        self.enemies.append(enemy)

        for sprite in enemy.get_all_sprites():
            sprite_group.add(sprite)

    def spawn_enemy(self, window_width: int, y: int, sprite_group: Group):
        t = self.elapsed_time
        if t - self.last_enemy_spawn_time < self.cool_down:
            return

        self.prob, self.cool_down = self.get_spawn_rates()
        if random.random() > self.prob:
            return

        self.last_enemy_spawn_time = t

        enemy_type = random.choice(self.enemy_types)
        if self.prob < 0.7:
            facing = (Facing.LEFT, Facing.RIGHT)[random.random() < self.prob]
        else:
            facing = random.choice((Facing.LEFT, Facing.RIGHT))

        loc_x = random.randint(-600, -100)

        if facing == Facing.LEFT:
            loc_x = window_width + loc_x * -1

        enemy = Enemy(enemy_type, SpriteLoader.copy_sprites(
            self.enemy_sprites[enemy_type]), (loc_x, y), facing)

        enemies = list(self.enemies)
        self.add_enemy(enemy, sprite_group)

        while enemy.rect.collidelist([e.rect for e in enemies]) != -1:
            enemy.rect.move_ip(enemy.rect.width * facing.value, 0)

    def update(self, camera: Camera):
        for enemy_node in self.enemies.iter_node():
            if enemy_node.data.is_dead:
                self.enemies.delete(node=enemy_node)
            else:
                tmp_action = enemy_node.data.current_action
                distance = abs(self.player.loc[0] - enemy_node.data.loc[0])
                # print(distance)
                if distance > self.window_width:
                    self.player.score += 25
                    self.enemies.delete(node=enemy_node)
                # elif distance > self.window_width // 4:
                #     enemy_node.data.current_action = EnemyAction.RUN
                else:
                    enemy_node.data.current_action = tmp_action if tmp_action != EnemyAction.RUN else EnemyAction.WALK

                enemy_node.data.update(camera)

    def __check_enemy_collisions(self, enemy: Enemy, enemies_dict: dict):
        for _rect, enemy_node in enemy.rect.collidedictall(enemies_dict):
            if enemy_node.data == enemy:
                continue

            enemy_node.data.knock_back()

            while enemy_node.data.rect.collidelist([e.rect for e in self.enemies if e != enemy_node.data and e.current_action not in (EnemyAction.DEATH, EnemyAction.KNOCK_BACK, EnemyAction.ATTACK)]) != -1:
                enemy_node.data.rect.move_ip(-1 * enemy.facing.value, 0)

    def check_enemy_collisions(self, enemies_dict: dict | None = None):
        if enemies_dict is None:
            enemies_dict = {tuple(
                enemy_node.data.rect): enemy_node for enemy_node in self.enemies.iter_node() if enemy_node.data.current_action not in (EnemyAction.DEATH, EnemyAction.KNOCK_BACK, EnemyAction.ATTACK)}

        for enemy in self.enemies:
            if enemy.current_action == EnemyAction.KNOCK_BACK:
                self.__check_enemy_collisions(enemy, enemies_dict)

    def check_collisions(self, player: Player):
        enemies_dict = {tuple(
            enemy_node.data.rect): enemy_node for enemy_node in self.enemies.iter_node() if enemy_node.data.current_action not in (EnemyAction.DEATH, EnemyAction.ATTACK)}

        output = player.rect.collidedictall(enemies_dict)  # type: ignore

        for _rect, enemy_node in output:
            if player.current_action == PlayerAction.KNOCK_BACK:
                enemy_node.data.knock_back()
            else:
                enemy_node.data.attack()
                player.handle_attack(enemy_node.data)
