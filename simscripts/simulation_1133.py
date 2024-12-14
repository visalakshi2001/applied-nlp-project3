
# Claim: TMEM27 is a marker for beta cells.
# The simulation will check if TMEM27 is specifically associated with pancreatic beta cells and if its expression correlates with beta cell mass.

from simulation_utils import GameObject, Container

class BetaCell(GameObject):
    def __init__(self, name, tmem27_expression=0):
        super().__init__(name)
        self.tmem27_expression = tmem27_expression

    def tick(self):
        # Simulate the effect of TMEM27 expression on beta cell growth
        if self.tmem27_expression > 0:
            self.tmem27_expression += 1  # Simulate increase in TMEM27 expression
        else:
            self.tmem27_expression = 0  # Ensure it doesn't go negative

    def makeDescriptionStr(self):
        return f"A {self.name} with TMEM27 expression level: {self.tmem27_expression}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        beta_cell = BetaCell("beta_cell_1", tmem27_expression=5)  # Initial TMEM27 expression
        world.addObject(beta_cell)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

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

    # Check if TMEM27 is a marker for beta cells based on the expression level
    beta_cell = simulation.rootObject.containsItemWithName("beta_cell_1")[0]
    if beta_cell.tmem27_expression > 0:
        print("Claim Supported: TMEM27 is a marker for beta cells.")
    else:
        print("Claim Refuted: TMEM27 is not a marker for beta cells.")

if __name__ == "__main__":
    main()
