import pygame
from src.constants import *
from src.utils import *
from src.font_manager import get_font

class Enemy:
	def __init__(self, x, y, hp):
		self.x = x
		self.y = y
		self.hp = hp

	def draw(self, screen):
		rect = pygame.Rect(self.x - ENEMY_SIZE / 2, self.y - ENEMY_SIZE / 2, ENEMY_SIZE, ENEMY_SIZE)
		pygame.draw.rect(screen, Color.BLACK, rect, 0, 5)
		pygame.draw.rect(screen, Color.GRAY, rect, 2, 5)
		hp_text = get_font().render(str(self.hp), True, Color.WHITE)
		screen.blit(hp_text, (self.x - hp_text.get_width() / 2, self.y - hp_text.get_height() / 2))