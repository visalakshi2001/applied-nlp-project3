
# Claim: Pioglitazone use is significantly associated with an increased risk of pancreatic cancer.
# The simulation will evaluate the association between pioglitazone use and pancreatic cancer risk.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, pioglitazone_use=False, pancreatic_cancer=False):
        super().__init__(name)
        self.properties = {
            "pioglitazone_use": pioglitazone_use,
            "pancreatic_cancer": pancreatic_cancer
        }

    def tick(self):
        # Simulate the risk of pancreatic cancer based on pioglitazone use
        if self.properties["pioglitazone_use"]:
            # Increased risk of pancreatic cancer
            self.properties["pancreatic_cancer"] = True if random.random() < 0.41 else False  # 41% risk based on HR

    def makeDescriptionStr(self):
        return f"{self.name} - Pioglitazone Use: {self.properties['pioglitazone_use']}, Pancreatic Cancer: {self.properties['pancreatic_cancer']}"

class World(Container):
    def __init__(self):
        super().__init__("Diabetes Treatment Environment")

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
        # Create patients with and without pioglitazone use
        patient1 = Patient("Patient 1", pioglitazone_use=True)  # Using pioglitazone
        patient2 = Patient("Patient 2", pioglitazone_use=False)  # Not using pioglitazone
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
            # Perform a tick to simulate the risk assessment
            allPatients = self.rootObject.getAllContainedObjectsRecursive()
            for patient in allPatients:
                patient.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the environment
    for _ in range(5):  # Run multiple ticks to observe changes
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
