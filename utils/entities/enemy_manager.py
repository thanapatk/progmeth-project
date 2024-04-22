import random
from typing import Literal
from pygame import Rect
from pygame.sprite import Group
from utils.camera.camera import Camera
from utils.entities.enemy import Enemy, EnemyAction
from utils.data_structure.llist import DoublyLinkedList as DLList
from utils.entities.entity import Facing
from utils.entities.player import Player, PlayerAction
from utils.sprite import SpriteLoader, Sprites


class EnemyManager:
    def __init__(self, enemy_sprites: dict[str, dict[str, Sprites]]) -> None:
        self.enemies: DLList[Enemy] = DLList()
        self.enemy_sprites = enemy_sprites
        self.enemy_types = list(self.enemy_sprites.keys())

    def add_enemy(self, enemy: Enemy, sprite_group: Group):
        self.enemies.append(enemy)

        for sprite in enemy.get_all_sprites():
            sprite_group.add(sprite)

    def spawn_enemy(self, loc: tuple[int, int], facing: Facing, sprite_group: Group):
        enemy_type = random.choice(self.enemy_types)

        self.add_enemy(
            Enemy(enemy_type, SpriteLoader.copy_sprites(self.enemy_sprites[enemy_type]), loc, facing), sprite_group)

    def update(self, camera: Camera):
        for enemy_node in self.enemies.iter_node():
            if enemy_node.data.is_dead:
                self.enemies.delete(node=enemy_node)
            else:
                enemy_node.data.update(camera)

    def __check_enemy_collisions(self, enemy: Enemy, enemies_dict: dict):
        for _rect, enemy_node in enemy.rect.collidedictall(enemies_dict):
            enemy_node.data.knock_back()

    def check_enemy_collisions(self, enemies_dict: dict | None = None):
        if enemies_dict is None:
            enemies_dict = {tuple(
                enemy_node.data.rect): enemy_node for enemy_node in self.enemies.iter_node() if enemy_node.data.current_action != EnemyAction.DEATH and enemy_node.data.current_action != EnemyAction.KNOCK_BACK}

        for enemy in self.enemies:
            if enemy.current_action == EnemyAction.KNOCK_BACK:
                self.__check_enemy_collisions(enemy, enemies_dict)

    def check_collisions(self, player: Player):
        enemies_dict = {tuple(
            enemy_node.data.rect): enemy_node for enemy_node in self.enemies.iter_node() if enemy_node.data.current_action != EnemyAction.DEATH}

        output = player.rect.collidedictall(enemies_dict)  # type: ignore

        for _rect, enemy_node in output:
            if player.current_action == PlayerAction.KNOCK_BACK:
                enemy_node.data.knock_back()
                self.__check_enemy_collisions(enemy_node.data, enemies_dict)
            else:
                enemy_node.data.attack()
                player.handle_attack(enemy_node.data)
