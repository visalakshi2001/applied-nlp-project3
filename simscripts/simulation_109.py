
# Claim: An M2-like phenotype in brown adipose tissue macrophages is quickly induced by cold exposure.
# The simulation will model the effect of cold exposure on macrophages in brown adipose tissue.

from simulation_utils import GameObject, Container

class Macrophage(GameObject):
    def __init__(self, name, activation_state="M0"):
        super().__init__(name)
        self.activation_state = activation_state  # M0 (resting), M2 (activated)

    def tick(self):
        if self.activation_state == "M0":
            self.activation_state = "M2"  # Rapidly induced to M2-like phenotype

    def makeDescriptionStr(self):
        return f"A {self.name} macrophage, currently in {self.activation_state} state."

class BrownAdiposeTissue(Container):
    def __init__(self):
        super().__init__("Brown Adipose Tissue")

class ColdExposure(GameObject):
    def __init__(self):
        super().__init__("Cold Exposure")

    def induceActivation(self, macrophages):
        for macrophage in macrophages:
            macrophage.activation_state = "M2"  # Induce M2-like phenotype

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        brown_adipose_tissue = BrownAdiposeTissue()
        macrophage1 = Macrophage("macrophage_1")
        macrophage2 = Macrophage("macrophage_2")
        cold_exposure = ColdExposure()

        brown_adipose_tissue.addObject(macrophage1)
        brown_adipose_tissue.addObject(macrophage2)
        world.addObject(brown_adipose_tissue)
        world.addObject(cold_exposure)

        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("induce M2 activation", ["induce", allObjects["macrophage_1"][0], allObjects["macrophage_2"][0]])

    def actionInduceActivation(self, macrophages):
        for macrophage in macrophages:
            macrophage.tick()  # Simulate the activation
        return "M2-like phenotype induced in macrophages."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "induce":
            self.observationStr = self.actionInduceActivation(action[1:])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "induce M2 activation"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
