import pygame
from src.constants import *
from src import font_manager
from src.game import Game
from src.scene import Scene

def main():
	pygame.init()
	print("程式啟動中...")

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Dice Defense")
	font_manager.init_fonts()
	
	state = "menu"
	highest_stage = 0
	game = Game(screen)
	scene = Scene(screen)
 
	while True:
		if state == "menu":
			if scene.menu(highest_stage):
				state = "gaming"
		
		elif state == "gaming":
			if game.run() == "game_over":
				state = "game_over"
				if(highest_stage < game.get_stage() - 1):
					highest_stage = game.get_stage() - 1
     
			elif game.run() == "stage_clear":  
				state = "stage_clear"
		
		elif state == "game_over":
			scene.game_over()
			state = "menu"
			pygame.time.delay(3000)
			game.reset()
   
		elif state == "stage_clear":
			scene.stage_clear()
			state = "menu"
			highest_stage = game.get_stage()
			pygame.time.delay(4000)
			game.reset()
	
if __name__ == "__main__":
    main()