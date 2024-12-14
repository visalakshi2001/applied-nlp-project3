
# Claim: Pyridostatin induces checkpoint activation.
# The simulation will model the effects of Pyridostatin on cells, particularly focusing on checkpoint activation and DSB accumulation.

from simulation_utils import GameObject, Container

class Cell(GameObject):
    def __init__(self, name, hr_deficiency=False, dSB_accumulation=0, checkpoint_activated=False):
        super().__init__(name)
        self.properties = {
            "hr_deficiency": hr_deficiency,
            "dSB_accumulation": dSB_accumulation,
            "checkpoint_activated": checkpoint_activated
        }

    def treat_with_pyridostatin(self):
        if self.properties["hr_deficiency"]:
            self.properties["dSB_accumulation"] += 1  # Inducing DSB accumulation
            self.properties["checkpoint_activated"] = True  # Activating checkpoint
        return self.makeDescriptionStr()

    def makeDescriptionStr(self):
        return f"A {self.name} cell with HR deficiency: DSB accumulation is {self.properties['dSB_accumulation']}, checkpoint activated: {self.properties['checkpoint_activated']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cell_environment")
        cell1 = Cell("HR-deficient cell 1", hr_deficiency=True)
        cell2 = Cell("HR-deficient cell 2", hr_deficiency=True)
        world.addObject(cell1)
        world.addObject(cell2)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("treat with pyridostatin", ["treat"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "treat":
            allCells = self.rootObject.getAllContainedObjectsRecursive()
            for cell in allCells:
                if isinstance(cell, Cell):
                    self.observationStr += cell.treat_with_pyridostatin() + "\n"

        return self.observationStr

def main():
    simulation = Simulation()
    print("Initial State:")
    print(simulation.observationStr)
    
    print("Applying treatment:")
    result = simulation.step("treat with pyridostatin")
    print(result)

    # Check if the claim is supported
    if "checkpoint activated: True" in result:
        print("Claim Supported: Pyridostatin induces checkpoint activation.")
    else:
        print("Claim Refuted: Pyridostatin does not induce checkpoint activation.")

if __name__ == "__main__":
    main()
