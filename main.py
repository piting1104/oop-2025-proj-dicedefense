from src.utils import Color, lighten
from src.button import *
from src.constants import *
from src.dice import Dice, CollectionDice, TYPE_COLOR
from src.enemy import Enemy
from src.custom_dice import *
from src import font_manager
from src.cash import CashManager

import sys, random
import pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Defense")
font_manager.init_font()

# drawing grid
def draw_grid():
	outside_rect = pygame.Rect(GRID_POS - MARGIN, GRID_POS - MARGIN, CELL_SIZE * GRID_COLS + GAP * (GRID_COLS - 1) + MARGIN * 2, CELL_SIZE * GRID_ROWS + GAP * (GRID_ROWS - 1) + MARGIN * 2)
	pygame.draw.rect(screen, Color.GRAY, outside_rect, 2, 5)
	for row in range(GRID_ROWS):
		for col in range(GRID_COLS):
			rect = pygame.Rect(GRID_POS + col * (CELL_SIZE + GAP), GRID_POS + row * (CELL_SIZE + GAP), CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(screen, lighten(Color.GRAY, 0.4), rect, 0, 5)

def draw_moving_line():
	pygame.draw.line(screen, Color.GRAY, LEFT_TOP, RIGHT_TOP, 2)
	pygame.draw.line(screen, Color.GRAY, LEFT_TOP, LEFT_DOWN, 2)
	pygame.draw.line(screen, Color.GRAY, RIGHT_TOP, RIGHT_DOWN, 2)

# initialize dice collection and drawing
my_dices = get_dice_collection()

dice_collection = []
def draw_dice_collection(mouse_pos):
	dice_collection.clear()
	rect = pygame.Rect(50, 420, 400, 80)
	pygame.draw.rect(screen, lighten(Color.GRAY, 0.3), rect, 0, 5)
	for i, d in enumerate(my_dices):
		dice = CollectionDice(250 + (i - 2) * 76, 460, 60, TYPE_COLOR[i], d.level)
		dice.draw(screen, mouse_pos)
		dice_collection.append(dice)

# cash manager initialization
cash = CashManager(100)

# dice buying initialization
dices_on_grid = []
available_grids = []
for i in range(GRID_ROWS):
	for j in range(GRID_COLS):
		available_grids.append((i, j))

def purchase_dice():
	if cash.get_cash() < 10:
		print("Not enough cash to buy a dice!")
		return
	if len(available_grids) == 0:
		print("No available grids for buying!")
		return
					
	cash.spend(10) # cost of buying a dice
	grid = random.choice(available_grids)
	type = random.choice([i for i in range(5)])
	dices_on_grid.append(Dice(grid[0], grid[1], type, 1, my_dices[type].basic_atk, my_dices[type].basic_atk_speed))
	available_grids.remove(grid)

buying_button = CircleButton((WIDTH / 2, 350), 35, "Buy")

# bullet initialization
bullet_on_screen = []

# enemy initialization
enemies = [
	Enemy(LEFT_DOWN, 2000),
]

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

	levels = list(map(lambda d: d.level, dice_collection))
	for dice in dices_on_grid:
		dice.periodic_attack(bullet_on_screen, enemies, levels)
		dice.draw(screen)
	
	for bullet in bullet_on_screen:
		for enemy in enemies:
			if enemy.get_rect().collidepoint(bullet.pos):
				enemy.damage(bullet.atk)
				bullet.show == False
				break
		bullet.move()
		bullet.draw(screen)
	
	bullet_on_screen = list(filter(lambda b: b.show and in_screen(b.pos), bullet_on_screen))

	for enemy in enemies:
		state = enemy.move()
		enemy.draw(screen)
	
	# check if enemies are defeated
	for enemy in enemies:
		if enemy.hp <= 0:
			cash.gain(10)
	enemies = list(filter(lambda e: e.hp > 0, enemies))

	cash.draw(screen)
 
	pygame.display.flip()
	pygame.time.delay(40)