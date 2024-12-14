
# Claim: Nonsteroidal antinflammatory drugs are ineffective as cancer treatments.
# The simulation will evaluate the effectiveness of NSAIDs in reducing the risk of colorectal cancer based on the provided reference text.

from simulation_utils import GameObject, Container

class CancerRisk(GameObject):
    def __init__(self, name, regular_use=False):
        super().__init__(name)
        self.regular_use = regular_use
        self.risk_level = 1.0  # baseline risk level

    def tick(self):
        if self.regular_use:
            self.risk_level *= 0.69  # reduce risk by 31% if NSAIDs are used regularly

    def makeDescriptionStr(self):
        return f"{self.name} has a risk level of {self.risk_level:.2f}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        cancer_case = CancerRisk("Colorectal Cancer Case", regular_use=True)
        world.addObject(cancer_case)
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
    print("Simulating the effect of regular NSAID use on cancer risk...")
    obs = simulation.step("look")
    print(obs)

if __name__ == "__main__":
    main()
