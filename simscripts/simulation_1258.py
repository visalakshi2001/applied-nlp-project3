
# Claim: The recruitment of Wdr5 to its target loci depends on Kat8.
# The simulation will check if Wdr5 recruitment is dependent on Kat8 based on the provided reference text.

from simulation_utils import GameObject, Container

class Wdr5(GameObject):
    def __init__(self, name, recruited=False):
        super().__init__(name)
        self.recruited = recruited

    def recruit(self, kat8_present):
        if kat8_present:
            self.recruited = True
        else:
            self.recruited = False

    def makeDescriptionStr(self):
        return f"{self.name} is {'recruited' if self.recruited else 'not recruited'}."

class Kat8(GameObject):
    def __init__(self, name, active=False):
        super().__init__(name)
        self.active = active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def makeDescriptionStr(self):
        return f"{self.name} is {'active' if self.active else 'inactive'}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        wdr5 = Wdr5("Wdr5")
        kat8 = Kat8("Kat8")
        world.addObject(wdr5)
        world.addObject(kat8)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("activate Kat8", ["activate", allObjects["Kat8"][0]])
        self.addAction("deactivate Kat8", ["deactivate", allObjects["Kat8"][0]])
        self.addAction("recruit Wdr5", ["recruit", allObjects["Wdr5"][0]])

    def actionRecruit(self, wdr5, kat8):
        wdr5.recruit(kat8.active)

    def actionActivate(self, kat8):
        kat8.activate()

    def actionDeactivate(self, kat8):
        kat8.deactivate()

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "activate":
            self.actionActivate(action[1])
            self.observationStr = f"{action[1].name} activated."
        elif actionVerb == "deactivate":
            self.actionDeactivate(action[1])
            self.observationStr = f"{action[1].name} deactivated."
        elif actionVerb == "recruit":
            self.actionRecruit(action[1], self.rootObject.containsItemWithName("Kat8")[0])
            self.observationStr = f"{action[1].name} recruitment status updated."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "activate Kat8", "recruit Wdr5", "look", "deactivate Kat8", "recruit Wdr5"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
