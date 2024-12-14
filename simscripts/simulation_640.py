
# Claim: Inside the body, falciparum parasites reproduce asexually.
# The simulation will model the asexual reproduction of Plasmodium falciparum parasites.

from simulation_utils import GameObject, Container

class FalciparumParasite(GameObject):
    def __init__(self, name, reproduction_stage=0):
        super().__init__(name)
        self.reproduction_stage = reproduction_stage  # 0: not reproducing, 1: reproducing asexually

    def tick(self):
        if self.reproduction_stage == 1:
            # Simulate asexual reproduction
            new_parasite = FalciparumParasite(f"{self.name}_offspring")
            self.parent.addObject(new_parasite)

    def makeDescriptionStr(self):
        return f"A {self.name} at reproduction stage {self.reproduction_stage}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "body")
        self.parasite = FalciparumParasite("Plasmodium_falciparum")
        self.addObject(self.parasite)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += self.parasite.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        world.parasite.reproduction_stage = 1  # Set the parasite to reproduce asexually
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"], "reproduce": ["reproduce"]}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "reproduce":
            self.rootObject.parasite.tick()  # Simulate reproduction
            self.observationStr = "The parasite reproduces asexually."

        # Do one tick of the environment
        self.doWorldTick()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "reproduce", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
