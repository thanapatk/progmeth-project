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

with open('config.pkl', 'wb') as f:
    pickle.dump(KEYBINDING, f)
