from pygame.math import Vector2
from src.constants import *

class Color:
	WHITE  = (255, 255, 255)
	BLACK  = (0, 0, 0)
	GRAY   = (200, 200, 200)
	DARK_GRAY = (150, 150, 150)
	# dice color
	RED    = (220, 0, 0)
	BLUE   = (0, 0, 220)
	ORANGE = (255, 165, 0)
	GREEN  = (0, 200, 0)
	PURPLE = (220, 0, 220)

def lighten(color, factor: float):
	r, g, b = color
	r = min(int(r + (255 - r) * factor), 255)
	g = min(int(g + (255 - g) * factor), 255)
	b = min(int(b + (255 - b) * factor), 255)
	return (r, g, b)

def darken(color: tuple[int, int, int], factor: float = 0.2) -> tuple[int, int, int]:
	r, g, b = color
	r = max(int(r * (1 - factor)), 0)
	g = max(int(g * (1 - factor)), 0)
	b = max(int(b * (1 - factor)), 0)
	return (r, g, b)

def in_screen(pos: Vector2):
	return 0 <= pos.x <= WIDTH and 0 <= pos.y <= HEIGHT