# constant parameters
INITIAL_CASH = 1000
INITIAL_DICE_COST = 100
INITIAL_UPGRADE_COST_LIST = [100, 100, 100, 100, 100]

# functions
def enemy_gain(hp: int):
	return max(10, hp // 10)

def dice_bullet_atk_multiplier(level: int, points: int):
	return (1 + level * 0.2) * (1 + (points - 1) * 0.2)

def dice_atk_speed_multiplier(level: int, points: int):
	return (1 + level * 0.05) * (1 + (points - 1) * 0.02)