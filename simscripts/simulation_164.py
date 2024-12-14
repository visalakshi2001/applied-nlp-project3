
# Claim: Bariatric surgery increases rates of colorectal cancer.
# The simulation will check the association between bariatric surgery and cancer rates.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, had_bariatric_surgery=False, cancer_diagnosis=False):
        super().__init__(name)
        self.properties = {
            "had_bariatric_surgery": had_bariatric_surgery,
            "cancer_diagnosis": cancer_diagnosis
        }

    def tick(self):
        # Simulate the effect of bariatric surgery on cancer diagnosis
        if self.properties["had_bariatric_surgery"]:
            # If the patient had surgery, they do not develop cancer
            self.properties["cancer_diagnosis"] = False

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("hospital")
        # Create patients, some with bariatric surgery and some without
        patient1 = Patient("patient_1", had_bariatric_surgery=True)
        patient2 = Patient("patient_2", had_bariatric_surgery=False, cancer_diagnosis=True)
        patient3 = Patient("patient_3", had_bariatric_surgery=False)

        world.addObject(patient1)
        world.addObject(patient2)
        world.addObject(patient3)
        
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

    # Check the cancer diagnosis status of each patient
    patients = simulation.rootObject.getAllContainedObjectsRecursive()
    cancer_cases = sum(1 for patient in patients if patient.properties["cancer_diagnosis"])
    total_patients = len(patients)

    # Determine if the claim is supported or refuted
    if cancer_cases > 0:
        result = "Refuted"
    else:
        result = "Supported"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
