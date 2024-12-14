
# Claim: Aggravated inflammation is dependent on NLRP3 inflammasome activation.
# The simulation will model the relationship between NLRP3 inflammasome activation and inflammation levels.

from simulation_utils import GameObject, Container

class Inflammasome(GameObject):
    def __init__(self, name, activated=False):
        super().__init__(name)
        self.activated = activated

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

class Inflammation(GameObject):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.level = level

    def increase(self):
        self.level += 1

    def decrease(self):
        self.level -= 1

class Macrophage(GameObject):
    def __init__(self, name, inflammasome):
        super().__init__(name)
        self.inflammasome = inflammasome

    def respond_to_crystals(self):
        if self.inflammasome.activated:
            return True
        return False

class World(Container):
    def __init__(self):
        super().__init__("inflammation environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        inflammasome = Inflammasome("NLRP3 Inflammasome")
        inflammation = Inflammation("Inflammation Level")
        macrophage = Macrophage("Macrophage", inflammasome)

        world.addObject(inflammasome)
        world.addObject(inflammation)
        world.addObject(macrophage)

        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "activate inflammasome": ["activate"],
            "deactivate inflammasome": ["deactivate"],
            "increase inflammation": ["increase"],
            "decrease inflammation": ["decrease"],
            "check inflammation level": ["check"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "activate":
            self.rootObject.contains[0].activate()  # Activate NLRP3 inflammasome
            self.rootObject.contains[1].increase()   # Increase inflammation level
            self.observationStr = "NLRP3 inflammasome activated. Inflammation level increased."
        elif action[0] == "deactivate":
            self.rootObject.contains[0].deactivate()  # Deactivate NLRP3 inflammasome
            self.rootObject.contains[1].decrease()     # Decrease inflammation level
            self.observationStr = "NLRP3 inflammasome deactivated. Inflammation level decreased."
        elif action[0] == "increase":
            self.rootObject.contains[1].increase()
            self.observationStr = "Inflammation level increased."
        elif action[0] == "decrease":
            self.rootObject.contains[1].decrease()
            self.observationStr = "Inflammation level decreased."
        elif action[0] == "check":
            inflammasome_status = "activated" if self.rootObject.contains[0].activated else "deactivated"
            inflammation_level = self.rootObject.contains[1].level
            self.observationStr = f"NLRP3 inflammasome is {inflammasome_status}. Inflammation level is {inflammation_level}."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["activate inflammasome", "check inflammation level", "deactivate inflammasome", "check inflammation level"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
