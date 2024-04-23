from utils.screen.settings import Button
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
BFONT = pygame.font.Font('font/8-bit Arcade In.ttf', 120)


class Tutorial:
    def __init__(self, window) -> None:
        self.window = window
        self.sfont = SFONT
        self.bfont = BFONT
        self.show = True
        self.close_button = Button(
            "Close", SCREEN_WIDTH - 200, 50, 150, 50, BRIGHT_RED, WHITE)
        self.show_settings = True

    def draw(self):
        xoffset = 5
        yoffset = 3
        pygame.draw.rect(self.window, DARK_GRAY,
                         (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        self.close_button.draw(self.window, self.sfont)
        title = self.bfont.render("HOW TO PLAY", True, LIGHT_ORANGE)
        titlew, titleh = title.get_size()
        self.window.blit(self.bfont.render("HOW TO PLAY", True, BLACK),
                         (SCREEN_WIDTH//2-titlew//2 + xoffset, 100+yoffset))
        self.window.blit(title, (SCREEN_WIDTH//2-titlew//2, 100))
        lines = ["THERE ARE THREE TYPES OF ATTACKS", "JAB BEATS KICK", "KICK BEATS SWEEP",
                 "AND SWEEP BEATS PUNCH", "FIGHT AND ESCAPE FOR AS LONG AS YOU CAN"]
        y = 220
        xoffset = 3
        yoffset = 1
        for line in lines:
            title = self.sfont.render(line, True, LIGHT_GRAY)
            titlew, titleh = title.get_size()
            self.window.blit(self.sfont.render(line, True, BLACK),
                             (SCREEN_WIDTH//2-titlew//2 + xoffset, y+yoffset))
            self.window.blit(title, (SCREEN_WIDTH//2-titlew//2, y))
            y += titleh + 10

    def handle_event(self, event):
        if self.close_button.is_clicked(event):
            self.show = False
