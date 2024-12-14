
# Claim: ALDH1 expression is associated with poorer prognosis for breast cancer primary tumors.
# The simulation will model breast cancer tumors and their ALDH1 expression levels to determine the correlation with prognosis.

from simulation_utils import GameObject, Container

class Tumor(GameObject):
    def __init__(self, name, ALDH1_expression=0):
        super().__init__(name)
        self.properties = {
            "ALDH1_expression": ALDH1_expression,
            "prognosis": self.determine_prognosis(ALDH1_expression)
        }

    def determine_prognosis(self, ALDH1_expression):
        # Higher ALDH1 expression correlates with poorer prognosis
        if ALDH1_expression > 5:  # Arbitrary threshold for high expression
            return "poor"
        else:
            return "good"

    def tick(self):
        # Simulate changes in ALDH1 expression over time
        self.properties["ALDH1_expression"] += 1  # Simulate increase
        self.properties["prognosis"] = self.determine_prognosis(self.properties["ALDH1_expression"])

    def makeDescriptionStr(self):
        description = f"A tumor named {self.name} with ALDH1 expression level {self.properties['ALDH1_expression']} and prognosis is {self.properties['prognosis']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "breast cancer environment")

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
        tumor1 = Tumor("Tumor A", ALDH1_expression=6)  # High expression
        tumor2 = Tumor("Tumor B", ALDH1_expression=3)  # Low expression
        world.addObject(tumor1)
        world.addObject(tumor2)        
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
