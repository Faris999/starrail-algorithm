from mcts import mcts
from copy import deepcopy

class Entity():
  def __init__(self, name, hp, atk, skill_dmg, type):
    self.name = name
    self.hp = hp
    self.atk = atk
    self.skill_dmg = skill_dmg
    self.type = type

  def __str__(self) -> str:
    return f'{self.name}, hp: {self.hp}'
  
  def __repr__(self) -> str:
    return str(self)

class State():
  def __init__(self, entities, turns):
    self.entities = entities
    self.turns = turns
    self.skill_points = 3
    
  def getPossibleActions(self):
    attacker = self.entities[self.turns[0]]
    targets = [i for i in self.entities.keys() if self.entities[i].type != attacker.type]
    
    return [Action(attacker, target) for target in targets]


  def takeAction(self, action):
    new_state = deepcopy(self)
    attacker = action.attacker
    target = action.target
    new_state.entities[target].hp -= attacker.atk
    new_state.turns = new_state.turns[1:] + [new_state.turns[0]]
    
    if new_state.entities[target].hp <= 0:
      del new_state.entities[target]
      new_state.turns.remove(target)  
    return new_state

  def isTerminal(self):
    players_hp_cond = [entity.hp <= 0 for key, entity in self.entities.items() if entity.type == 'player']
    enemies_hp_cond = [entity.hp <= 0 for key, entity in self.entities.items() if entity.type == 'enemy']
    
    return all(players_hp_cond) or all(enemies_hp_cond)

  def getReward(self):
    return 1
  
  def __str__(self) -> str:
    return f'turn: {self.turns[0]}, {self.entities}'

class Action():
  def __init__(self, attacker, target):
    self.attacker = attacker
    self.target = target

  def __str__(self) -> str:
    return f'Attacker: {self.attacker}, Target: {self.target}'
  
  def __repr__(self) -> str:
    return str(self)

  def __hash__(self) -> int:
    return hash((self.attacker, self.target))

state = State(entities={
  'stelle': Entity('stelle', 100, 5, 'player'),
  'march 7th': Entity('march 7th', 50, 20, 'player'),
  'enemy1': Entity('enemy1', 100, 10, 'enemy'),
  'enemy2': Entity('enemy2', 100, 10, 'enemy')
}, turns=['stelle', 'march 7th', 'enemy1', 'enemy2'])
print(state)
mcts = mcts(timeLimit=1000)

while True:
  bestAction = mcts.search(state)
  print(bestAction)
  state = state.takeAction(bestAction)
  print(state)
  if state.isTerminal():
    break