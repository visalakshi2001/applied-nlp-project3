
# Claim: The NF-κB essential modulator gene induces intestinal inflammation by promoting receptor-interacting protein (RIP) kinase 1 kinase activity-mediated epithelial cell death.

from simulation_utils import GameObject, Container

class EpithelialCell(GameObject):
    def __init__(self, name, is_alive=True):
        super().__init__(name)
        self.properties = {
            "is_alive": is_alive,
            "RIPK1_activity": 0  # Represents the activity level of RIPK1 kinase
        }

    def tick(self):
        # If RIPK1 activity is high, the cell dies
        if self.properties["RIPK1_activity"] > 5:
            self.properties["is_alive"] = False

    def makeDescriptionStr(self):
        status = "alive" if self.properties["is_alive"] else "dead"
        return f"{self.name} is {status} with RIPK1 activity at {self.properties['RIPK1_activity']}."

class NEMO(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "inhibiting_RIPK1": True  # NEMO inhibits RIPK1 activity
        }

    def inhibit_RIPK1(self, epithelial_cell):
        if self.properties["inhibiting_RIPK1"]:
            epithelial_cell.properties["RIPK1_activity"] = max(0, epithelial_cell.properties["RIPK1_activity"] - 3)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("intestinal_environment")
        epithelial_cell = EpithelialCell("Epithelial Cell 1")
        nemo = NEMO("NEMO Protein")
        world.addObject(epithelial_cell)
        world.addObject(nemo)
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
                if isinstance(obj, EpithelialCell):
                    self.addAction(f"increase RIPK1 activity of {objReferent}", ["increase", obj])
                if isinstance(obj, NEMO):
                    self.addAction(f"apply NEMO inhibition on Epithelial Cell 1", ["inhibit", obj, epithelial_cell])

    def actionIncreaseRIPK1(self, epithelial_cell):
        epithelial_cell.properties["RIPK1_activity"] += 2
        return f"You increase the RIPK1 activity of {epithelial_cell.name}."

    def actionInhibit(self, nemo, epithelial_cell):
        nemo.inhibit_RIPK1(epithelial_cell)
        return f"NEMO inhibits RIPK1 activity of {epithelial_cell.name}."

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
            self.observationStr = self.actionIncreaseRIPK1(action[1])
        elif actionVerb == "inhibit":
            self.observationStr = self.actionInhibit(action[1], action[2])

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
    actions = ["increase RIPK1 activity of Epithelial Cell 1", "apply NEMO inhibition on Epithelial Cell 1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
