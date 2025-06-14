import json
from collections import namedtuple
from queue import Queue
from src.enemy import Enemy
from src.utils import LEFT_DOWN

EnemySet = namedtuple("EnemySet", ["hp", "amount"])
Wave = list[EnemySet]
StageBoss = namedtuple("StageBoss", ["hp"])

class Stage:
	def __init__(self, id: int, waves: list[Wave], boss: StageBoss):
		self.id = id
		self.waves = waves
		self.boss = boss

def get_stages() -> list[Stage]:
	stage_json_list = json.load(open("src/resources/stages.json", "r"))
	stages = []
	for stage_json in stage_json_list:
		id = stage_json["level_id"]
		waves = []
		for wave_js in stage_json["waves"]:
			waves.append(list(map(lambda js: EnemySet(js["hp"], js["amount"]), wave_js)))
		boss = StageBoss(stage_json["boss"]["hp"])
		stages.append(Stage(id, waves, boss))

	return stages

def add_enemies_to_queue(wave: Wave, q: Queue):
	for es in wave:
		for i in range(es.amount):
			q.put(es.hp)

def add_boss_to_queue(boss: StageBoss, q: Queue):
	q.put(boss.hp)

class StageManager:
	def __init__(self, stages: list[Stage]):
		self.stages = stages
		self.current_stage = 0
		self.current_wave = 0
		self.enemy_queue = Queue()
		add_enemies_to_queue(stages[0].waves[0], self.enemy_queue)
		self.clock = 0
		self.is_boss_wave = False
	
	def clocking(self):
		self.clock += 1
	
	def reset_clock(self):
		self.clock = 0
	
	def next_stage(self):
		if self.current_stage == len(self.stages) - 1:
			print("All stages clear!")
			return "stage_clear"

		self.current_stage += 1
		self.current_wave = 0
		self.enemy_queue = Queue()
		add_enemies_to_queue(self.stages[self.current_stage].waves[0], self.enemy_queue)
		self.reset_clock()
		self.is_boss_wave = False
	
	def next_wave(self):
		if self.current_wave == len(self.stages[self.current_stage].waves) - 1:
			self.next_boss()
			return
		
		self.current_wave += 1
		add_enemies_to_queue(
			self.stages[self.current_stage].waves[self.current_wave],
			self.enemy_queue
		)

		self.reset_clock()
	
	def next_boss(self):
		add_boss_to_queue(self.stages[self.current_stage].boss, self.enemy_queue)
		self.is_boss_wave = True
	
	def periodic_generate_enemies(self, enemies):
		if not self.enemy_queue.empty() and self.clock % 20 == 0:
			enemies.append(Enemy(LEFT_DOWN, self.enemy_queue.get()))
		
		if self.enemy_queue.empty() and len(enemies) == 0:
			if self.is_boss_wave:
				if self.next_stage() == "stage_clear":
					return "stage_clear"
			else:
				self.next_wave()
		
		self.clocking()