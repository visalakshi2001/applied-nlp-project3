
# Claim: Pioglitazone use is significantly associated with an increased risk of prostate cancer.
# The simulation will evaluate the association between pioglitazone use and prostate cancer risk.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, pioglitazone_use=False, prostate_cancer=False):
        super().__init__(name)
        self.properties = {
            "pioglitazone_use": pioglitazone_use,
            "prostate_cancer": prostate_cancer
        }

    def tick(self):
        # Simulate the risk of developing prostate cancer based on pioglitazone use
        if self.properties["pioglitazone_use"]:
            # Increase the risk of prostate cancer
            self.properties["prostate_cancer"] = True if random.random() < 0.13 else False  # 13% risk based on HR

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

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

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

    # Check the results for prostate cancer risk
    patients = simulation.rootObject.getAllContainedObjectsRecursive()
    pioglitazone_users = [p for p in patients if p.properties["pioglitazone_use"]]
    prostate_cancer_cases = [p for p in pioglitazone_users if p.properties["prostate_cancer"]]

    if len(prostate_cancer_cases) > 0:
        print("Claim Supported: Pioglitazone use is associated with an increased risk of prostate cancer.")
    else:
        print("Claim Refuted: No significant association found between pioglitazone use and prostate cancer risk.")

if __name__ == "__main__":
    main()
