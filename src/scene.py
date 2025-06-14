from src.utils import Color, lighten
from src.button import *
from src.constants import *
from src.font_manager import *
from src.cash import *
from src.stage import *

import sys, random
import pygame

class Scene:
    def __init__(self, screen):
        self.screen = screen
    
    def menu(self, best_level):
        background = pygame.image.load("src/resources//dice_defense.png")
        background = pygame.transform.scale(background, (621/1.25, 379/1.25)) 
        self.start_button = CircleButton((WIDTH / 2, HEIGHT / 2 - 65), 50, "Start")
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_mouse_on(mouse_pos):
                    return True
        
        self.screen.fill(Color.WHITE)
        self.screen.blit(background, (0, 250))
        menu_text = get_font(type="title").render("Dice Defense" , True, Color.BLACK)
        self.screen.blit(menu_text, (WIDTH/2 - menu_text.get_width() / 2, 60))
        highest_level_text = get_font().render("Highest Stage: " + str(best_level), True, Color.GREEN)
        self.screen.blit(highest_level_text, (WIDTH/2 - highest_level_text.get_width() / 2, HEIGHT/2 + 40))
        self.start_button.draw(self.screen, mouse_pos, font=get_font(type="h2"))
        
        pygame.display.flip()
        pygame.time.delay(40)

    def game_over(self):
        gameover_text = get_font().render("Game Over" , True, Color.RED)
        self.screen.blit(gameover_text, (WIDTH/2 - 40, HEIGHT/3))
        
        pygame.display.flip()
        pygame.time.delay(40)
        
    def stage_clear(self):
        self.screen.fill(Color.WHITE)
        gameover_text = get_font().render("Stage Clear" , True, Color.GREEN)
        self.screen.blit(gameover_text, (WIDTH/2 - 40, HEIGHT/3))
        
        pygame.display.flip()
        pygame.time.delay(40)

