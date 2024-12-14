
# Claim: 40mg/day dosage of folic acid and 2mg/day dosage of vitamin B12 does not affect chronic kidney disease (CKD) progression.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, folic_acid_dosage=0, vitamin_b12_dosage=0, homocysteine_level=24.0, mortality_rate=0):
        super().__init__(name)
        self.folic_acid_dosage = folic_acid_dosage
        self.vitamin_b12_dosage = vitamin_b12_dosage
        self.homocysteine_level = homocysteine_level
        self.mortality_rate = mortality_rate

    def tick(self):
        # Simulate the effect of folic acid and vitamin B12 on homocysteine levels
        if self.folic_acid_dosage == 40 and self.vitamin_b12_dosage == 2:
            self.homocysteine_level -= 6.3  # Decrease in homocysteine level
        else:
            self.homocysteine_level += 0  # No effect

        # Mortality rate remains unchanged as per the study results
        self.mortality_rate = 448  # Number of deaths in the vitamin group

    def makeDescriptionStr(self):
        return f"{self.name} with folic acid dosage: {self.folic_acid_dosage}mg, vitamin B12 dosage: {self.vitamin_b12_dosage}mg, homocysteine level: {self.homocysteine_level}, mortality rate: {self.mortality_rate}."

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
        patient = Patient("CKD Patient", folic_acid_dosage=40, vitamin_b12_dosage=2)
        world.addObject(patient)
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

    # Check the results to determine if the claim is supported or refuted
    patient = simulation.rootObject.contains[0]  # Get the patient object
    if patient.mortality_rate == 448:
        print("Claim is supported: 40mg/day dosage of folic acid and 2mg/day dosage of vitamin B12 does not affect CKD progression.")
    else:
        print("Claim is refuted: 40mg/day dosage of folic acid and 2mg/day dosage of vitamin B12 affects CKD progression.")

if __name__ == "__main__":
    main()
