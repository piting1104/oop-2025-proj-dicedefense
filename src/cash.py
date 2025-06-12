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
        cash_text = get_font().render("Current$: " + str(self.cash), True, Color.BLACK)
        screen.blit(cash_text, (80, 340))
        
class BuyingDiceCashManager:
    def __init__(self, initial_buying_dice_cash=10):
        self.buying_dice_cash = initial_buying_dice_cash

    def upgrade(self, amount):
        self.buying_dice_cash += amount

    def get_cost(self):
        return self.buying_dice_cash
        
    def reset(self):
        self.buying_dice_cash = 10

    def draw(self, screen):
        buying_dice_cash_text = get_font().render("Cost$: " + str(self.buying_dice_cash), True, Color.BLACK)
        screen.blit(buying_dice_cash_text, (210, 390))