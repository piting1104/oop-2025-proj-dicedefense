import pygame
from pygame.math import Vector2
from src.constants import *
from src.utils import *
from src.constants import *
from src.font_manager import get_font

class Enemy:
	def __init__(self, pos: Vector2, hp: int):
		self.pos = pos.copy()
		self.hp = hp
		self.on_path = 0
		self.moving_speed = 2
	
	def get_rect(self):
		square = Vector2(ENEMY_SIZE, ENEMY_SIZE)
		return pygame.Rect(self.pos - square / 2, square)

	def draw(self, screen):
		if self.hp <= 0:
			return

		rect = self.get_rect()
		pygame.draw.rect(screen, Color.BLACK, rect, 0, 5)
		pygame.draw.rect(screen, Color.GRAY, rect, 2, 5)
		hp_text = get_font().render(str(self.hp), True, Color.WHITE)
		screen.blit(hp_text, self.pos - Vector2(hp_text.get_size()) / 2)
		
	def set_speed(self, speed):
		self.moving_speed = speed
	
	def move(self):
		if self.on_path == 0:
			if self.pos.y <= DIST:
				self.on_path = 1
				self.pos.x += self.moving_speed
			else:
				self.pos.y -= self.moving_speed
		
		elif self.on_path == 1:
			if self.pos.x >= RIGHT_TOP.x:
				self.on_path = 2
				self.pos.y += self.moving_speed
			else:
				self.pos.x += self.moving_speed
		
		elif self.on_path == 2:
			if self.pos.y >= RIGHT_DOWN.y:
				return 0
			else:
				self.pos.y += self.moving_speed
		
		return 1
	
	def damage(self, damage):
		self.hp -= int(damage)
