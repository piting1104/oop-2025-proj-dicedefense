import pygame
from pygame.math import Vector2

BULLET_SPEED = 30

class Bullet:
	def __init__(self, pos: Vector2, color, direction: Vector2, atk):
		self.pos = pos.copy()
		self.color = color
		self.direction = direction.copy()
		self.atk = atk
		self.show = True
	
	def draw(self, screen):
		if self.show:
			pygame.draw.circle(screen, self.color, self.pos, 4)

	def move(self):
		self.pos += self.direction.normalize() * BULLET_SPEED