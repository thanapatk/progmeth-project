import pygame
# from pygame.locals import *
import sys
import pygwidgets
# from utils.screen.background import Background

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_ORANGE = (255, 165, 80)
DARK_GRAY = (40, 40, 40)
BROWN = (139, 69, 19)
LIGHT_BROWN = (139, 69, 19)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FRAME_RATE = 24
HIGHEST_SCORE = 10
HIGHEST_SCORE_OUTPUT = str(HIGHEST_SCORE)


class Menu:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 165, 0)
    LIGHT_ORANGE = (255, 165, 80)
    DARK_GRAY = (40, 40, 40)
    BROWN = (139, 69, 19)
    LIGHT_BROWN = (139, 69, 19)
    # WINDOW_WIDTH = 1280
    # WINDOW_HEIGHT = 720
    # FRAME_RATE = 24
    # HIGHEST_SCORE = 10
    # HIGHEST_SCORE_OUTPUT = str(HIGHEST_SCORE)

    def __init__(self, window, highscore=0) -> None:
        self.show = True
        # self.background = pygame.image.load(bg_path).convert_alpha()
        self.highscore = highscore
        self.window = window
        self.WINDOW_WIDTH = window.get_width()
        self.WINDOW_HEIGHT = window.get_height()
        self.oStartbutton = pygwidgets.CustomButton(
            window, (self.WINDOW_WIDTH // 2, 360), "sprites/ui/play_up.png", "sprites/ui/play_down.png")
        self.oSettingbutton = pygwidgets.CustomButton(
            window, (740, 360), "sprites/ui/setting_up.png", "sprites/ui/setting_down.png")
        self.oBackgroundchange = pygwidgets.CustomButton(
            window, (540, 360), "sprites/ui/background_up.png", "sprites/ui/background_down.png")
        self.oTexthighscore = pygwidgets.DisplayText(window, (550, 300), "HIGH SCORE", "font/8-bit Arcade In.ttf", 100, justified="center",
                                                     textColor=LIGHT_ORANGE)
        self.oTextscore = pygwidgets.DisplayText(window, (550, 330), str(self.highscore), "font/8-bit Arcade In.ttf", 90, justified="center",
                                                 textColor=LIGHT_ORANGE)
        self.oTextgamename = pygwidgets.DisplayText(window, (self.WINDOW_WIDTH // 2, 360), "JAB KICK SWEEP", "font/8-bit Arcade In.ttf", 160,
                                                    justified="left", textColor=LIGHT_ORANGE)

        self.oBGname = pygwidgets.DisplayText(window, (self.WINDOW_WIDTH // 2, 360), "JAB KICK SWEEP", "font/8-bit Arcade In.ttf", 160,
                                              justified="left", textColor=BLACK)
        self.oBGhighscore = pygwidgets.DisplayText(window, (550, 300), "HIGH SCORE", "font/8-bit Arcade In.ttf", 100, justified="center",
                                                   textColor=BLACK)
        self.oBGscore = pygwidgets.DisplayText(window, (550, 330), str(self.highscore), "font/8-bit Arcade In.ttf", 90, justified="center",
                                               textColor=BLACK)
        self.oTutorialbutton = pygwidgets.TextButton(
            window, (1050, 10), "Tutorial", fontName="font/8-bit Arcade In.ttf", fontSize=48, upColor=LIGHT_ORANGE, overColor=LIGHT_BROWN, downColor=BROWN)

        adjust(self.oStartbutton, 250)
        adjust(self.oSettingbutton, 250, width=360)
        adjust(self.oBackgroundchange, 250, width=-360)
        adjust(self.oTexthighscore, -170)
        adjust(self.oTextscore, -120)
        adjust(self.oTextgamename, -270)

        adjust(self.oBGname, -264, 6)
        adjust(self.oBGhighscore, -166, 4)
        adjust(self.oBGscore, -116, 4)

    def update_highscore(self, new_score):
        self.highscore = new_score

    # def update_background(self, bg_path):
    #     self.background = pygame.image.load(bg_path).convert_alpha()

    def draw(self):
        self.oBGname.draw()
        self.oBGhighscore.draw()
        self.oBGscore.draw()

        self.oTexthighscore.draw()
        self.oTextscore.draw()
        self.oTextgamename.draw()
        self.oStartbutton.draw()
        self.oSettingbutton.draw()
        self.oBackgroundchange.draw()
        self.oTutorialbutton.draw()

    def handle_event(self, event):
        if self.oStartbutton.handleEvent(event):
            return "start"
        elif self.oSettingbutton.handleEvent(event):
            return "settings"

        elif self.oBackgroundchange.handleEvent(event):
            return "background"

        elif self.oTutorialbutton.handleEvent(event):
            return "tutorial"

        return "menu"


def adjust(obj, height=None, width=None):
    w, h = obj.getRect().size

    loc = [WINDOW_WIDTH // 2 - w // 2, WINDOW_HEIGHT // 2 - h // 2]

    if width:
        loc[0] += width
    if height:
        loc[1] += height

    obj.setLoc(loc)


# if __name__ == '__main__':
#     pygame.init()
#     window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#     clock = pygame.time.Clock()
#     Background = pygame.image.load("sprites/ui/BG.png").convert_alpha()

#     menu = Menu(window, 100)
#     page = "menu"

#     while True:
#         if page == "menu":
#             menu.draw()
#             menu.handle_event()

#         pygame.display.update()

#         clock.tick(FRAME_RATE)
