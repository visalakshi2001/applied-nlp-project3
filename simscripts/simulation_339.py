
# Claim: Dexamethasone increases risk of postoperative bleeding.
# The simulation will model the effect of dexamethasone on postoperative bleeding risk in children undergoing tonsillectomy.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, dexamethasone_dose=0):
        super().__init__(name)
        self.dexamethasone_dose = dexamethasone_dose
        self.properties = {
            "bleeding_risk": self.calculate_bleeding_risk()
        }

    def calculate_bleeding_risk(self):
        # Risk increases with the dose of dexamethasone
        if self.dexamethasone_dose == 0:
            return 4  # 4% risk for placebo
        elif self.dexamethasone_dose == 0.05:
            return 11  # 11% risk for 0.05 mg/kg
        elif self.dexamethasone_dose == 0.15:
            return 24  # 24% risk for 0.15 mg/kg
        elif self.dexamethasone_dose == 0.5:
            return 24  # 24% risk for 0.5 mg/kg
        return 0

    def tick(self):
        # Update bleeding risk based on the current dose
        self.properties["bleeding_risk"] = self.calculate_bleeding_risk()

    def makeDescriptionStr(self):
        return f"{self.name} with dexamethasone dose {self.dexamethasone_dose} mg/kg has a bleeding risk of {self.properties['bleeding_risk']}%."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("hospital")
        # Create patients with different doses of dexamethasone
        patient_placebo = Patient("Patient Placebo", 0)
        patient_low = Patient("Patient Low Dose", 0.05)
        patient_medium = Patient("Patient Medium Dose", 0.15)
        patient_high = Patient("Patient High Dose", 0.5)

        world.addObject(patient_placebo)
        world.addObject(patient_low)
        world.addObject(patient_medium)
        world.addObject(patient_high)

        return world

    def step(self):
        # Simulate a tick to update the state of the patients
        allPatients = self.rootObject.getAllContainedObjectsRecursive()
        for patient in allPatients:
            patient.tick()
        self.observationStr = self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    simulation.step()
    print("After simulation step:")
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
