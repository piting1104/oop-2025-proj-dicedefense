import pygame
from pygame.math import Vector2
from src.constants import *
from src.utils import *
from src.font_manager import get_font
from src.bullet import Bullet
from src.enemy import Enemy

# dice type
TYPE_COLOR = [Color.RED, Color.BLUE, Color.ORANGE, Color.GREEN, Color.PURPLE]

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
	def __init__(self, i, j, type, points: int, basic_atk, basic_atk_speed):
		self.i = i
		self.j = j
		self.origin = Vector2(GRID_POS + j * (CELL_SIZE + GAP) + CELL_SIZE / 2, TOP_PADDING + GRID_POS + i * (CELL_SIZE + GAP) + CELL_SIZE / 2)
		self.rect = pygame.Rect(GRID_POS + j * (CELL_SIZE + GAP), TOP_PADDING + GRID_POS + i * (CELL_SIZE + GAP), CELL_SIZE, CELL_SIZE)
		self.type = type
		self.points = points
		self.basic_atk = basic_atk
		self.basic_atk_speed = basic_atk_speed
		self.clock = 0

	def draw(self, screen):
		color = TYPE_COLOR[self.type]
		pygame.draw.rect(screen, lighten(color, 0.6), self.rect, 0, 5) # fill
		pygame.draw.rect(screen, color, self.rect, 2, 5) # border
		for pos in dice_dots_pos[self.points - 1]:
			pygame.draw.circle(screen, color, self.origin + Vector2(pos) * CELL_SIZE / 2, 4)
	
	def clocking(self):
		self.clock += 1

	def select_enemy(self, enemies: list[Enemy]) -> Enemy:
		return enemies[0]
	
	def get_atk(self, levels: list[int]):
		# Calculate the attack power based on the dice type and points
		point_bonus = 1 + 0.2 * (self.points - 1)
		return self.basic_atk * (1 + levels[self.type] * 0.2) * point_bonus
	
	def get_atk_speed(self, levels: list[int]):
		return self.basic_atk_speed * (1 + levels[self.type] * 0.05)
	
	def periodic_attack(self, bullet_on_screen: list[Bullet], enemies: list[Enemy], levels: list[int]):
		if len(enemies) == 0:
			return
		
		if self.clock >= 8 / self.get_atk_speed(levels):
			for pos in dice_dots_pos[self.points - 1]:
				starting = self.origin + Vector2(pos) * CELL_SIZE / 2
				target = self.select_enemy(enemies).pos
				bullet_on_screen.append(Bullet(starting, TYPE_COLOR[self.type], target - starting, self.get_atk(levels)))
			self.clock = 0
		
		self.clocking()

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