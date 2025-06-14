import pygame

TEXT_FONT = None
TITLE_FONT = None
H2_FONT = None

def init_fonts():
    global TEXT_FONT, TITLE_FONT, H2_FONT
    TEXT_FONT = pygame.font.SysFont(None, 24)
    TITLE_FONT = pygame.font.SysFont(None, 70)
    H2_FONT = pygame.font.SysFont(None, 40)

def check_and_return(font):
    if font is None:
        raise RuntimeError("FONT is not initialized")
    return font

def get_font(type = "text"):
    if type == "text":
        return check_and_return(TEXT_FONT)
    if type == "title":
        return check_and_return(TITLE_FONT)
    if type == "h2":
        return check_and_return(H2_FONT)