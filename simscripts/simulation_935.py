
# Claim: Peroxynitrite is required for induction of T cell tolerance.
# This simulation will test the relationship between peroxynitrite and T cell tolerance induction.

from simulation_utils import GameObject, Container

class TCell(GameObject):
    def __init__(self, name, tolerance_level=0):
        super().__init__(name)
        self.tolerance_level = tolerance_level

    def induceTolerance(self, peroxynitrite_level):
        if peroxynitrite_level > 0:
            self.tolerance_level += 1  # Induction of tolerance occurs
        else:
            self.tolerance_level = max(0, self.tolerance_level - 1)  # Tolerance decreases if no peroxynitrite

    def makeDescriptionStr(self):
        return f"A T-cell named {self.name} with tolerance level: {self.tolerance_level}."

class Peroxynitrite(GameObject):
    def __init__(self, name, concentration=0):
        super().__init__(name)
        self.concentration = concentration

    def increaseConcentration(self):
        self.concentration += 1

    def decreaseConcentration(self):
        self.concentration = max(0, self.concentration - 1)

    def makeDescriptionStr(self):
        return f"Peroxynitrite with concentration: {self.concentration}."

class World(Container):
    def __init__(self):
        super().__init__("immune system environment")

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
        t_cell = TCell("TCell_1")
        peroxynitrite = Peroxynitrite("Peroxynitrite_1")
        world.addObject(t_cell)
        world.addObject(peroxynitrite)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}

        self.addAction("look", ["look"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if isinstance(obj, Peroxynitrite):
                    self.addAction(f"increase concentration of {objReferent}", ["increase", obj])
                    self.addAction(f"decrease concentration of {objReferent}", ["decrease", obj])
                elif isinstance(obj, TCell):
                    self.addAction(f"induce tolerance in {objReferent}", ["induce", obj])

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase":
            action[1].increaseConcentration()
        elif actionVerb == "decrease":
            action[1].decreaseConcentration()
        elif actionVerb == "induce":
            action[1].induceTolerance(action[1].getProperty("concentration"))

        self.doWorldTick()
        self.generatePossibleActions()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["increase concentration of Peroxynitrite_1", "induce tolerance in TCell_1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
