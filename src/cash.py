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
    def __init__(self, initial_buying_dice_cash=100):
        self.buying_dice_cash = initial_buying_dice_cash
        self.color = Color.BLACK

    def upgrade(self, amount):
        self.buying_dice_cash += amount

    def get_cost(self):
        return self.buying_dice_cash
        
    def reset(self):
        self.buying_dice_cash = 100
   
    def upgradable_colors_status(self, cash):
        if cash < self.buying_dice_cash:
            self.color = Color.GRAY
        else:
            self.color = Color.BLACK        

    def draw(self, screen):
        buying_dice_cash_text = get_font().render("Cost$: " + str(self.buying_dice_cash), True, self.color)
        screen.blit(buying_dice_cash_text, (210, 390))
        
class UpgradeDiceCashManager:
    def __init__(self, initial_upgrade_dice_cash = [100, 100, 100, 100, 100]):
        self.upgrade_dice_cash = [initial_upgrade_dice_cash[i] for i in range(5)]
        self.colors = [Color.BLACK, Color.BLACK, Color.BLACK, Color.BLACK, Color.BLACK]

    def upgrade(self, dice_index, amount):
        self.upgrade_dice_cash[dice_index] += amount

    def get_cost(self, dice_index):
        return self.upgrade_dice_cash[dice_index]
        
    def reset(self):
        self.upgrade_dice_cash = [100, 100, 100, 100, 100]
    
    def upgradable_colors_status(self, cash):
        for i in range(5):
            if cash < self.upgrade_dice_cash[i]:
                self.colors[i] = Color.GRAY
            else:
                self.colors[i] = Color.BLACK
    
    def draw(self, screen):
        for i in range(5):
            upgrade_dice_cash_text = get_font().render(str(self.upgrade_dice_cash[i]), True, self.colors[i])
            screen.blit(upgrade_dice_cash_text, (83 + i*76, 470))
            

