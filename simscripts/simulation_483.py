
# Claim: H.pylori-mediated gastric cancer occurs due to the accumulation of mutations in host epithelial cells.
# This simulation will model the effects of H. pylori infection on gastric epithelial cells and the resulting mutations.

from simulation_utils import GameObject, Container

class EpithelialCell(GameObject):
    def __init__(self, name, mutations=0):
        super().__init__(name)
        self.mutations = mutations

    def infect_with_h_pylori(self):
        # Simulate the effect of H. pylori infection leading to mutation accumulation
        self.mutations += 1  # Each infection increases mutations
        return f"{self.name} has been infected with H. pylori, mutations increased to {self.mutations}."

class H_Pylori(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def induce_mutations(self, epithelial_cell):
        # Induce mutations in the epithelial cell
        return epithelial_cell.infect_with_h_pylori()

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("Gastric Environment")
        epithelial_cell = EpithelialCell("Gastric Epithelial Cell")
        h_pylori = H_Pylori("H. pylori")
        world.addObject(epithelial_cell)
        world.addObject(h_pylori)
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
        self.addAction("infect epithelial cell", ["infect", allObjects["Gastric Epithelial Cell"][0]])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "infect":
            epithelial_cell = action[1]
            self.observationStr = epithelial_cell.induce_mutations(epithelial_cell)

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "infect epithelial cell"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check to determine if the claim is supported or refuted
    if simulation.rootObject.contains[0].mutations > 0:
        print("Claim Supported: H.pylori-mediated gastric cancer occurs due to the accumulation of mutations in host epithelial cells.")
    else:
        print("Claim Refuted: No mutations accumulated in host epithelial cells.")

if __name__ == "__main__":
    main()
