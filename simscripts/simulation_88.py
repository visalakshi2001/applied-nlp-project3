
# Claim: Adult tissue-resident macrophages possess a self-renewing capacity.
# The simulation will demonstrate the self-renewing capacity of tissue-resident macrophages.

from simulation_utils import GameObject, Container

class Macrophage(GameObject):
    def __init__(self, name, self_renewing_capacity=0):
        super().__init__(name)
        self.properties = {
            "self_renewing_capacity": self_renewing_capacity
        }

    def tick(self):
        # Simulate self-renewing capacity
        if self.properties["self_renewing_capacity"] > 0:
            self.properties["self_renewing_capacity"] += 1  # Increase capacity over time

    def makeDescriptionStr(self):
        description = f"A {self.name} with a self-renewing capacity of {self.properties['self_renewing_capacity']}."
        return description

class Tissue(Container):
    def __init__(self, name):
        super().__init__(name)

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
        tissue = Tissue("tissue")
        macrophage = Macrophage("tissue-resident macrophage", self_renewing_capacity=1)  # Initial self-renewing capacity
        tissue.addObject(macrophage)
        return tissue

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
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
