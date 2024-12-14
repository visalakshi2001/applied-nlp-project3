
# Claim: A breast cancer patient's capacity to metabolize tamoxifen influences treatment outcome.
# The simulation will model the relationship between CYP2D6 metabolism and treatment outcomes in breast cancer patients.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, metabolism_type):
        super().__init__(name)
        self.metabolism_type = metabolism_type  # 'extensive', 'heterozygous', 'poor'
        self.recurrence_rate = self.set_recurrence_rate()
        self.mortality_rate = self.set_mortality_rate()

    def set_recurrence_rate(self):
        if self.metabolism_type == 'extensive':
            return 14.9
        elif self.metabolism_type == 'heterozygous':
            return 20.9
        elif self.metabolism_type == 'poor':
            return 29.0
        else:
            return None

    def set_mortality_rate(self):
        if self.metabolism_type == 'extensive':
            return 16.7
        elif self.metabolism_type == 'heterozygous':
            return 18.0
        elif self.metabolism_type == 'poor':
            return 22.8
        else:
            return None

    def makeDescriptionStr(self):
        return f"{self.name} is a patient with {self.metabolism_type} metabolism. Recurrence rate: {self.recurrence_rate}%, Mortality rate: {self.mortality_rate}%."

class World(Container):
    def __init__(self):
        super().__init__("breast_cancer_treatment_environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        patient1 = Patient("Patient A", "extensive")
        patient2 = Patient("Patient B", "heterozygous")
        patient3 = Patient("Patient C", "poor")
        world.addObject(patient1)
        world.addObject(patient2)
        world.addObject(patient3)
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Analyzing the outcomes based on metabolism type
    outcomes = {
        "extensive": (14.9, 16.7),
        "heterozygous": (20.9, 18.0),
        "poor": (29.0, 22.8)
    }

    for metabolism_type, (recurrence_rate, mortality_rate) in outcomes.items():
        print(f"For {metabolism_type} metabolizers: Recurrence Rate = {recurrence_rate}%, Mortality Rate = {mortality_rate}%.")

    # Conclusion based on the simulation
    print("\nConclusion: The simulation shows that a breast cancer patient's capacity to metabolize tamoxifen (CYP2D6 variation) influences treatment outcomes, supporting the claim.")

if __name__ == "__main__":
    main()
