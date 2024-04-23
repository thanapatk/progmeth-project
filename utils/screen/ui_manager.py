import pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
BRIGHT_GREEN = (0, 255, 0)
BRIGHT_RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_ORANGE = (255, 165, 80)
SFONT = pygame.font.Font('font/8-bit Arcade In.ttf', 50)
BFONT = pygame.font.Font('font/8-bit Arcade In.ttf', 100)


class UI:

    def __init__(self, screen, player, image_path) -> None:
        self.bfont = BFONT
        self.sfont = SFONT
        self.player = player
        self.hearts = player.health
        self.score = player.score
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen

    def update(self):
        self.hearts: int = self.player.health
        self.score = self.player.score

    def draw(self):
        xoffset = 5
        yoffset = 3
        self.update()
        title = self.bfont.render(f"Score {self.score}", True, LIGHT_ORANGE)
        titlew, titleh = title.get_size()
        self.screen.blit(self.bfont.render(f"Score {self.score}", True, BLACK),
                         (SCREEN_WIDTH//2-titlew//2 + xoffset, 10+yoffset))
        self.screen.blit(title, (SCREEN_WIDTH//2-titlew//2, 10))
        for i in range(1, self.hearts + 1):
            self.screen.blit(
                self.image, (SCREEN_WIDTH - 40 - 40*i, 40))
