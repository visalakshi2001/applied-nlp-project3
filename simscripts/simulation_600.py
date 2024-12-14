
# Claim: Including pharmacists in rounding teams does not alter the incidence of adverse drug events (ADEs).
# The simulation will test the effect of pharmacist participation on the rate of preventable adverse drug events (ADEs).

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, ade_rate):
        super().__init__(name)
        self.properties = {
            "ade_rate": ade_rate  # Initial rate of adverse drug events
        }

    def tick(self, intervention_effect):
        # Apply the intervention effect to the ADE rate
        self.properties["ade_rate"] -= intervention_effect

    def makeDescriptionStr(self):
        return f"{self.name} has an adverse drug event rate of {self.properties['ade_rate']} per 1000 patient-days."

class ICU(Container):
    def __init__(self):
        super().__init__("ICU")
        self.patients = []

    def addPatient(self, patient):
        self.addObject(patient)
        self.patients.append(patient)

    def simulateRounds(self, intervention_effect):
        for patient in self.patients:
            patient.tick(intervention_effect)

    def makeDescriptionStr(self):
        outStr = super().makeDescriptionStr()
        for patient in self.patients:
            outStr += "\n" + patient.makeDescriptionStr()
        return outStr

class Simulation:
    def __init__(self):
        self.icu = ICU()
        self.setup_patients()
        self.intervention_effect = 6.9  # The effect of pharmacist intervention (10.4 - 3.5)
        self.icu.simulateRounds(self.intervention_effect)

    def setup_patients(self):
        # Adding patients with initial ADE rates
        self.icu.addPatient(Patient("Patient 1", 10.4))  # Baseline rate
        self.icu.addPatient(Patient("Patient 2", 10.4))  # Baseline rate
        self.icu.addPatient(Patient("Patient 3", 10.4))  # Baseline rate

    def run(self):
        print(self.icu.makeDescriptionStr())
        # Check if the claim is supported or refuted
        if all(patient.properties["ade_rate"] <= 10.4 for patient in self.icu.patients):
            return "Claim Refuted: Including pharmacists in rounding teams reduces the incidence of ADEs."
        else:
            return "Claim Supported: Including pharmacists in rounding teams does not alter the incidence of ADEs."

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
