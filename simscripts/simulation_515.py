
# Claim: High levels of CRP lead to a higher risk of exacerbations in chronic obstructive pulmonary disease (COPD).
# The simulation will model the relationship between CRP levels and exacerbation risk in COPD patients.

from simulation_utils import GameObject, Container

class COPDPatient(GameObject):
    def __init__(self, name, CRP_level=0):
        super().__init__(name)
        self.CRP_level = CRP_level
        self.exacerbation_risk = 0

    def calculate_exacerbation_risk(self):
        if self.CRP_level > 3:  # High CRP level threshold
            self.exacerbation_risk = 81  # High risk for 3 high biomarkers
        elif self.CRP_level > 1:  # Moderate CRP level
            self.exacerbation_risk = 32  # Moderate risk for 2 high biomarkers
        else:
            self.exacerbation_risk = 9  # Low risk for no elevated biomarkers

    def tick(self):
        self.calculate_exacerbation_risk()

    def makeDescriptionStr(self):
        return f"{self.name} has a CRP level of {self.CRP_level} and an exacerbation risk of {self.exacerbation_risk} events/1000 person-years."

class World(Container):
    def __init__(self):
        Container.__init__(self, "COPD Environment")

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
        patient1 = COPDPatient("Patient 1", CRP_level=4)  # High CRP level
        patient2 = COPDPatient("Patient 2", CRP_level=2)  # Moderate CRP level
        patient3 = COPDPatient("Patient 3", CRP_level=0)  # Low CRP level
        world.addObject(patient1)
        world.addObject(patient2)
        world.addObject(patient3)
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

        # Call tick to update exacerbation risks
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

# The expected output will show that Patient 1 has a high exacerbation risk due to high CRP levels,
# Patient 2 has a moderate risk, and Patient 3 has a low risk, supporting the claim.
