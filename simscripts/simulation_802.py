
# Claim: Monoclonal antibody targeting of N-cadherin encourages metastasis.
# The simulation will model the effects of monoclonal antibodies on N-cadherin expression and its impact on metastasis.

from simulation_utils import GameObject, Container

class CancerCell(GameObject):
    def __init__(self, name, n_cadherin_expression=0, metastasis_level=0):
        super().__init__(name)
        self.properties = {
            "n_cadherin_expression": n_cadherin_expression,
            "metastasis_level": metastasis_level
        }

    def tick(self):
        # If N-cadherin expression is high, increase metastasis level
        if self.properties["n_cadherin_expression"] > 5:
            self.properties["metastasis_level"] += 1

    def makeDescriptionStr(self):
        description = f"A {self.name} with N-cadherin expression level {self.properties['n_cadherin_expression']} and metastasis level {self.properties['metastasis_level']}."
        return description

class Antibody(GameObject):
    def __init__(self, name, effectiveness=0):
        super().__init__(name)
        self.properties = {
            "effectiveness": effectiveness
        }

    def apply(self, cancer_cell):
        # Antibodies reduce N-cadherin expression and metastasis
        cancer_cell.properties["n_cadherin_expression"] -= self.properties["effectiveness"]
        if cancer_cell.properties["n_cadherin_expression"] < 0:
            cancer_cell.properties["n_cadherin_expression"] = 0

class World(Container):
    def __init__(self):
        super().__init__("environment")

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
        cancer_cell = CancerCell("Prostate Cancer Cell", n_cadherin_expression=7)
        antibody = Antibody("N-cadherin Monoclonal Antibody", effectiveness=3)
        world.addObject(cancer_cell)
        world.addObject(antibody)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "apply antibody": ["apply", self.rootObject.contains[1], self.rootObject.contains[0]],  # Apply antibody to cancer cell
            "look": ["look"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply":
            antibody = action[1]
            cancer_cell = action[2]
            antibody.apply(cancer_cell)

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
    actions = ["apply antibody", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
