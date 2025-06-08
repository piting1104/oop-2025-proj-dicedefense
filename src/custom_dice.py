from src.utils import *
import json

color_dict = {
	"red": Color.RED,
	"blue": Color.BLUE,
	"orange": Color.ORANGE,
	"green": Color.GREEN,
	"purple": Color.PURPLE
}

class CustomDice:
	def __init__(self, color, basic_atk, basic_atk_speed):
		self.color = color
		self.basic_atk = basic_atk
		self.basic_atk_speed = basic_atk_speed
		self.level = 1
	
	def from_json(json):
		return CustomDice(color_dict[json["color"]], json["basic_atk"], json["basic_atk_speed"])
	
	def upgrade(self):
		self.level += 1

def get_dice_collection() -> list[CustomDice]:
	json_list = json.load(open("src/dice_collection.json", "r"))
	collection = []
	for j in json_list:
		collection.append(CustomDice.from_json(j))
	
	return collection