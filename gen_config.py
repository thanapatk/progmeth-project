import pygame
import pickle

KEYBINDING = {
    'punch_r': pygame.K_j,
    'kick_r': pygame.K_k,
    'duck_r': pygame.K_l,
    'run': pygame.K_SPACE,
    'punch_l': pygame.K_f,
    'kick_l': pygame.K_d,
    'duck_l': pygame.K_s
}

VOLUME = 0.5

HIGH_SCORE = 0

with open('config.pkl', 'wb') as f:
    pickle.dump((KEYBINDING, VOLUME, HIGH_SCORE), f)
