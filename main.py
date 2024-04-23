# 1 - Import packages
import random
from pickle import load as pk_load, dump as pk_dump
from typing import Literal

import pygame

from utils.screen.menu import Menu
from utils.screen.settings import Settings
from utils.screen.stage import Stage
from utils.screen.tutorial import Tutorial
from utils.screen.background import Background
from utils.camera.camera import Camera
from utils.camera.scroll_method import Border, Follow
from utils.entities.enemy import Enemy
from utils.entities.enemy_manager import EnemyManager
from utils.entities.entity import Facing
from utils.entities.player import Player
from utils.sprite import RepeatType, SpriteLoader
from utils.screen.ui_manager import UI

# 2 - Define constants
GRAY = (200, 200, 200)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FRAMES_PER_SECOND = 24
SCROLL_PID = (.3, 0, .2)

with open('config.pkl', 'rb') as f:
    KEY_BINDING, VOLUME, HIGH_SCORE = pk_load(f)

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sound(s), etc.
player_sprites = SpriteLoader.load_sprites(
    'sprites/characters/player', scale=3, repeat=True, repeat_type=RepeatType.REITERATE, repeat_count=4)

enemy_sprites = {
    'punch': SpriteLoader.load_sprites('sprites/characters/enemy_punch',
                                       scale=3, repeat=True, repeat_type=RepeatType.REITERATE, repeat_count=4),
    'kick': SpriteLoader.load_sprites('sprites/characters/enemy_kick',
                                      scale=3, repeat=True, repeat_type=RepeatType.REITERATE, repeat_count=4),
    'duck': SpriteLoader.load_sprites('sprites/characters/enemy_duck',
                                      scale=3, repeat=True, repeat_type=RepeatType.REITERATE, repeat_count=4)
}

BGM = {
    'menu': 'audio/bgm/MENU.mp3',
    'playing': 'audio/bgm/ORIENTAL_GARDENS.mp3'
}
SOUND_FX = {
    'button_click': 'audio/sfx/menu/BUTTON_CLICK.mp3',
    'collide': 'audio/sfx/game/COLLIDE.wav',
    'duck_1': 'audio/sfx/game/DUCK_HIT1.wav',
    'duck_2': 'audio/sfx/game/DUCK_HIT2.wav',
    'kick_1': 'audio/sfx/game/KICK_HIT1.wav',
    'kick_2': 'audio/sfx/game/KICK_HIT2.wav',
    'punch_1': 'audio/sfx/game/PUNCH_HIT1.wav',
    'punch_2': 'audio/sfx/game/PUNCH_HIT2.wav',
    'take_damage': 'audio/sfx/game/TAKE_DAMAGE.wav'
}

SOUND_FX = {k: pygame.mixer.Sound(v) for k, v in SOUND_FX.items()}
for sound in SOUND_FX.values():
    sound.set_volume(VOLUME)

player = Player(player_sprites,
                (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), Facing.RIGHT, key_binding=KEY_BINDING, sfx=SOUND_FX)
player.is_running = False

entities_sprite_group = pygame.sprite.Group()
enemy_manager = EnemyManager(player, WINDOW_WIDTH, enemy_sprites, clock)

for sprite in player.get_all_sprites():
    entities_sprite_group.add(sprite)

camera = Camera(player, (WINDOW_WIDTH, WINDOW_WIDTH))
scroll_method = {
    'follow': Follow(camera, player, *SCROLL_PID),
    'border': Border(camera, player, *SCROLL_PID, border_left=0)
}
camera.scroll_method = scroll_method['follow']

background = Background(window)

# enemy_manager.started = True

ui = UI(window, player, "sprites/ui/heart.png")
menu = Menu(window, HIGH_SCORE)
settings = Settings(window, KEY_BINDING)
tutorial = Tutorial(window)
stage = Stage(window)
PAGE: Literal["menu", "settings", "tutorial",
              "start", "background"] = "menu"

stage_number = 1

pygame.mixer.music.load(BGM['menu'])
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play()

# 5 - Initialize variables

running = True
# 6 - Loop forever
while running:
    # print(KEY_BINDING)
    camera.scroll()
    background.draw()

    if PAGE == "menu":
        # player.started = False
        enemy_manager.started = False

        player.update(camera)
        entities_sprite_group.draw(window)

        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            PAGE = menu.handle_event(event)

    elif PAGE == "settings":
        settings.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            settings.handle_settings_events(event)

        VOLUME = settings.volume_value
        for sound in SOUND_FX.values():
            sound.set_volume(VOLUME)
        pygame.mixer.music.set_volume(VOLUME)

        if not settings.show_settings:
            settings.show_settings = True

            for key, value in settings.key_mappings.items():

                KEY_BINDING[key] = value

            player.key_binding = KEY_BINDING

            PAGE = "menu"

    elif PAGE == "background":
        stage.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                stage.handle_event(event, background)
        if not stage.show:
            background.update_stage(stage.stage)
            stage.show = True
            PAGE = "menu"

    elif PAGE == "tutorial":
        tutorial.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                tutorial.handle_event(event)
        if not tutorial.show:
            tutorial.show = True
            PAGE = "menu"

    elif PAGE == "start":
        if not player.started:
            player.started = True
            player.score = 0
        elif not enemy_manager.started:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(BGM['playing'])
            pygame.mixer.music.set_volume(VOLUME)
            pygame.mixer.music.play()

            enemy_manager.started = True
            enemy_manager.clear()
            background.reset_scroll()
            player.started = False

        camera.scroll()

        # 7 - Check for and handle events
        player.is_running = pygame.key.get_pressed()[player.key_binding['run']]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                player.handle_action(event.key)

        # 8 - Do any "per frame" actions
        enemy_manager.spawn_enemy(
            WINDOW_WIDTH, player.rect.y, entities_sprite_group)

        enemy_manager.check_collisions(player)
        enemy_manager.check_enemy_collisions()

        # 9 - Clear the window
        background.draw()
        ui.draw()

        # 10 - Draw all window elements
        # enemy_1.get_sprite()
        entities_sprite_group.draw(window)

        # 11 - Update the window
        player.update(camera)
        enemy_manager.update(camera)

        if player.health == 0:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(BGM['menu'])
            pygame.mixer.music.set_volume(VOLUME)
            pygame.mixer.music.play()

            HIGH_SCORE = max(HIGH_SCORE, player.score)
            menu.update_highscore(HIGH_SCORE)

            PAGE = 'menu'

    background.update_scroll(camera.offset.x)
    entities_sprite_group.update(play_animation=(
        enemy_manager.started or not Player.is_dead))
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait

with open('config.pkl', 'wb') as f:
    pk_dump((KEY_BINDING, VOLUME, HIGH_SCORE), f)

pygame.quit()
