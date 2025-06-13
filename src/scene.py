# from src.utils import Color, lighten
# from src.button import *
# from src.constants import *
# from src import font_manager
# from src.cash import *
# from src.stage import *

# import sys, random
# import pygame

# def menu(screen, best_score):
#     start_button = CircleButton((WIDTH / 2, 360), 50, "Start")
#     while True:
#         screen.fill(Color.WHITE)
#         menu_text = get_font().render("Menu" , True, Color.BLACK)
#         screen.blit(menu_text, (HEIGHT/2, WIDTH/2))
#         start_button.draw(screen, pygame.mouse.get_pos())
#         pygame.display.flip()

#         # for event in pygame.event.get():
#             # if event.type == pygame.QUIT:
#             #     pygame.quit()
#             #     sys.exit()
#             # elif event.type == pygame.MOUSEBUTTONDOWN:
#             #     if start_button.is_mouse_on(pygame.mouse.get_pos()):
#             #         return
#         pygame.display.flip()
#         pygame.time.delay(40)

# def game_over(screen, score):
#     clock = pygame.time.Clock()
#     timer = 0
#     while timer < 120:
#         screen.fill(Color.WHITE)
#         draw_text_centered(screen, "GAME OVER", 200, 50, Color.RED)
#         draw_text_centered(screen, f"Score: {score}", 280, 30, Color.WHITE)
#         pygame.display.flip()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#         timer += 1
#         clock.tick(60)
