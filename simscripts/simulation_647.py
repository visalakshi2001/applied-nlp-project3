
# Claim: Integrated care is ineffective at tackling multiple comorbidities.
# The simulation will evaluate the effectiveness of integrated care based on the provided reference text.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, disability_score=0, quality_of_life=0):
        super().__init__(name)
        self.properties = {
            "disability_score": disability_score,
            "quality_of_life": quality_of_life
        }

    def apply_intervention(self):
        # Simulate the effect of integrated care intervention
        self.properties["disability_score"] -= 0.9  # Improvement in disability score
        self.properties["quality_of_life"] += 0.7   # Improvement in quality of life

    def makeDescriptionStr(self):
        description = f"{self.name} has a disability score of {self.properties['disability_score']} and a quality of life score of {self.properties['quality_of_life']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "healthcare environment")

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
        patient1 = Patient("Patient 1", disability_score=5, quality_of_life=2)
        patient2 = Patient("Patient 2", disability_score=4, quality_of_life=3)
        world.addObject(patient1)
        world.addObject(patient2)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("apply integrated care intervention", [])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def actionApplyIntervention(self):
        allPatients = self.rootObject.getAllContainedObjectsRecursive()
        for patient in allPatients:
            if isinstance(patient, Patient):
                patient.apply_intervention()

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "apply integrated care intervention":
            self.actionApplyIntervention()

        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print("Before intervention:")
    print(simulation.observationStr)
    
    print("Applying integrated care intervention...")
    simulation.step("apply integrated care intervention")
    
    print("After intervention:")
    print(simulation.observationStr)

    # Determine if the claim is supported or refuted based on the results
    patient1_disability = simulation.rootObject.contains[0].properties["disability_score"]
    patient1_quality_of_life = simulation.rootObject.contains[0].properties["quality_of_life"]

    if patient1_disability < 5 and patient1_quality_of_life > 2:
        print("Claim is Refuted: Integrated care is effective at tackling multiple comorbidities.")
    else:
        print("Claim is Supported: Integrated care is ineffective at tackling multiple comorbidities.")

if __name__ == "__main__":
    main()
