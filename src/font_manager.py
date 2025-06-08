import pygame

FONT = None

def init_font(size=24):
    global FONT
    FONT = pygame.font.SysFont(None, size)

def get_font():
    if FONT is None:
        raise RuntimeError("FONT is not initialized")
    return FONT