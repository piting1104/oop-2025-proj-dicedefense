from src.utils import *
import json

class CustomDice:
	def __init__(self, basic_atk, basic_atk_speed):
		self.basic_atk = basic_atk
		self.basic_atk_speed = basic_atk_speed
		self.level = 1
	
	def upgrade(self):
		self.level += 1

def get_dice_collection() -> list[CustomDice]:
	js = json.load(open("src/dice_collection.json", "r"))
	collection = []
	for i in range(5):
		dice_json = js[f"dice{i+1}"]
		collection.append(CustomDice(dice_json["basic_atk"], dice_json["basic_atk_speed"]))
	
	return collection