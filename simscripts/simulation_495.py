
# Claim: Having a main partner improves HIV outcomes.
# This simulation will model the effect of having a stable partnership on HIV outcomes.

from simulation_utils import GameObject, Container

class HIVPatient(GameObject):
    def __init__(self, name, has_stable_partnership=False):
        super().__init__(name)
        self.has_stable_partnership = has_stable_partnership
        self.properties = {
            "time_to_AIDS_or_death": 0,
            "death": False,
            "CD4_increase": 0,
            "viral_suppression": False
        }

    def tick(self):
        if self.has_stable_partnership:
            self.properties["time_to_AIDS_or_death"] += 0.79  # Slower progression
            self.properties["CD4_increase"] += 1  # Increase in CD4 cells
            self.properties["viral_suppression"] = True  # Optimal viral suppression
        else:
            self.properties["time_to_AIDS_or_death"] += 1  # Faster progression
            self.properties["CD4_increase"] += 0  # No increase in CD4 cells
            self.properties["viral_suppression"] = False  # No viral suppression

    def makeDescriptionStr(self):
        description = f"{self.name} - Stable Partnership: {self.has_stable_partnership}, Time to AIDS/Death: {self.properties['time_to_AIDS_or_death']}, CD4 Increase: {self.properties['CD4_increase']}, Viral Suppression: {self.properties['viral_suppression']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "HIV Environment")

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
        patient_with_partner = HIVPatient("Patient A", has_stable_partnership=True)
        patient_without_partner = HIVPatient("Patient B", has_stable_partnership=False)
        world.addObject(patient_with_partner)
        world.addObject(patient_without_partner)
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
            allPatients = self.rootObject.getAllContainedObjectsRecursive()
            for patient in allPatients:
                patient.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the progression of time
    for _ in range(5):  # Simulate 5 time ticks
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
