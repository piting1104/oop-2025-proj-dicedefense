from src.utils import *
from src.font_manager import get_font


class CashManager:
    def __init__(self, initial_cash=100):
        self.cash = initial_cash

    def gain(self, amount):
        self.cash += amount

    def spend(self, amount):
        if self.cash >= amount:
            self.cash -= amount
            return True
        return False

    def get_cash(self):
        return self.cash
        
    def reset(self):
        self.cash = self.initial_cash

    def draw(self, screen):
        cash_text = get_font().render("$: " + str(self.cash), True, Color.BLACK)
        screen.blit(cash_text, (100, 340))