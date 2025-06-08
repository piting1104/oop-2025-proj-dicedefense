from src.utils import Color, lighten
from src.button import *
from src.constants import *
from src.dice import Dice, CollectionDice
from src.enemy import Enemy
from src.custom_dice import *
from src import font_manager

import sys, random
import pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Defense")
font_manager.init_font()

def draw_grid():
	outside_rect = pygame.Rect(GRID_POS - MARGIN, GRID_POS - MARGIN, CELL_SIZE * GRID_COLS + GAP * (GRID_COLS - 1) + MARGIN * 2, CELL_SIZE * GRID_ROWS + GAP * (GRID_ROWS - 1) + MARGIN * 2)
	pygame.draw.rect(screen, Color.GRAY, outside_rect, 2, 5)
	for row in range(GRID_ROWS):
		for col in range(GRID_COLS):
			rect = pygame.Rect(GRID_POS + col * (CELL_SIZE + GAP), GRID_POS + row * (CELL_SIZE + GAP), CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(screen, lighten(Color.GRAY, 0.4), rect, 0, 5)

def draw_moving_line():
	DIST = (GRID_POS - MARGIN) / 2
	lt_pos = (DIST, DIST)
	rt_pos = (WIDTH - DIST, DIST)
	ld_pos = (DIST, DIST * 2 + CELL_SIZE * 4)
	rd_pos = (WIDTH - DIST, DIST * 2 + CELL_SIZE * 4)
	pygame.draw.line(screen, Color.GRAY, lt_pos, rt_pos, 2)
	pygame.draw.line(screen, Color.GRAY, lt_pos, ld_pos, 2)
	pygame.draw.line(screen, Color.GRAY, rt_pos, rd_pos, 2)

my_dices = get_dice_collection()

dice_collection = []
def draw_dice_collection(mouse_pos):
	dice_collection.clear()
	rect = pygame.Rect(50, 420, 400, 80)
	pygame.draw.rect(screen, lighten(Color.GRAY, 0.3), rect, 0, 5)
	for d, j in list(zip(my_dices, [-2, -1, 0, 1, 2])):
		dice = CollectionDice(250 + j * 76, 460, 60, d.color, d.level)
		dice.draw(screen, mouse_pos)
		dice_collection.append(dice)

clock = pygame.time.Clock()

# TODO: enemies
enemies = [
	Enemy(50, 100, 450),
	Enemy(50, 180, 400),
	Enemy(50, 260, 400),
]
###############

dices_on_grid = []
available_grids = []
for i in range(GRID_ROWS):
	for j in range(GRID_COLS):
		available_grids.append((i, j))

def purchase_dice():
	if len(available_grids) == 0:
		print("No available grids for buying!")
		return
	
	grid = random.choice(available_grids)
	dice = random.choice(my_dices)
	dices_on_grid.append(Dice(grid[0], grid[1], dice.color, 1))
	available_grids.remove(grid)


buying_button = CircleButton((WIDTH / 2, 350), 35, "Buy")

while True:
	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if buying_button.is_mouse_on(mouse_pos):
				purchase_dice()
			for idx, d in enumerate(dice_collection):
				if d.is_mouse_on(mouse_pos):
					my_dices[idx].upgrade()

	
	screen.fill(Color.WHITE)
	draw_grid()
	draw_moving_line()
	draw_dice_collection(mouse_pos)

	buying_button.draw(screen, mouse_pos)

	for dice in dices_on_grid:
		dice.draw(screen)

	for enemy in enemies:
		enemy.draw(screen)

	pygame.display.flip()
	clock.tick(60)