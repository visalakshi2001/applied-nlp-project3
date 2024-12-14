
# Claim: Progerin induces premature aging in stem cells.
# This simulation will model the effects of progerin on induced pluripotent stem cells (iPSCs) to verify the claim.

from simulation_utils import GameObject, Container

class StemCell(GameObject):
    def __init__(self, name, progerin_expression=0):
        super().__init__(name)
        self.progerin_expression = progerin_expression
        self.properties = {
            "aging_markers": 0,
            "dopamine_specific_phenotypes": 0
        }

    def tick(self):
        # Increase aging markers and dopamine-specific phenotypes based on progerin expression
        self.properties["aging_markers"] += self.progerin_expression
        self.properties["dopamine_specific_phenotypes"] += self.progerin_expression * 2  # Arbitrary multiplier for phenotypes

    def makeDescriptionStr(self):
        description = (f"A {self.name} with progerin expression level {self.progerin_expression}, "
                       f"aging markers: {self.properties['aging_markers']}, "
                       f"dopamine-specific phenotypes: {self.properties['dopamine_specific_phenotypes']}.")
        return description

class ProgerinContainer(Container):
    def __init__(self):
        super().__init__("Progerin Environment")

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
        world = ProgerinContainer()
        stem_cell = StemCell("iPSC", progerin_expression=1)  # Simulating progerin expression
        world.addObject(stem_cell)
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

    # Check the aging markers to determine if the claim is supported
    stem_cell = simulation.rootObject.contains[0]  # Accessing the stem cell
    if stem_cell.properties["aging_markers"] > 0:
        print("Claim Supported: Progerin induces premature aging in stem cells.")
    else:
        print("Claim Refuted: Progerin does not induce premature aging in stem cells.")

if __name__ == "__main__":
    main()
