
# The claim is that the combination of physical examinations with C-reactive protein values do not improve the accuracy of radiographic verified pneumonia predictions.
# The reference text indicates that the addition of CRP improved diagnostic classification.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, symptoms, crp_value):
        super().__init__(name)
        self.properties = {
            "symptoms": symptoms,
            "crp_value": crp_value,
            "diagnosis": None
        }

    def assess_diagnosis(self):
        # Simulate the diagnostic process
        if self.properties["crp_value"] > 30:
            self.properties["diagnosis"] = "High risk for pneumonia"
        else:
            self.properties["diagnosis"] = "Low risk for pneumonia"

class DiagnosticTool(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def evaluate(self, patient):
        patient.assess_diagnosis()
        return patient.properties["diagnosis"]

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("Diagnostic Environment")
        patient1 = Patient("Patient 1", ["cough", "fever"], 35)  # High CRP
        patient2 = Patient("Patient 2", ["cough"], 20)           # Low CRP
        diagnostic_tool = DiagnosticTool("Pneumonia Diagnostic Tool")

        world.addObject(patient1)
        world.addObject(patient2)
        world.addObject(diagnostic_tool)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if isinstance(obj, Patient):
                    self.addAction(f"assess {objReferent}", ["assess", obj])

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "assess":
            diagnosis = action[1].assess_diagnosis()
            self.observationStr = f"{action[1].name} is assessed: {diagnosis}"

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["assess Patient 1", "assess Patient 2", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
