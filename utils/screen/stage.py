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


class Stage:
    def __init__(self, window) -> None:
        self.stage = 1
        self.window = window
        self.sfont = SFONT
        self.bfont = BFONT
        self.show = True
        self.close_button = Button(
            "Close", SCREEN_WIDTH - 200, 50, 150, 50, BRIGHT_RED, WHITE)
        self.show_settings = True

        self.button1 = Button("POWER STATION DAY", 70, 220,
                              SCREEN_WIDTH-140, 80, LIGHT_ORANGE, BLACK)
        self.button2 = Button("POWER STATION NIGHT", 70,
                              320, SCREEN_WIDTH-140, 80, LIGHT_ORANGE, BLACK)
        self.button3 = Button("ABANDONED CITY DAY", 70,
                              420, SCREEN_WIDTH-140, 80, LIGHT_ORANGE, BLACK)
        self.button4 = Button("ABANDONED CITY NIGHT", 70,
                              520, SCREEN_WIDTH-140, 80, LIGHT_ORANGE, BLACK)

    def draw(self):
        xoffset = 5
        yoffset = 3
        pygame.draw.rect(self.window, DARK_GRAY,
                         (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        self.close_button.draw(self.window, self.sfont)
        title = self.bfont.render("BACKGROUND SELECT", True, LIGHT_ORANGE)
        titlew, titleh = title.get_size()
        self.window.blit(self.bfont.render("BACKGROUND SELECT", True, BLACK),
                         (SCREEN_WIDTH//2-titlew//2 + xoffset, 100+yoffset))
        self.window.blit(title, (SCREEN_WIDTH//2-titlew//2, 100))
        self.button1.draw(self.window, SFONT)
        self.button2.draw(self.window, SFONT)
        self.button3.draw(self.window, SFONT)
        self.button4.draw(self.window, SFONT)

    def handle_event(self, event, background):
        if self.close_button.is_clicked(event):
            self.show = False
        elif self.button1.is_clicked(event):
            self.stage = 1
        elif self.button2.is_clicked(event):
            self.stage = 2
        elif self.button3.is_clicked(event):
            self.stage = 3
        elif self.button4.is_clicked(event):
            self.stage = 4

        background.update_stage(self.stage)
