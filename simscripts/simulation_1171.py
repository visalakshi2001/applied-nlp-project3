
# Claim: The NF-κB essential modulator gene prevents intestinal inflammation by inhibiting receptor-interacting protein (RIP) kinase 1 kinase activity-mediated epithelial cell death.

from simulation_utils import GameObject, Container

class EpithelialCell(GameObject):
    def __init__(self, name, is_alive=True):
        super().__init__(name)
        self.properties = {
            "is_alive": is_alive
        }

    def tick(self, ripk1_inhibited):
        if not ripk1_inhibited:
            self.properties["is_alive"] = False  # Cell dies if RIPK1 is not inhibited

class NEMO(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "ripk1_inhibited": False
        }

    def inhibit_ripk1(self):
        self.properties["ripk1_inhibited"] = True

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("intestinal_environment")
        nemo = NEMO("NEMO")
        epithelial_cell = EpithelialCell("Epithelial_Cell_1")
        world.addObject(nemo)
        world.addObject(epithelial_cell)
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
        self.addAction("inhibit RIPK1", ["inhibit", allObjects["NEMO"][0]])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "inhibit":
            nemo = action[1]
            nemo.inhibit_ripk1()
            self.observationStr = f"{nemo.name} has inhibited RIPK1 activity."

        # Call tick for all objects
        epithelial_cell = self.rootObject.contains[1]  # Get the epithelial cell
        epithelial_cell.tick(nemo.properties["ripk1_inhibited"])

        # Check if the epithelial cell is alive
        if epithelial_cell.properties["is_alive"]:
            self.observationStr += f"{epithelial_cell.name} is alive."
        else:
            self.observationStr += f"{epithelial_cell.name} has died due to RIPK1 activity."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["inhibit RIPK1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
