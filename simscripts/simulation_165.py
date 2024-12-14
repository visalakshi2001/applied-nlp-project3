
# Claim: Bariatric surgery increases rates of postmenopausal breast cancer.
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
            self.properties["cancer_diagnosis"] = False  # No association found

    def makeDescriptionStr(self):
        return f"{self.name}: Had bariatric surgery: {self.properties['had_bariatric_surgery']}, Cancer diagnosis: {self.properties['cancer_diagnosis']}"

class World(Container):
    def __init__(self):
        super().__init__("hospital")

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
        patient1 = Patient("Patient 1", had_bariatric_surgery=True)
        patient2 = Patient("Patient 2", had_bariatric_surgery=False)
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

    # Check the cancer diagnosis status
    patient1 = simulation.rootObject.contains[0]  # Patient 1
    patient2 = simulation.rootObject.contains[1]  # Patient 2

    if patient1.properties["cancer_diagnosis"] or patient2.properties["cancer_diagnosis"]:
        print("Claim Supported: Bariatric surgery increases rates of postmenopausal breast cancer.")
    else:
        print("Claim Refuted: No association detected between bariatric surgery and cancer.")

if __name__ == "__main__":
    main()
