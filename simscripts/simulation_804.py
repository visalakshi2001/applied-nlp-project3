
# Claim: Monoclonal antibody targeting of N-cadherin inhibits growth.
# The simulation will model the effect of monoclonal antibodies on N-cadherin expression and its impact on cancer cell growth.

from simulation_utils import GameObject, Container

class CancerCell(GameObject):
    def __init__(self, name, n_cadherin_expression=1.0):
        super().__init__(name)
        self.n_cadherin_expression = n_cadherin_expression
        self.growth_rate = 1.0  # Base growth rate

    def apply_monoclonal_antibody(self):
        # Monoclonal antibodies reduce N-cadherin expression and thus inhibit growth
        self.n_cadherin_expression *= 0.5  # Reduce N-cadherin expression by half
        self.growth_rate *= 0.5  # Reduce growth rate by half

    def tick(self):
        # Simulate growth based on the current growth rate
        self.growth_rate += (1 - self.n_cadherin_expression) * 0.1  # Growth is inhibited by N-cadherin expression

    def makeDescriptionStr(self):
        return f"{self.name} with N-cadherin expression level {self.n_cadherin_expression:.2f} and growth rate {self.growth_rate:.2f}."

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
        cancer_cell = CancerCell("Prostate Cancer Cell")
        world.addObject(cancer_cell)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("apply monoclonal antibody", ["apply", self.rootObject.contains[0]])

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
        elif actionVerb == "apply":
            action[1].apply_monoclonal_antibody()
            self.observationStr = f"Applied monoclonal antibody to {action[1].name}."

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "apply monoclonal antibody"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
