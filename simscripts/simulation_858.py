
# Claim: Normal expression of RUNX1 causes tumorsuppressing effects.
# The simulation will model the relationship between RUNX1 expression and tumor suppression.

from simulation_utils import GameObject, Container

class RUNX1(GameObject):
    def __init__(self, expression_level=0):
        super().__init__("RUNX1")
        self.expression_level = expression_level
        self.tumor_suppressor_effect = 0

    def tick(self):
        # The higher the expression level, the greater the tumor suppressor effect
        self.tumor_suppressor_effect = self.expression_level * 2  # Arbitrary multiplier for effect

    def makeDescriptionStr(self):
        return f"{self.name} with expression level {self.expression_level} has a tumor suppressor effect of {self.tumor_suppressor_effect}."

class Tumor(GameObject):
    def __init__(self, size=0):
        super().__init__("Tumor")
        self.size = size

    def grow(self, effect):
        # Tumor growth is inversely related to the tumor suppressor effect
        self.size = max(0, self.size - effect)  # Tumor size cannot be negative

    def makeDescriptionStr(self):
        return f"{self.name} with size {self.size}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        runx1 = RUNX1(expression_level=5)  # Normal expression level
        tumor = Tumor(size=10)  # Initial tumor size
        world.addObject(runx1)
        world.addObject(tumor)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("simulate", ["simulate"])

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

        if actionVerb == "simulate":
            runx1 = self.rootObject.containsItemWithName("RUNX1")[0]
            tumor = self.rootObject.containsItemWithName("Tumor")[0]
            runx1.tick()  # Update RUNX1 effects
            tumor.grow(runx1.tumor_suppressor_effect)  # Tumor grows based on RUNX1 effect
            self.observationStr = f"After simulation: {runx1.makeDescriptionStr()} | {tumor.makeDescriptionStr()}"

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    action = "simulate"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

if __name__ == "__main__":
    main()
