from src.utils import Color, lighten
from src.button import *
from src.constants import *
from src.dice import Dice, CollectionDice, TYPE_COLOR
from src.enemy import Enemy
from src.custom_dice import *
from src import font_manager
from src.cash import *
from src.stage import *

import sys, random
import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.my_dices = get_dice_collection()
        self.dice_collection = []

        self.cash = CashManager(1000)
        self.buying_dice_cash = BuyingDiceCashManager(100)
        initial_upgrade_dice_cash = [100, 100, 100, 100, 100]  # initial cash for upgrading dice
        self.upgrade_dice_cash = UpgradeDiceCashManager(initial_upgrade_dice_cash)	

        self.dices_on_grid = []
        self.available_grids = []
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                self.available_grids.append((i, j))

        self.buying_button = CircleButton((WIDTH / 2, 350), 35, "Buy")

        # bullet initialization
        self.bullet_on_screen = []

        # enemy initialization
        self.enemies = []

        # stage initialization
        self.stage = StageManager(stages=get_stages())

        # selected dice initialization
        self.selected_dice = None  
        
    def reset(self):
        self.my_dices = get_dice_collection()
        self.dice_collection = []

        self.cash = CashManager(1000)
        self.buying_dice_cash = BuyingDiceCashManager(100)
        initial_upgrade_dice_cash = [100, 100, 100, 100, 100]  # initial cash for upgrading dice
        self.upgrade_dice_cash = UpgradeDiceCashManager(initial_upgrade_dice_cash)	

        self.dices_on_grid = []
        self.available_grids = []
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                self.available_grids.append((i, j))

        self.buying_button = CircleButton((WIDTH / 2, 350), 35, "Buy")

        # bullet initialization
        self.bullet_on_screen = []

        # enemy initialization
        self.enemies = []

        # stage initialization
        self.stage = StageManager(stages=get_stages())

    def draw_grid(self):
        outside_rect = pygame.Rect(GRID_POS - MARGIN, GRID_POS - MARGIN, CELL_SIZE * GRID_COLS + GAP * (GRID_COLS - 1) + MARGIN * 2, CELL_SIZE * GRID_ROWS + GAP * (GRID_ROWS - 1) + MARGIN * 2)
        pygame.draw.rect(self.screen, Color.GRAY, outside_rect, 2, 5)
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect(GRID_POS + col * (CELL_SIZE + GAP), GRID_POS + row * (CELL_SIZE + GAP), CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, lighten(Color.GRAY, 0.4), rect, 0, 5)

    def draw_moving_line(self):
        pygame.draw.line(self.screen, Color.GRAY, LEFT_TOP, RIGHT_TOP, 2)
        pygame.draw.line(self.screen, Color.GRAY, LEFT_TOP, LEFT_DOWN, 2)
        pygame.draw.line(self.screen, Color.GRAY, RIGHT_TOP, RIGHT_DOWN, 2)

    def draw_dice_collection(self, mouse_pos):
        self.dice_collection.clear()
        rect = pygame.Rect(50, 420, 400, 80)
        pygame.draw.rect(self.screen, lighten(Color.GRAY, 0.3), rect, 0, 5)
        for i, d in enumerate(self.my_dices):
            dice = CollectionDice(250 + (i - 2) * 76, 460, 60, TYPE_COLOR[i], d.level)
            dice.draw(self.screen, mouse_pos)
            self.dice_collection.append(dice)

    def purchase_dice(self):
        if self.cash.get_cash() < self.buying_dice_cash.get_cost():
            print("Not enough cash to buy a dice!")
            return
        if len(self.available_grids) == 0:
            print("No available grids for buying!")
            return
                        
        self.cash.spend(self.buying_dice_cash.get_cost()) # cost of buying a dice
        self.buying_dice_cash.upgrade(50)  # increase the cost for next purchase
    
        grid = random.choice(self.available_grids)
        type = random.choice([i for i in range(5)])
        self.dices_on_grid.append(Dice(grid[0], grid[1], type, 1, self.my_dices[type].basic_atk, self.my_dices[type].basic_atk_speed))
        self.available_grids.remove(grid)

    def upgrade_dice(self, dice_index):
        if self.cash.get_cash() < self.upgrade_dice_cash.get_cost(dice_index):
            print("Not enough cash to upgrade this dice!")
            return
        
        self.cash.spend(self.upgrade_dice_cash.get_cost(dice_index))  # cost of upgrading a dice
        self.upgrade_dice_cash.upgrade(dice_index, 100)  # increase the cost for next upgrade
        self.my_dices[dice_index].upgrade()
        
    def can_merge(self, d1, d2):
        return d1 is not d2 and d1.type == d2.type and d1.points == d2.points

    def merge_dices(self, d1, d2):
        # 保留 d1 的位置，移除 d1 和 d2
        self.dices_on_grid.remove(d1)
        self.dices_on_grid.remove(d2)
        self.available_grids.append((d1.rect.top // (CELL_SIZE + GAP), d1.rect.left // (CELL_SIZE + GAP)))
        self.available_grids.append((d2.rect.top // (CELL_SIZE + GAP), d2.rect.left // (CELL_SIZE + GAP)))

        # 加入新骰子（合併升一級）
        new_points = d1.points + 1
        i = (d1.rect.top - GRID_POS) // (CELL_SIZE + GAP)
        j = (d1.rect.left - GRID_POS) // (CELL_SIZE + GAP)
        self.dices_on_grid.append(Dice(i, j, d1.type, new_points, d1.basic_atk, d1.basic_atk_speed))

        # 只保留合併後骰子的位置為佔用
        self.available_grids.remove((i, j))

    def get_stage(self):
        return self.stage.current_stage + 1

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.buying_button.is_mouse_on(mouse_pos):
                    self.purchase_dice()
                for idx, d in enumerate(self.dice_collection):
                    if d.is_mouse_on(mouse_pos):
                        self.upgrade_dice(idx)
                
                clicked_dice = None
                for dice in self.dices_on_grid:
                    if dice.rect.collidepoint(mouse_pos):
                        clicked_dice = dice
                        break
                
                if clicked_dice:
                    if self.selected_dice is None:
                        self.selected_dice = clicked_dice
                    elif self.selected_dice == clicked_dice:
                        self.selected_dice = None  # Cancel selection
                    elif (self.selected_dice.type == clicked_dice.type and 
                        self.selected_dice.points == clicked_dice.points):
                        
                        if self.selected_dice.points >= MAX_POINTS:
                            print("已達最大合成等級，無法再合成")
                            self.selected_dice = None
                            return "game_continue"  # Cancel merge if max points reached
                        
                        # Merge the two dices
                        new_points = self.selected_dice.points + 1
                        row = (clicked_dice.rect.top - GRID_POS) // (CELL_SIZE + GAP)
                        col = (clicked_dice.rect.left - GRID_POS) // (CELL_SIZE + GAP)
                        new_dice = Dice(row, col, clicked_dice.type, new_points,
                                        clicked_dice.basic_atk, clicked_dice.basic_atk_speed)

                        self.dices_on_grid.remove(self.selected_dice)
                        self.dices_on_grid.remove(clicked_dice)
                        self.dices_on_grid.append(new_dice)

                        # Add the grids of the merged dices back to available grids
                        i = (self.selected_dice.rect.top - GRID_POS) // (CELL_SIZE + GAP)
                        j = (self.selected_dice.rect.left - GRID_POS) // (CELL_SIZE + GAP)
                        if (i, j) not in self.available_grids:
                            self.available_grids.append((i, j))
                        
                        self.available_grids = list(filter(lambda pos: 0 <= pos[0] < GRID_ROWS and 0 <= pos[1] < GRID_COLS, self.available_grids))
                        self.selected_dice = None
                    else:
                        self.selected_dice = None  # Cancel selection if different dice are clicked
        
        self.screen.fill(Color.WHITE)
        self.draw_grid()
        self.draw_moving_line()
        self.draw_dice_collection(mouse_pos)

        self.buying_button.draw(self.screen, mouse_pos)

        levels = list(map(lambda d: d.level, self.dice_collection))
        for dice in self.dices_on_grid:
            dice.periodic_attack(self.bullet_on_screen, self.enemies, levels)
            dice.draw(self.screen)
            
            # 如果這顆是被選到的骰子，就畫黃色邊框
            if self.selected_dice == dice:
                pygame.draw.rect(self.screen, Color.YELLOW, dice.rect, 3, 5)
        
        for bullet in self.bullet_on_screen:
            for enemy in self.enemies:
                if enemy.get_rect().collidepoint(bullet.pos):
                    enemy.damage(bullet.atk)
                    bullet.show == False
                    break
            bullet.move()
            bullet.draw(self.screen)
        
        self.bullet_on_screen = list(filter(lambda b: b.show and in_screen(b.pos), self.bullet_on_screen))

        for enemy in self.enemies:
            state = enemy.move()
            enemy.draw(self.screen)
            
            if state == 0:  # enemy reached the end
                return "game_over"  # game over
            
            # check if enemies are defeated
            if enemy.hp <= 0:
                self.cash.gain(10)

        self.enemies = list(filter(lambda e: e.hp > 0, self.enemies))

        self.cash.draw(self.screen)
        self.buying_dice_cash.upgradable_colors_status(self.cash.get_cash())
        self.buying_dice_cash.draw(self.screen)
        self.upgrade_dice_cash.upgradable_colors_status(self.cash.get_cash())
        self.upgrade_dice_cash.draw(self.screen)
        stages_text = get_font().render("Stage: " + str(self.stage.current_stage + 1) , True, Color.BLUE)
        self.screen.blit(stages_text, (WIDTH/2 - 40, 10))

        # stage generate enemies
        if(self.stage.periodic_generate_enemies(self.enemies) == "stage_clear"):
            return "stage_clear"
    
        pygame.display.flip()
        pygame.time.delay(40)
        
        return "game_continue"  # continue the game
        
