
# Claim: Intramembrane cleavage by signal peptide peptidase aids in the degradation of proteins with a complex membrane orientation.
# The simulation will model the behavior of a protein that undergoes intramembrane cleavage and its degradation process.

from simulation_utils import GameObject, Container

class MembraneProtein(GameObject):
    def __init__(self, name, orientation_stability=0):
        super().__init__(name)
        self.properties = {
            "orientation_stability": orientation_stability,  # Stability of the protein's orientation
            "isCleaved": False,  # Indicates if the protein has been cleaved
            "isDegraded": False   # Indicates if the protein has been degraded
        }

    def cleave(self):
        if self.properties["orientation_stability"] < 5:  # Arbitrary threshold for cleavage
            self.properties["isCleaved"] = True
            return f"{self.name} has been cleaved."
        else:
            return f"{self.name} is too stable to be cleaved."

    def degrade(self):
        if self.properties["isCleaved"]:
            self.properties["isDegraded"] = True
            return f"{self.name} has been degraded."
        else:
            return f"{self.name} cannot be degraded until it is cleaved."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cell_environment")
        protein = MembraneProtein("membrane_protein_1", orientation_stability=3)  # Unstable protein
        world.addObject(protein)
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
                self.addAction(f"cleave {objReferent}", ["cleave", obj])
                self.addAction(f"degrade {objReferent}", ["degrade", obj])

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "cleave":
            self.observationStr = action[1].cleave()
        elif actionVerb == "degrade":
            self.observationStr = action[1].degrade()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["cleave membrane_protein_1", "degrade membrane_protein_1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
