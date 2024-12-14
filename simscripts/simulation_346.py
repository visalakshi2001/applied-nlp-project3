
# Claim: Differentiation of progenitor cells to myeloid cells is skewed upon activation of insulin signaling.
# The simulation will model the effect of insulin signaling on progenitor cells and their differentiation into myeloid cells.

from simulation_utils import GameObject, Container

class ProgenitorCell(GameObject):
    def __init__(self, name, insulin_signal=0):
        super().__init__(name)
        self.insulin_signal = insulin_signal
        self.differentiation_state = "undifferentiated"

    def tick(self):
        if self.insulin_signal > 0:
            self.differentiation_state = "differentiated"
        else:
            self.differentiation_state = "undifferentiated"

    def makeDescriptionStr(self):
        return f"A {self.name} with insulin signal level {self.insulin_signal}, currently {self.differentiation_state}."

class MyeloidCell(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def makeDescriptionStr(self):
        return f"A {self.name}, which is a differentiated myeloid cell."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        progenitor = ProgenitorCell("progenitor_cell_1")
        myeloid = MyeloidCell("myeloid_cell_1")
        world.addObject(progenitor)
        world.addObject(myeloid)
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

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"activate insulin signaling for {objReferent}", ["activate", obj])
                self.addAction(f"deactivate insulin signaling for {objReferent}", ["deactivate", obj])

    def actionActivateInsulin(self, progenitor):
        if type(progenitor) != ProgenitorCell:
            return f"Cannot activate insulin signaling for {progenitor.name}."
        else:
            progenitor.insulin_signal += 1
            return f"You activate insulin signaling for {progenitor.name}."

    def actionDeactivateInsulin(self, progenitor):
        if type(progenitor) != ProgenitorCell:
            return f"Cannot deactivate insulin signaling for {progenitor.name}."
        else:
            progenitor.insulin_signal = max(0, progenitor.insulin_signal - 1)
            return f"You deactivate insulin signaling for {progenitor.name}."

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
            self.observationStr = self.actionActivateInsulin(action[1])
        elif actionVerb == "deactivate":
            self.observationStr = self.actionDeactivateInsulin(action[1])

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
    actions = ["look", "activate insulin signaling for progenitor_cell_1", "look", "deactivate insulin signaling for progenitor_cell_1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
