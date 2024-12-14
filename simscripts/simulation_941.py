
# Claim: Pharmacist attendance at ward rounds reduces adverse events in wards.
# The simulation will model the effect of pharmacist participation on the rate of preventable adverse drug events (ADEs).

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, ad_event_rate):
        super().__init__(name)
        self.ad_event_rate = ad_event_rate  # Rate of adverse drug events per 1000 patient-days

    def tick(self, intervention):
        if intervention:
            # Simulate the effect of pharmacist intervention reducing ADEs by 66%
            self.ad_event_rate *= 0.34  # 66% reduction
        else:
            # No intervention, rate remains the same
            pass

    def makeDescriptionStr(self):
        return f"{self.name} has an adverse event rate of {self.ad_event_rate:.2f} per 1000 patient-days."

class ICU(Container):
    def __init__(self):
        super().__init__("ICU")
        self.patients = []

    def addPatient(self, patient):
        self.addObject(patient)

    def simulateRound(self, intervention):
        for patient in self.contains:
            patient.tick(intervention)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see:\n"
        for patient in self.contains:
            outStr += "\t" + patient.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.icu = ICU()
        self.initialize_patients()
        self.intervention = False  # Initially no intervention

    def initialize_patients(self):
        # Initialize patients with baseline adverse event rates
        self.icu.addPatient(Patient("Patient 1", 10.4))
        self.icu.addPatient(Patient("Patient 2", 10.9))
        self.icu.addPatient(Patient("Patient 3", 12.4))

    def run_simulation(self):
        # Simulate before intervention
        print("Before intervention:")
        print(self.icu.makeDescriptionStr())

        # Simulate intervention (pharmacist attendance)
        self.intervention = True
        self.icu.simulateRound(self.intervention)

        # Simulate after intervention
        print("After intervention:")
        print(self.icu.makeDescriptionStr())

def main():
    simulation = Simulation()
    simulation.run_simulation()

if __name__ == "__main__":
    main()
