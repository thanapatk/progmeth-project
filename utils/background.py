import pygame
import math


class Background:
    def __init__(self, screen: pygame.Surface):
        self.update_stage(1)
        self.bg_width = self.bg_images[0].get_width()
        self.screen = screen
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.tiles = math.ceil(self.SCREEN_WIDTH / self.bg_width) + 1
        self.scroll = [0] * len(self.bg_images)
        self.is_running = False
        self.is_still = True

    def update_stage(self, stage: int):
        self.bg_images = list()
        self.background = pygame.image.load(
            f"sprites/background/{stage}/1.png").convert_alpha()
        for i in range(5):
            bg_image = pygame.image.load(
                f"sprites/background/{stage}/{i+2}.png").convert_alpha()
            self.bg_images.append(bg_image)

    def draw(self):
        for x in range(self.tiles):
            self.screen.blit(self.background, ((x * self.bg_width), 0))

        for i in range(len(self.bg_images)):
            for x in range(self.tiles):
                self.screen.blit(self.bg_images[i], ((
                    x * self.bg_width) + self.scroll[i], 0))

    def update_scroll(self, scroll_speed: int | float):
        for i in range(len(self.bg_images)):
            self.scroll[i] -= math.floor(scroll_speed * (1 + 0.2 * i))

        self.reset_scroll()

    def reset_scroll(self):
        for i in range(len(self.bg_images)):
            if abs(self.scroll[i]) > self.bg_width:
                self.scroll[i] = 0
