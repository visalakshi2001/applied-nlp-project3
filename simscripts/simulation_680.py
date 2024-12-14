
# Claim: Lack of FGF21 in mice increases life expectancy.
# The simulation will model the effects of FGF21 deficiency on life expectancy in mice.

from simulation_utils import GameObject, Container

class Mouse(GameObject):
    def __init__(self, name, fgf21_present=True):
        super().__init__(name)
        self.fgf21_present = fgf21_present
        self.lifespan = 100  # Default lifespan in days

    def tick(self):
        if not self.fgf21_present:
            self.lifespan -= 10  # Decrease lifespan due to FGF21 deficiency

    def makeDescriptionStr(self):
        return f"A mouse named {self.name} with FGF21 present: {self.fgf21_present}. Current lifespan: {self.lifespan} days."

class World(Container):
    def __init__(self):
        super().__init__("environment")

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
        mouse_with_fgf21 = Mouse("Mouse_with_FGF21", fgf21_present=True)
        mouse_without_fgf21 = Mouse("Mouse_without_FGF21", fgf21_present=False)
        world.addObject(mouse_with_fgf21)
        world.addObject(mouse_without_fgf21)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Simulate for a few ticks to observe the effects
    for _ in range(5):
        print(simulation.step("look"))
        print()

if __name__ == "__main__":
    main()
