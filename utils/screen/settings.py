import pygame

# pygame.init()

# Constants
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

# Screen setup
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Game")


class Settings:

    def __init__(self, screen, key_binding):
        self.sfont = SFONT
        self.bfont = BFONT
        self.screen = screen
        self.close_button = Button(
            "Close", SCREEN_WIDTH - 200, 50, 150, 50, BRIGHT_RED, WHITE)
        self.show_settings = True
        self.volume_value = 0.5  # Initialize volume control
        self.is_dragging = False  # Initialize is_dragging

        self.slider_rect = pygame.Rect(SCREEN_WIDTH // 3, 150, 600, 20)
        self.slider_handle_rect = pygame.Rect(
            self.slider_rect.x + self.slider_rect.width * self.volume_value - 10, self.slider_rect.y - 5, 20, 30)

        # Key bindings setup
        self.key_buttons = {}
        self.key_mappings = {}

        self.key_binding = key_binding
        # actions = ["Action 1", "Action 2", "Action 3",
        #            "RUNN", "Action 5", "Action 6", "Action 7"]
        # default_keys = ['s', 'd', 'f', 'space', 'j', 'k', 'l']

        # Calculate positions for symmetry
        left_column_x = SCREEN_WIDTH // 4
        right_column_x = 3 * SCREEN_WIDTH // 4
        start_y = 300
        gap_y = 70

        positions = [
            (left_column_x, start_y),
            (left_column_x, start_y + gap_y),
            (left_column_x, start_y + 2 * gap_y),
            # Space button centered and lower
            (SCREEN_WIDTH // 2 + 120, start_y + 3.5 * gap_y),
            (right_column_x, start_y),
            (right_column_x, start_y + gap_y),
            (right_column_x, start_y + 2 * gap_y)
        ]

        for i, action in enumerate(self.key_binding.keys()):
            key = self.key_binding.get(action)
            rect = pygame.Rect(positions[i][0] - 100, positions[i][1], 200, 50)
            self.key_buttons[action] = rect
            self.key_mappings[action] = key

    def draw(self):
        xoffset = 5
        yoffset = 3
        # Draw a settings background
        pygame.draw.rect(self.screen, DARK_GRAY,
                         (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        # Draw close button
        self.close_button.draw(self.screen, self.sfont)
        # Draw volume slider and percentage
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.slider_rect)
        pygame.draw.rect(self.screen, LIGHT_ORANGE, self.slider_handle_rect)
        volume_text = "Volume "
        self.screen.blit(self.sfont.render(volume_text, True, ORANGE),
                         (SCREEN_WIDTH//4-70, self.slider_rect.y-15))

        # JAB
        Jab = self.bfont.render("JAB", True, LIGHT_ORANGE)
        Jabw, Jabh = Jab.get_size()
        self.screen.blit(self.bfont.render("JAB", True, BLACK),
                         (SCREEN_WIDTH//2-Jabw//2 + xoffset, 300-15+2+yoffset))
        self.screen.blit(Jab, (SCREEN_WIDTH//2-Jabw//2, 300-15))

        # KICK
        Kick = self.bfont.render("KICK", True, LIGHT_ORANGE)
        Kickw, Kickh = Kick.get_size()
        self.screen.blit(self.bfont.render("KICK", True, BLACK),
                         (SCREEN_WIDTH//2-Kickw//2 + xoffset, 300-15+70+2+yoffset))
        self.screen.blit(Kick, (SCREEN_WIDTH//2-Kickw//2, 300-15+70))

        # SWEEP
        Sweep = self.bfont.render("SWEEP", True, LIGHT_ORANGE)
        Sweepw, Kickh = Sweep.get_size()
        self.screen.blit(self.bfont.render("SWEEP", True, BLACK),
                         (SCREEN_WIDTH//2-Sweepw//2 + xoffset, 300-15+70+70+2+yoffset))
        self.screen.blit(Sweep, (SCREEN_WIDTH//2-Sweepw//2, 300-15+70+70))

        # RUN
        Run = self.bfont.render("RUN", True, LIGHT_ORANGE)
        Runw, Runh = Run.get_size()
        self.screen.blit(self.bfont.render("RUN", True, BLACK), (SCREEN_WIDTH //
                         2-1.2*Runw + xoffset, 300-15+70+70+70*1.5+2+yoffset-5))
        self.screen.blit(
            Run, (SCREEN_WIDTH//2-1.2*Runw, 300-15+70+70+70*1.5-5))

        # Left
        Left = self.bfont.render("Left", True, LIGHT_ORANGE)
        Leftw, Lefth = Run.get_size()
        self.screen.blit(self.bfont.render("Left", True, BLACK), ((
            SCREEN_WIDTH // 4 - Leftw//2 - 20)+xoffset, 230+yoffset))
        self.screen.blit(Left, (SCREEN_WIDTH // 4 - Leftw//2-20, 230))

        # RIGHT
        RIGHT = self.bfont.render("Right", True, LIGHT_ORANGE)
        RIGHTw, Lefth = RIGHT.get_size()
        self.screen.blit(self.bfont.render("RIGHT", True, BLACK), ((
            3*SCREEN_WIDTH // 4 - RIGHTw//2)+xoffset, 230+yoffset))
        self.screen.blit(RIGHT, (3*SCREEN_WIDTH // 4 - RIGHTw//2, 230))

        # Draw key mapping buttons
        for action, rect in self.key_buttons.items():
            pygame.draw.rect(self.screen, LIGHT_GRAY, rect, 5)
            key_name = pygame.key.name(self.key_mappings[action])
            text = f"{key_name.upper()}"
            text_surface = self.sfont.render(text, True, ORANGE)
            text_shadow = self.sfont.render(text, True, BLACK)

            text_width, text_height = text_surface.get_size()
            self.screen.blit(text_shadow, (rect.x + (rect.width - text_width) //
                             2, rect.y + (rect.height - text_height) // 2))
            self.screen.blit(text_surface, (rect.x + (rect.width - text_width) //
                             2 - 5, rect.y + (rect.height - text_height) // 2-3))

    def handle_settings_events(self, event):
        if self.close_button.is_clicked(event):
            self.show_settings = False
        elif event.type == pygame.MOUSEBUTTONDOWN and self.slider_handle_rect.collidepoint(event.pos):
            self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.adjust_volume(event.pos[0])
        elif event.type == pygame.KEYDOWN:
            for action, rect in self.key_buttons.items():
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.key_mappings[action] = event.key

    def adjust_volume(self, mouse_x):
        x_pos = max(self.slider_rect.x, min(
            mouse_x, self.slider_rect.x + self.slider_rect.width))
        self.slider_handle_rect.x = x_pos - 10
        self.volume_value = (x_pos - self.slider_rect.x) / \
            self.slider_rect.width

# Button class


class Button:
    def __init__(self, text, x, y, width, height, color, text_color=WHITE):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_width, text_height = text_surface.get_size()
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_width) //
                    2, self.rect.y + (self.rect.height - text_height) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Main game class
# class Game:
#     def __init__(self):
#         self.sfont = SFONT
#         self.bfont = BFONT
#         self.settings_button = Button("Settings", 10, 10, 180, 50, DARK_GRAY, CYAN)
#         self.close_button = Button("Close", SCREEN_WIDTH -200, 50, 150, 50, BRIGHT_RED, WHITE)
#         self.show_settings = False
#         self.volume_value = 0.5  # Initialize volume control
#         self.is_dragging = False  # Initialize is_dragging
#         self.init_settings()

#     def init_settings(self):
#         # Slider for volume control
#         self.slider_rect = pygame.Rect(SCREEN_WIDTH // 3  , 150, 600, 20)
#         self.slider_handle_rect = pygame.Rect(
#             self.slider_rect.x + self.slider_rect.width * self.volume_value - 10, self.slider_rect.y - 5, 20, 30)

#         # Key bindings setup
#         self.key_buttons = {}
#         self.key_mappings = {}
#         actions = ["Action 1", "Action 2", "Action 3", "RUNN", "Action 5", "Action 6", "Action 7"]
#         default_keys = ['s', 'd', 'f', 'space', 'j', 'k', 'l']

#         # Calculate positions for symmetry
#         left_column_x = SCREEN_WIDTH // 4
#         right_column_x = 3 * SCREEN_WIDTH // 4
#         start_y = 300
#         gap_y = 70

#         positions = [
#             (left_column_x, start_y),
#             (left_column_x, start_y + gap_y),
#             (left_column_x, start_y + 2 * gap_y),
#             (SCREEN_WIDTH // 2 +120, start_y + 3.5 * gap_y),  # Space button centered and lower
#             (right_column_x, start_y),
#             (right_column_x, start_y + gap_y),
#             (right_column_x, start_y + 2 * gap_y)
#         ]

#         for i, action in enumerate(actions):
#             key = pygame.key.key_code(default_keys[i])
#             rect = pygame.Rect(positions[i][0] - 100, positions[i][1], 200, 50)
#             self.key_buttons[action] = rect
#             self.key_mappings[action] = key

#     def run(self):
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 elif self.show_settings:
#                     self.handle_settings_events(event)
#                 elif self.settings_button.is_clicked(event):
#                     self.show_settings = True

#             screen.fill(BLACK)
#             if self.show_settings:
#                 self.draw_settings()
#             else:
#                 self.settings_button.draw(screen, self.sfont)

#             pygame.display.flip()

#     def handle_settings_events(self, event):
#         if self.close_button.is_clicked(event):
#             self.show_settings = False
#         elif event.type == pygame.MOUSEBUTTONDOWN and self.slider_handle_rect.collidepoint(event.pos):
#             self.is_dragging = True
#         elif event.type == pygame.MOUSEBUTTONUP:
#             self.is_dragging = False
#         elif event.type == pygame.MOUSEMOTION and self.is_dragging:
#             self.adjust_volume(event.pos[0])
#         elif event.type == pygame.KEYDOWN:
#             for action, rect in self.key_buttons.items():
#                 if rect.collidepoint(pygame.mouse.get_pos()):
#                     self.key_mappings[action] = event.key

#     def adjust_volume(self, mouse_x):
#         x_pos = max(self.slider_rect.x, min(mouse_x, self.slider_rect.x + self.slider_rect.width))
#         self.slider_handle_rect.x = x_pos - 10
#         self.volume_value = (x_pos - self.slider_rect.x) / self.slider_rect.width

#     def draw_settings(self):
#         xoffset = 5
#         yoffset = 3
#         # Draw a settings background
#         pygame.draw.rect(screen, DARK_GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
#         # Draw close button
#         self.close_button.draw(screen, self.sfont)
#         # Draw volume slider and percentage
#         pygame.draw.rect(screen, LIGHT_GRAY, self.slider_rect)
#         pygame.draw.rect(screen, LIGHT_ORANGE, self.slider_handle_rect)
#         volume_text = "Volume "
#         screen.blit(self.sfont.render(volume_text, True, ORANGE), (SCREEN_WIDTH//4-70 , self.slider_rect.y-15))

#         #JAB
#         Jab = self.bfont.render("JAB", True, LIGHT_ORANGE)
#         Jabw,Jabh = Jab.get_size()
#         screen.blit(self.bfont.render("JAB", True, BLACK),( SCREEN_WIDTH//2-Jabw//2 +xoffset, 300-15+2+yoffset))
#         screen.blit(Jab,( SCREEN_WIDTH//2-Jabw//2 , 300-15))

#         #KICK
#         Kick = self.bfont.render("KICK", True, LIGHT_ORANGE)
#         Kickw,Kickh = Kick.get_size()
#         screen.blit(self.bfont.render("KICK", True, BLACK),( SCREEN_WIDTH//2-Kickw//2 +xoffset, 300-15+70+2+yoffset))
#         screen.blit(Kick,( SCREEN_WIDTH//2-Kickw//2 , 300-15+70))

#         #SWEEP
#         Sweep = self.bfont.render("SWEEP", True, LIGHT_ORANGE)
#         Sweepw,Kickh = Sweep.get_size()
#         screen.blit(self.bfont.render("SWEEP", True, BLACK),( SCREEN_WIDTH//2-Sweepw//2 +xoffset, 300-15+70+70+2+yoffset))
#         screen.blit(Sweep,( SCREEN_WIDTH//2-Sweepw//2 , 300-15+70+70))

#         #RUN
#         Run = self.bfont.render("RUN", True, LIGHT_ORANGE)
#         Runw,Runh = Run.get_size()
#         screen.blit(self.bfont.render("RUN", True, BLACK),( SCREEN_WIDTH//2-1.2*Runw +xoffset, 300-15+70+70+70*1.5+2+yoffset))
#         screen.blit(Run,( SCREEN_WIDTH//2-1.2*Runw , 300-15+70+70+70*1.5))

#         #Left
#         Left = self.bfont.render("Left", True, LIGHT_ORANGE)
#         Leftw,Lefth = Run.get_size()
#         screen.blit(self.bfont.render("Left", True, BLACK),( (SCREEN_WIDTH // 4 - Leftw//2 -20)+xoffset, 230+yoffset))
#         screen.blit(Left,( SCREEN_WIDTH // 4 -Leftw//2-20, 230))

#         #RIGHT
#         RIGHT = self.bfont.render("Right", True, LIGHT_ORANGE)
#         RIGHTw,Lefth = RIGHT.get_size()
#         screen.blit(self.bfont.render("RIGHT", True, BLACK),( (3*SCREEN_WIDTH // 4 - RIGHTw//2 )+xoffset, 230+yoffset))
#         screen.blit(RIGHT,( 3*SCREEN_WIDTH // 4 -RIGHTw//2, 230))


#         # Draw key mapping buttons
#         for action, rect in self.key_buttons.items():
#             pygame.draw.rect(screen, LIGHT_GRAY, rect,5)
#             key_name = pygame.key.name(self.key_mappings[action])
#             text = f"{key_name.upper()}"
#             text_surface = self.sfont.render(text, True, ORANGE)
#             text_shadow = self.sfont.render(text, True, BLACK)

#             text_width, text_height = text_surface.get_size()
#             screen.blit(text_shadow , (rect.x + (rect.width - text_width) // 2, rect.y + (rect.height - text_height) // 2))
#             screen.blit(text_surface , (rect.x + (rect.width - text_width) // 2 -5, rect.y + (rect.height - text_height) // 2-3))

# # Main
# if __name__ == "__main__":
#     game = Game()
#     game.run()
#     pygame.quit()
