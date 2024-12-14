
# Claim: BRCA 1 mutation carriers' risk of breast and ovarian cancer depends on where the mutation is located.
# The simulation will model BRCA1 mutation carriers and their associated cancer risks based on mutation location.

from simulation_utils import GameObject, Container

class BRCA1Carrier(GameObject):
    def __init__(self, name, mutation_location, breast_cancer_risk, ovarian_cancer_risk):
        super().__init__(name)
        self.mutation_location = mutation_location
        self.breast_cancer_risk = breast_cancer_risk
        self.ovarian_cancer_risk = ovarian_cancer_risk

    def tick(self):
        # Simulate the risk assessment based on mutation location
        if self.mutation_location in ["BCCR1", "BCCR2", "BCCR2'"]:
            self.breast_cancer_risk *= 1.2  # Increased risk for breast cancer
        elif self.mutation_location == "OCCR":
            self.ovarian_cancer_risk *= 1.2  # Increased risk for ovarian cancer

    def makeDescriptionStr(self):
        description = (f"{self.name} has a mutation at {self.mutation_location}. "
                       f"Breast cancer risk: {self.breast_cancer_risk}, "
                       f"Ovarian cancer risk: {self.ovarian_cancer_risk}.")
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "BRCA1 Mutation Environment")

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
        carrier1 = BRCA1Carrier("Carrier 1", "BCCR1", 1.46, 0.62)  # Example risks based on mutation location
        carrier2 = BRCA1Carrier("Carrier 2", "OCCR", 1.34, 1.2)    # Example risks based on mutation location
        world.addObject(carrier1)
        world.addObject(carrier2)        
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

if __name__ == "__main__":
    main()
