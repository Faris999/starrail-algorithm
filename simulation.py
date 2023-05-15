import random
from copy import deepcopy


class Entity:
    def __init__(self, name, hp, atk, type):
        self.name = name
        self.hp = hp
        self.atk = atk
        # self.skill_dmg = skill_dmg
        self.type = type

    def __str__(self) -> str:
        return f"{self.name}, hp: {self.hp}"

    def __repr__(self) -> str:
        return str(self)


class State:
    def __init__(self, entities, turns):
        self.entities = entities
        self.turns = turns
        self.num_turns = 0
        self.skill_points = 3

    def current_turn(self):
        return self.entities[self.turns[0]]

    def getPossibleActions(self):
        attacker = self.entities[self.turns[0]]
        targets = [
            i for i in self.entities.keys() if self.entities[i].type != attacker.type
        ]

        types = ['basic atk', 'skill']
        if self.skill_points <= 0 or attacker.type == 'enemy':
            types = ['basic atk']
            
        

        return [Action(attacker, type, target) for type in types for target in targets]

    def takeAction(self, action):
        new_state = deepcopy(self)
        attacker = action.attacker
        type = action.type
        target = action.target
        new_state.turns = new_state.turns[1:] + [new_state.turns[0]]
        new_state.num_turns += 1
        
        
        if type == 'basic atk':
            new_state.entities[target].hp -= attacker.atk
            if attacker.type == 'player':
                new_state.skill_points = min(5, self.skill_points + 1)
        elif type == 'skill':
            new_state.entities[target].hp -= attacker.atk * 2
            if attacker.type == 'player':
                new_state.skill_points = max(0, self.skill_points - 1)

        if new_state.entities[target].hp <= 0:
            del new_state.entities[target]
            new_state.turns.remove(target)
        return new_state

    def isTerminal(self):
        players_hp_cond = [
            entity.hp <= 0
            for key, entity in self.entities.items()
            if entity.type == "player"
        ]
        enemies_hp_cond = [
            entity.hp <= 0
            for key, entity in self.entities.items()
            if entity.type == "enemy"
        ]

        return all(players_hp_cond) or all(enemies_hp_cond)

    def getReward(self):
        enemies_hp_cond = [
            entity.hp <= 0
            for key, entity in self.entities.items()
            if entity.type == "enemy"
        ]
        if not all(enemies_hp_cond):
            return -9999999

        hp_left = sum(
            [
                entity.hp
                for key, entity in self.entities.items()
                if entity.type == "player"
            ]
        )
        chars_alive = sum(
            1 for key, entity in self.entities.items() if entity.type == "player"
        )

        return hp_left + 10 * chars_alive - self.num_turns + 100 * self.skill_points

    def __str__(self) -> str:
        return f"turn: {self.turns[0]}, skill points: {self.skill_points}, {self.entities}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, State):
            return False
        return self.entities == __value.entities and self.turns == __value.turns


class Action:
    def __init__(self, attacker, type, target):
        self.attacker = attacker
        self.type = type
        self.target = target

    def __str__(self) -> str:
        return f"Attacker: {self.attacker.name}, Type: {self.type} Target: {self.target}"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Action):
            return False
        return (
            __value.attacker.name == self.attacker.name
            and self.target == __value.target
            and self.type == __value.type
        )


def main():
    current_state = State(
        entities={
            "stelle": Entity("stelle", 100, 40, "player"),
            "march 7th": Entity("march 7th", 50, 30, "player"),
            "enemy1": Entity("enemy1", 200, 5, "enemy"),
            "enemy2": Entity("enemy2", 50, 50, "enemy"),
        },
        turns=["stelle", "march 7th", "enemy1", "enemy2"],
    )

    while True:
        print(current_state)

        if current_state.isTerminal():
            print('Battle over')
            break
        
        if current_state.current_turn().type == 'player':
            print('Select action: ')
            for i, action in enumerate(current_state.getPossibleActions()):
                print(f'{i+1}. {action}')
            action = current_state.getPossibleActions()[int(input('> ')) - 1]
            current_state = current_state.takeAction(action)
        elif current_state.current_turn().type == 'enemy':
            action = random.choice(current_state.getPossibleActions())
            current_state = current_state.takeAction(action)
            print(action)

        

if __name__ == "__main__":
    main()
