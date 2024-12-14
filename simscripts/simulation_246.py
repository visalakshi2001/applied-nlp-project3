
# Claim: Charcoal shows no benefit for acute paraquat poisoning.
# The simulation will analyze the effect of activated charcoal hemoperfusion on renal function and paraquat elimination.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, renal_function_normal=True, survived=True):
        super().__init__(name)
        self.properties = {
            "renal_function_normal": renal_function_normal,
            "survived": survived,
            "activated_charcoal_effect": None
        }

    def apply_activated_charcoal(self):
        # Simulate the effect of activated charcoal
        if self.properties["renal_function_normal"]:
            self.properties["activated_charcoal_effect"] = "little effect"
        else:
            self.properties["activated_charcoal_effect"] = "no benefit"

    def makeDescriptionStr(self):
        return f"{self.name}: Renal function normal: {self.properties['renal_function_normal']}, Survived: {self.properties['survived']}, Activated charcoal effect: {self.properties['activated_charcoal_effect']}."

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.observationStr = self.makeObservationStr()

    def _initialize_simulation(self):
        # Create patients based on the reference text
        patient1 = Patient("Patient 1", renal_function_normal=False, survived=False)  # Died with non-oliguric renal failure
        patient2 = Patient("Patient 2", renal_function_normal=True, survived=True)    # Survived with normal renal function
        patient3 = Patient("Patient 3", renal_function_normal=True, survived=True)    # Survived with normal renal function
        patient4 = Patient("Patient 4", renal_function_normal=False, survived=False)  # Died with non-oliguric renal failure
        return [patient1, patient2, patient3, patient4]

    def apply_treatment(self):
        for patient in self.patients:
            patient.apply_activated_charcoal()

    def makeObservationStr(self):
        outStr = "Simulation Results:\n"
        for patient in self.patients:
            outStr += patient.makeDescriptionStr() + "\n"
        return outStr

def main():
    simulation = Simulation()
    simulation.apply_treatment()
    print(simulation.makeObservationStr())

if __name__ == "__main__":
    main()
