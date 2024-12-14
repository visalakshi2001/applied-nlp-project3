
# Claim: Elevated cell-free mitochondrial DNA levels are associated with mortality.
# The simulation will model ICU patients and their mtDNA levels to determine the association with mortality.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, mtDNA_level=0, mortality_risk=0):
        super().__init__(name)
        self.properties = {
            "mtDNA_level": mtDNA_level,
            "mortality_risk": mortality_risk
        }

    def tick(self):
        # Update mortality risk based on mtDNA level
        if self.properties["mtDNA_level"] >= 3200:
            self.properties["mortality_risk"] = 1  # High risk
        else:
            self.properties["mortality_risk"] = 0  # Low risk

    def makeDescriptionStr(self):
        description = f"{self.name} has an mtDNA level of {self.properties['mtDNA_level']} copies/µl plasma and a mortality risk of {self.properties['mortality_risk']}."
        return description

class ICU(Container):
    def __init__(self):
        super().__init__("ICU")

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
        icu = ICU()
        patient1 = Patient("Patient 1", mtDNA_level=3500)  # Elevated mtDNA level
        patient2 = Patient("Patient 2", mtDNA_level=2500)  # Normal mtDNA level
        icu.addObject(patient1)
        icu.addObject(patient2)
        return icu

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

    # Check the mortality risk based on mtDNA levels
    patient1_risk = simulation.rootObject.contains[0].properties["mortality_risk"]
    patient2_risk = simulation.rootObject.contains[1].properties["mortality_risk"]

    if patient1_risk == 1 and patient2_risk == 0:
        print("Claim Supported: Elevated mtDNA levels are associated with increased mortality risk.")
    else:
        print("Claim Refuted: No association found.")

if __name__ == "__main__":
    main()
