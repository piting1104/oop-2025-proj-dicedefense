import pygame
from pygame.math import Vector2
from src.constants import *
from src.utils import *
from src.constants import *
from src.font_manager import get_font
from src.game_parameters import *

class Enemy:
	def __init__(self, pos: Vector2, hp: int, moving_speed=1.5, resize=1):
		self.pos = pos.copy()
		self.hp = hp
		self.on_path = 0
		self.moving_speed = moving_speed
		self.resize = resize
	
	def get_rect(self):
		square = Vector2(ENEMY_SIZE, ENEMY_SIZE) * self.resize
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
			if self.pos.y <= LEFT_TOP.y:
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
	
	def damage_by(self, bullet):
		if bullet.show:
			self.hp -= int(bullet.atk)
	
	def money(self):
		return enemy_gain(self.hp)

class Boss(Enemy):
	def __init__(self, pos: Vector2, hp: int):
		super().__init__(pos, hp, moving_speed=1.3, resize=1.2)

class HealerEnemy(Enemy):
    def __init__(self, pos: Vector2, hp: int, healing_amount=10, healing_range=100, healing_cooldown=50):
        super().__init__(pos, hp, moving_speed=1.4, resize=1.0)
        self.healing_amount = healing_amount
        self.healing_range = healing_range
        self.healing_cooldown = healing_cooldown
        self.healing_clock = 0

    def heal_others(self, enemies):
        self.healing_clock += 1
        if self.healing_clock < self.healing_cooldown:
            return
        self.healing_clock = 0

        for enemy in enemies:
            if enemy is not self and (self.pos - enemy.pos).length() <= self.healing_range:
                enemy.hp += self.healing_amount
