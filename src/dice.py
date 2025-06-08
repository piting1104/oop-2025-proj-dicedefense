import pygame
from pygame.math import Vector2
from src.constants import *
from src.utils import *
from src.font_manager import get_font

# relative, normalized
x = 0.6
dice_dots_pos = [
	[(0, 0)],
	[(-x, x), (x, -x)],
	[(-x, x), (0, 0), (x, -x)],
	[(x, x), (-x, -x), (x, -x), (-x, x)],
	[(x, x), (-x, -x), (x, -x), (-x, x), (0, 0)],
	[(x, x), (-x, -x), (x, -x), (-x, x), (x, 0), (-x, 0)]
]

class Dice:
	def __init__(self, i, j, color, points: int):
		self.origin = Vector2(GRID_POS + j * (CELL_SIZE + GAP) + CELL_SIZE / 2, GRID_POS + i * (CELL_SIZE + GAP) + CELL_SIZE / 2)
		self.rect = pygame.Rect(GRID_POS + j * (CELL_SIZE + GAP), GRID_POS + i * (CELL_SIZE + GAP), CELL_SIZE, CELL_SIZE)
		self.color = color
		self.points = points

	def draw(self, screen):
		pygame.draw.rect(screen, lighten(self.color, 0.6), self.rect, 0, 5) # fill
		pygame.draw.rect(screen, self.color, self.rect, 2, 5) # border
		for pos in dice_dots_pos[self.points - 1]:
			pygame.draw.circle(screen, self.color, self.origin + Vector2(pos) * CELL_SIZE / 2, 4)

class CollectionDice:
	def __init__(self, x, y, size, color, level):
		self.x = x
		self.y = y
		self.size = size
		self.rect = pygame.Rect(x - size / 2, y - size / 2, size, size)
		self.color = color
		self.level = level

	def draw(self, screen, mouse_pos):
		f = 0.1 if self.is_mouse_on(mouse_pos) else 0
		pygame.draw.rect(screen, darken(lighten(self.color, 0.7), f), self.rect, 0, 8) # fill
		pygame.draw.rect(screen, darken(self.color, f), self.rect, 2, 8) # border
		lvl_text = get_font().render("Lv." + str(self.level), True, self.color)
		screen.blit(lvl_text, (self.x - lvl_text.get_width() / 2, self.y - lvl_text.get_height() / 2))
	
	def is_mouse_on(self, mouse_pos):
		return self.rect.collidepoint(mouse_pos)