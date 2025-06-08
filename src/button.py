import pygame, math
from src.utils import *
from src.font_manager import get_font

class CircleButton:
	def __init__(self, center, radius, text):
		self.center = center
		self.radius = radius
		self.text = text
	
	def is_mouse_on(self, mouse_pos):
		dx = mouse_pos[0] - self.center[0]
		dy = mouse_pos[1] - self.center[1]
		distance = math.hypot(dx, dy)
		return distance <= self.radius
	
	def draw(self, surface, mouse_pos):
		color = darken(Color.GRAY, 0.1) if self.is_mouse_on(mouse_pos) else Color.GRAY
		pygame.draw.circle(surface, color, self.center, self.radius)
		pygame.draw.circle(surface, Color.BLACK, self.center, self.radius, 2)
		text_surf = get_font().render(self.text, True, Color.BLACK)
		text_rect = text_surf.get_rect(center=self.center)
		surface.blit(text_surf, text_rect)

# class RectButton:
# 	def __init__(self, rect: pygame.Rect, text):
# 		self.rect = rect
# 		self.text = text
	
# 	def is_mouse_on(self, mouse_pos):
# 		return self.rect.collidepoint(mouse_pos)
	
# 	def draw(self, surface, is_hovered):
# 		color = Color.DARK_GRAY if is_hovered else Color.GRAY
# 		pygame.draw.rect(surface, color, self.rect)
# 		pygame.draw.rect(surface, Color.BLACK, self.rect, 2)  # 外框
# 		text_surf = get_font().render(self.text, True, Color.BLACK)
# 		text_rect = text_surf.get_rect(center=self.rect.center)
# 		surface.blit(text_surf, text_rect)