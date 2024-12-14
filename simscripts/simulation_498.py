
# Claim: Having a main partner worsens HIV outcomes.
# The simulation will explore the relationship between stable partnerships and HIV outcomes.

from simulation_utils import GameObject, Container

class HIVPatient(GameObject):
    def __init__(self, name, stable_partnership=False):
        super().__init__(name)
        self.stable_partnership = stable_partnership
        self.properties = {
            "time_to_AIDS_or_death": 0,
            "CD4_count": 0,
            "viral_load": 0,
            "progression": 0
        }

    def tick(self):
        # Simulate the effect of having a stable partnership on HIV outcomes
        if self.stable_partnership:
            self.properties["time_to_AIDS_or_death"] += 0.79  # Slower progression
            self.properties["CD4_count"] += 1  # Increase in CD4 count
            self.properties["viral_load"] = max(0, self.properties["viral_load"] - 1)  # Better viral suppression
        else:
            self.properties["time_to_AIDS_or_death"] += 1  # Faster progression
            self.properties["CD4_count"] -= 1  # Decrease in CD4 count
            self.properties["viral_load"] += 1  # Worse viral suppression

    def makeDescriptionStr(self):
        description = f"{self.name} with stable partnership: {self.stable_partnership}. "
        description += f"Time to AIDS or death: {self.properties['time_to_AIDS_or_death']}, "
        description += f"CD4 count: {self.properties['CD4_count']}, "
        description += f"Viral load: {self.properties['viral_load']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "HIV Simulation Environment")

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
        patient_with_partner = HIVPatient("Patient A", stable_partnership=True)
        patient_without_partner = HIVPatient("Patient B", stable_partnership=False)
        world.addObject(patient_with_partner)
        world.addObject(patient_without_partner)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"tick": []}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        if actionStr == "tick":
            allPatients = self.rootObject.getAllContainedObjectsRecursive()
            for patient in allPatients:
                patient.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the progression of HIV outcomes
    for _ in range(5):  # Simulate 5 time steps
        print("Ticking...")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Final assessment based on the outcomes
    patient_with_partner = simulation.rootObject.contains[0]
    patient_without_partner = simulation.rootObject.contains[1]

    if patient_with_partner.properties["time_to_AIDS_or_death"] < patient_without_partner.properties["time_to_AIDS_or_death"]:
        print("Claim Refuted: Having a main partner does not worsen HIV outcomes.")
    else:
        print("Claim Supported: Having a main partner worsens HIV outcomes.")

if __name__ == "__main__":
    main()
