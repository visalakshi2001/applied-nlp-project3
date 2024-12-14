
# Claim: HAND2 methylation is a key step in early endometrial carcinogenesis.
# The simulation will model the relationship between HAND2 methylation and endometrial cancer development.

from simulation_utils import GameObject, Container

class HAND2(GameObject):
    def __init__(self, name, methylation_level=0):
        super().__init__(name)
        self.methylation_level = methylation_level  # Methylation level of HAND2

    def tick(self):
        # Simulate the effect of methylation on cancer development
        if self.methylation_level > 50:  # Arbitrary threshold for high methylation
            self.properties["cancer_risk"] = "high"
        else:
            self.properties["cancer_risk"] = "low"

    def makeDescriptionStr(self):
        return f"{self.name} with methylation level {self.methylation_level} and cancer risk is {self.properties.get('cancer_risk', 'unknown')}."

class EndometrialTissue(Container):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        tissue = EndometrialTissue("Endometrial Tissue")
        hand2 = HAND2("HAND2 Gene", methylation_level=70)  # High methylation level
        tissue.addObject(hand2)
        return tissue

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

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
