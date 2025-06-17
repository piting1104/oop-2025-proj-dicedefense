import json
from collections import namedtuple
from queue import Queue
from src.enemy import Enemy, Boss, HealerEnemy
from src.utils import LEFT_DOWN

# 先定義資料結構
EnemySet = namedtuple("EnemySet", ["enemy_class", "hp", "amount"])
Wave = list[EnemySet]
StageBoss = namedtuple("StageBoss", ["hp"])

class Stage:
    def __init__(self, id: int, waves: list[Wave], boss: StageBoss):
        self.id = id
        self.waves = waves
        self.boss = boss

# 讀取關卡設定
def get_stages() -> list[Stage]:
    stage_json_list = json.load(open("src/resources/stages.json", "r"))
    enemy_type_map = {
        "Enemy": Enemy,
        "HealerEnemy": HealerEnemy
    }
    stages = []
    for stage_json in stage_json_list:
        id = stage_json["level_id"]
        waves = []
        for wave_js in stage_json["waves"]:
            wave = []
            for js in wave_js:
                enemy_class = enemy_type_map[js["type"]]
                wave.append(EnemySet(enemy_class, js["hp"], js["amount"]))
            waves.append(wave)
        boss = StageBoss(stage_json["boss"]["hp"])
        stages.append(Stage(id, waves, boss))
    return stages

# 將敵人加入 queue
def add_enemies_to_queue(wave: Wave, q: Queue):
    for es in wave:
        for i in range(es.amount):
            q.put((es.enemy_class, es.hp))

# Boss 加入 queue
def add_boss_to_queue(boss: StageBoss, q: Queue):
    q.put(boss)

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
            e = self.enemy_queue.get()
            if isinstance(e, StageBoss):
                enemies.append(Boss(LEFT_DOWN, e.hp))
            else:
                enemy_class, hp = e
                enemies.append(enemy_class(LEFT_DOWN, hp))

        if self.enemy_queue.empty() and len(enemies) == 0:
            if self.is_boss_wave:
                if self.next_stage() == "stage_clear":
                    return "stage_clear"
            else:
                self.next_wave()

        self.clocking()
