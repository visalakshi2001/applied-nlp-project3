
# Claim: Environmentally-induced senescence is mimicked in disease modeling by adding specific molecules to the culture system.
# The simulation will model the addition of progerin to iPSC-derived cells to observe aging-related features.

from simulation_utils import GameObject, Container

class Cell(GameObject):
    def __init__(self, name, progerin_expression=0):
        super().__init__(name)
        self.properties = {
            "progerin_expression": progerin_expression,
            "aging_markers": 0,
            "disease_phenotypes": 0
        }

    def tick(self):
        # Simulate the effect of progerin expression on aging markers and disease phenotypes
        self.properties["aging_markers"] = self.properties["progerin_expression"] * 2  # Arbitrary relationship
        self.properties["disease_phenotypes"] = self.properties["progerin_expression"] * 3  # Arbitrary relationship

    def makeDescriptionStr(self):
        description = (f"A {self.name} with progerin expression level {self.properties['progerin_expression']}, "
                       f"aging markers: {self.properties['aging_markers']}, "
                       f"disease phenotypes: {self.properties['disease_phenotypes']}.")
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("lab")
        cell1 = Cell("iPSC-derived fibroblast")
        cell2 = Cell("iPSC-derived neuron")
        world.addObject(cell1)
        world.addObject(cell2)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("add progerin to fibroblast", ["add", "fibroblast"])
        self.addAction("add progerin to neuron", ["add", "neuron"])
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
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
        elif actionVerb == "add":
            if action[1] == "fibroblast":
                self.rootObject.contains[0].properties["progerin_expression"] += 1
                self.observationStr = f"Progerin added to {self.rootObject.contains[0].name}."
            elif action[1] == "neuron":
                self.rootObject.contains[1].properties["progerin_expression"] += 1
                self.observationStr = f"Progerin added to {self.rootObject.contains[1].name}."

        # Update the state of the cells
        for cell in self.rootObject.contains:
            cell.tick()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["add progerin to fibroblast", "add progerin to neuron", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
