
# Claim: Monoclonal antibody targeting of N-cadherin inhibits castration resistance.
# The simulation will model the effects of monoclonal antibodies targeting N-cadherin on castration resistance in prostate cancer.

from simulation_utils import GameObject, Container

class CancerCell(GameObject):
    def __init__(self, name, n_cadherin_expression=0, castration_resistance=False):
        super().__init__(name)
        self.properties = {
            "n_cadherin_expression": n_cadherin_expression,
            "castration_resistance": castration_resistance
        }

    def tick(self):
        # Simulate the effect of N-cadherin expression on castration resistance
        if self.properties["n_cadherin_expression"] > 0:
            self.properties["castration_resistance"] = True

    def makeDescriptionStr(self):
        description = f"{self.name} with N-cadherin expression level {self.properties['n_cadherin_expression']}."
        if self.properties["castration_resistance"]:
            description += " This cell exhibits castration resistance."
        else:
            description += " This cell does not exhibit castration resistance."
        return description

class MonoclonalAntibody(GameObject):
    def __init__(self, name, target):
        super().__init__(name)
        self.target = target

    def apply(self, cancer_cell):
        if self.target == "N-cadherin":
            # Reduce N-cadherin expression to inhibit castration resistance
            cancer_cell.properties["n_cadherin_expression"] = max(0, cancer_cell.properties["n_cadherin_expression"] - 1)

class World(Container):
    def __init__(self):
        super().__init__("Prostate Cancer Environment")

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
        cancer_cell = CancerCell("Prostate Cancer Cell", n_cadherin_expression=5)
        antibody = MonoclonalAntibody("N-cadherin Antibody", target="N-cadherin")
        world.addObject(cancer_cell)
        world.addObject(antibody)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "apply antibody": ["apply", self.rootObject.contains[1], self.rootObject.contains[0]]  # Apply antibody to cancer cell
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "apply":
            antibody = action[1]
            cancer_cell = action[2]
            antibody.apply(cancer_cell)

        # Do one tick of the environment
        self.doWorldTick()

        # Update observation
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Apply the monoclonal antibody to the cancer cell
    action = "apply antibody"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

if __name__ == "__main__":
    main()
