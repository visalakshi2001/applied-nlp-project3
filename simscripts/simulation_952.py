
# Claim: Pioglitazone use is not associated with an increased risk of prostate cancer.
# The simulation will evaluate the association between pioglitazone use and prostate cancer risk.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, pioglitazone_use=False, prostate_cancer_risk=0):
        super().__init__(name)
        self.pioglitazone_use = pioglitazone_use
        self.prostate_cancer_risk = prostate_cancer_risk

    def tick(self):
        # If the patient uses pioglitazone, increase the risk of prostate cancer
        if self.pioglitazone_use:
            self.prostate_cancer_risk += 1.13  # Simulating the increased risk factor

    def makeDescriptionStr(self):
        return f"{self.name} uses pioglitazone: {self.pioglitazone_use}. Prostate cancer risk: {self.prostate_cancer_risk}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

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
        patient1 = Patient("Patient 1", pioglitazone_use=True)
        patient2 = Patient("Patient 2", pioglitazone_use=False)
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

    # Evaluate the claim based on the simulation results
    patient1 = simulation.rootObject.contains[0]  # Patient 1 with pioglitazone use
    patient2 = simulation.rootObject.contains[1]  # Patient 2 without pioglitazone use

    if patient1.prostate_cancer_risk > patient2.prostate_cancer_risk:
        print("Claim is Refuted: Pioglitazone use is associated with an increased risk of prostate cancer.")
    else:
        print("Claim is Supported: Pioglitazone use is not associated with an increased risk of prostate cancer.")

if __name__ == "__main__":
    main()
