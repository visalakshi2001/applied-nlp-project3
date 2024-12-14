
# Claim: Pharmacist attendance at ward rounds increases adverse events in wards.
# The simulation will test the effect of pharmacist participation on the rate of preventable adverse drug events (ADEs).

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, ade_rate):
        super().__init__(name)
        self.properties = {
            "ade_rate": ade_rate  # Rate of preventable ADEs per 1000 patient-days
        }

    def tick(self):
        # Simulate the effect of pharmacist intervention
        if self.getProperty("pharmacist_present"):
            self.properties["ade_rate"] *= 0.34  # 66% reduction in ADEs
        else:
            self.properties["ade_rate"] *= 1  # No change if pharmacist is not present

    def makeDescriptionStr(self):
        return f"{self.name} has a current ADE rate of {self.properties['ade_rate']} per 1000 patient-days."

class Pharmacist(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties["pharmacist_present"] = True  # Indicates pharmacist is present during rounds

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("ICU")
        patient1 = Patient("Patient 1", 10.4)  # Baseline ADE rate
        patient2 = Patient("Patient 2", 10.9)  # Control unit ADE rate
        pharmacist = Pharmacist("Senior Pharmacist")

        world.addObject(patient1)
        world.addObject(patient2)
        world.addObject(pharmacist)

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
        self.addAction("simulate pharmacist rounds", ["simulate", "pharmacist"])

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
        elif actionVerb == "simulate":
            # Simulate the effect of pharmacist rounds
            for patient in self.rootObject.contains:
                if isinstance(patient, Patient):
                    patient.tick()
            self.observationStr = "Pharmacist rounds simulated. ADE rates updated."

        return self.observationStr

    def run_simulation(self):
        print(self.observationStr)
        print("Simulating pharmacist rounds...")
        print(self.step("simulate pharmacist rounds"))
        print(self.rootObject.makeDescriptionStr())

def main():
    simulation = Simulation()
    simulation.run_simulation()

if __name__ == "__main__":
    main()
