# 1 - Import packages
from utils.sprite import RepeatType, SpriteLoader, Sprites
from utils.entities.entity import Enemy, EnemyAction, Facing
import pygame
from copy import deepcopy


# 2 - Define constants
GRAY = (200, 200, 200)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FRAMES_PER_SECOND = 24

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sound(s), etc.
enemy_punch = SpriteLoader.load_sprites('sprites/characters/enemy_punch', (16, 32),
                                        scale=3, repeat=True, repeat_type=RepeatType.REITERATE, repeat_count=4)

enemy_1 = Enemy(SpriteLoader.copy_sprites(
    enemy_punch), (1280 - 32, 0), Facing.RIGHT)
enemy_2 = Enemy(SpriteLoader.copy_sprites(enemy_punch), (0, 0), Facing.LEFT)
# enemy_2 = Enemy(enemy_punch.copy(), (100, 0), Facing.LEFT)

enemies = [enemy_1, enemy_2]

entity_group = pygame.sprite.Group()

for sprites in map(Enemy.get_all_sprites, enemies):
    for sprite in sprites:
        entity_group.add(sprite)


# 5 - Initialize variables

running = True
# 6 - Loop forever
while running:
    # 7 - Check for and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                enemy_1.current_action = EnemyAction.RUN
            if event.key == pygame.K_d:
                enemy_2.current_action = EnemyAction.RUN
            if event.key == pygame.K_j:
                enemy_1.current_action = EnemyAction.ATTACK
            if event.key == pygame.K_f:
                enemy_2.current_action = EnemyAction.ATTACK
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                enemy_2.current_action = EnemyAction.WALK
            if event.key == pygame.K_k:
                enemy_1.current_action = EnemyAction.WALK

    # 8 - Do any "per frame" actions

    # 9 - Clear the window
    window.fill(GRAY)

    # 10 - Draw all window elements
    # enemy_1.get_sprite()
    entity_group.draw(window)

    # 11 - Update the window
    pygame.display.update()
    entity_group.update()
    for enemy in enemies:
        enemy.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait


pygame.quit()
