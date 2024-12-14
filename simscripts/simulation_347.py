
# Claim: Differentiation of progenitor cells to myeloid cells is skewed when insulin signaling is suppressed.
# The simulation will model the effect of insulin signaling on progenitor cells and their differentiation into myeloid cells.

from simulation_utils import GameObject, Container

class ProgenitorCell(GameObject):
    def __init__(self, name, insulin_signaling=1):
        super().__init__(name)
        self.insulin_signaling = insulin_signaling  # 1 means normal signaling, 0 means suppressed
        self.differentiation_status = "undifferentiated"

    def tick(self):
        if self.insulin_signaling == 0:
            self.differentiation_status = "skewed differentiation"
        else:
            self.differentiation_status = "normal differentiation"

    def makeDescriptionStr(self):
        return f"A {self.name} with insulin signaling at {self.insulin_signaling}, resulting in {self.differentiation_status}."

class MyeloidCell(GameObject):
    def __init__(self, name):
        super().__init__(name)

class World(Container):
    def __init__(self):
        super().__init__("haematopoietic environment")

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
        progenitor_cell_normal = ProgenitorCell("normal_progenitor", insulin_signaling=1)
        progenitor_cell_suppressed = ProgenitorCell("suppressed_progenitor", insulin_signaling=0)
        world.addObject(progenitor_cell_normal)
        world.addObject(progenitor_cell_suppressed)
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
