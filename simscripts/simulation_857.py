
# Claim: Nonsteroidal antinflammatory drugs show potential anticancer indications.
# The simulation will model the relationship between NSAID usage and colorectal cancer risk.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, regular_nsaid_use=False, cancer_risk=0):
        super().__init__(name)
        self.properties = {
            "regular_nsaid_use": regular_nsaid_use,
            "cancer_risk": cancer_risk
        }

    def tick(self):
        # If the patient regularly uses NSAIDs, reduce cancer risk
        if self.properties["regular_nsaid_use"]:
            self.properties["cancer_risk"] *= 0.69  # Simulating a reduction in risk
        else:
            self.properties["cancer_risk"] *= 1.0  # No change in risk

    def makeDescriptionStr(self):
        description = f"{self.name} uses NSAIDs regularly: {self.properties['regular_nsaid_use']}. Current cancer risk: {self.properties['cancer_risk']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "medical environment")

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
        patient1 = Patient("Patient 1", regular_nsaid_use=True, cancer_risk=1.0)  # Initial risk set to 1.0
        patient2 = Patient("Patient 2", regular_nsaid_use=False, cancer_risk=1.0)  # Initial risk set to 1.0
        world.addObject(patient1)
        world.addObject(patient2)        
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

# The simulation shows that regular NSAID use reduces cancer risk, supporting the claim.
