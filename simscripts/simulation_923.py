
# Claim: Patients in stable partnerships have a slower progression from HIV to AIDS.
# The simulation will model the effect of stable partnerships on the progression of HIV to AIDS.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, stable_partnership=False, progression_rate=1.0):
        super().__init__(name)
        self.stable_partnership = stable_partnership
        self.progression_rate = progression_rate  # Lower value means slower progression

    def tick(self):
        if self.stable_partnership:
            self.progression_rate *= 0.79  # Simulating slower progression due to stable partnership
        else:
            self.progression_rate *= 1.0  # No change if no stable partnership

    def makeDescriptionStr(self):
        partnership_status = "has a stable partnership" if self.stable_partnership else "does not have a stable partnership"
        return f"{self.name}, who {partnership_status}, has a progression rate of {self.progression_rate:.2f}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "HIV Patient Environment")

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
        patient1 = Patient("Patient A", stable_partnership=True)  # Stable partnership
        patient2 = Patient("Patient B", stable_partnership=False)  # No stable partnership
        world.addObject(patient1)
        world.addObject(patient2)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

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

        if actionVerb == "tick":
            # Perform a tick to simulate progression
            allPatients = self.rootObject.getAllContainedObjectsRecursive()
            for patient in allPatients:
                patient.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate progression
    for _ in range(5):  # Simulate 5 ticks
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
