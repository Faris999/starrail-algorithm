from mcts import mcts
from copy import deepcopy
from simulation import *
import random


state = State(
    entities={
        "stelle": Entity("stelle", 100, 40, "player"),
        "march 7th": Entity("march 7th", 50, 30, "player"),
        "enemy1": Entity("enemy1", 200, 5, "enemy"),
        "enemy2": Entity("enemy2", 50, 50, "enemy"),
    },
    turns=["stelle", "march 7th", "enemy1", "enemy2"],
)
print(state)
mcts = mcts(timeLimit=1000)

while True:
    if state.entities[state.turns[0]].type == "enemy":
        print("random")
        bestAction = random.choice(state.getPossibleActions())
    else:
        print("searching")
        bestAction = mcts.search(state)
    print(bestAction)
    state = state.takeAction(bestAction)
    print(state)
    if state.isTerminal():
        break
