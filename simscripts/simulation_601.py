
# Claim: Including pharmacists in rounding teams reduces the incidence of adverse drug events (ADEs).

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, ade_rate):
        super().__init__(name)
        self.properties = {
            "ade_rate": ade_rate  # Adverse drug event rate per 1000 patient-days
        }

    def tick(self):
        # Simulate the effect of pharmacist intervention
        if self.getProperty("pharmacist_present"):
            self.properties["ade_rate"] *= 0.34  # 66% reduction in ADEs
        else:
            self.properties["ade_rate"] *= 1  # No change if no pharmacist

    def makeDescriptionStr(self):
        return f"{self.name} has an ADE rate of {self.properties['ade_rate']} per 1000 patient-days."

class Pharmacist(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties["pharmacist_present"] = True  # Indicates pharmacist is present

class ICU(Container):
    def __init__(self, name):
        super().__init__(name)

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
        icu = ICU("ICU")
        patient_before = Patient("Patient Before Intervention", 10.4)  # ADE rate before intervention
        patient_after = Patient("Patient After Intervention", 10.4)  # Same initial rate
        pharmacist = Pharmacist("Pharmacist")
        
        icu.addObject(patient_before)
        icu.addObject(patient_after)
        icu.addObject(pharmacist)
        
        # Simulate the intervention
        patient_after.properties["pharmacist_present"] = True  # Pharmacist present during rounds
        
        return icu

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"]}

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
    print("Simulating the effect of pharmacist intervention...\n")
    print(simulation.step("look"))

if __name__ == "__main__":
    main()
