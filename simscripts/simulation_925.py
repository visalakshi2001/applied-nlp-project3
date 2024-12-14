
# Claim: Patients in stable partnerships progress from HIV to death at the same rate as patients not in partnerships.
# The simulation will compare the progression rates of patients in stable partnerships versus those not in partnerships.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, in_stable_partnership, progression_rate):
        super().__init__(name)
        self.properties = {
            "in_stable_partnership": in_stable_partnership,
            "progression_rate": progression_rate,  # Rate of progression to death
            "time_to_death": 0  # Time until death
        }

    def tick(self):
        self.properties["time_to_death"] += self.properties["progression_rate"]

    def makeDescriptionStr(self):
        partnership_status = "in a stable partnership" if self.properties["in_stable_partnership"] else "not in a stable partnership"
        return f"{self.name}, who is {partnership_status}, has progressed for {self.properties['time_to_death']} time units."

class World(Container):
    def __init__(self):
        super().__init__("HIV Patient Environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.simulation_steps = 10  # Number of simulation steps to run

    def _initialize_simulation(self):
        world = World()
        # Create patients with different progression rates
        patient1 = Patient("Patient A", True, 0.79)  # In stable partnership
        patient2 = Patient("Patient B", False, 1.0)  # Not in stable partnership
        world.addObject(patient1)
        world.addObject(patient2)
        return world

    def run_simulation(self):
        for _ in range(self.simulation_steps):
            for patient in self.rootObject.getAllContainedObjectsRecursive():
                patient.tick()
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print("Initial State:")
    print(simulation.observationStr)
    print("Running Simulation...")
    final_state = simulation.run_simulation()
    print("Final State After Simulation:")
    print(final_state)

    # Determine if the claim is supported or refuted
    patient_a_time = simulation.rootObject.contains[0].properties["time_to_death"]
    patient_b_time = simulation.rootObject.contains[1].properties["time_to_death"]

    if patient_a_time < patient_b_time:
        print("Claim Refuted: Patients in stable partnerships progress slower than those not in partnerships.")
    else:
        print("Claim Supported: Patients in stable partnerships progress at the same rate as those not in partnerships.")

if __name__ == "__main__":
    main()
