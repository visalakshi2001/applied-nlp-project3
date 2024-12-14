
# Claim: Stroke patients with prior use of direct oral anticoagulants have a higher risk of in-hospital mortality than stroke patients with prior use of warfarin.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, anticoagulant_type, in_hospital_mortality_rate):
        super().__init__(name)
        self.anticoagulant_type = anticoagulant_type
        self.in_hospital_mortality_rate = in_hospital_mortality_rate

    def makeDescriptionStr(self):
        return f"{self.name} is a patient taking {self.anticoagulant_type} with an in-hospital mortality rate of {self.in_hospital_mortality_rate}%."

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.result = self.compare_mortality_rates()

    def _initialize_simulation(self):
        # Initialize patients with their anticoagulant type and mortality rates
        warfarin_patient = Patient("Warfarin Patient", "Warfarin", 32.6)
        noac_patient = Patient("NOAC Patient", "NOAC", 26.5)
        return [warfarin_patient, noac_patient]

    def compare_mortality_rates(self):
        warfarin_mortality = self.patients[0].in_hospital_mortality_rate
        noac_mortality = self.patients[1].in_hospital_mortality_rate
        
        if noac_mortality < warfarin_mortality:
            return "Refuted: Patients with prior use of NOACs have a lower risk of in-hospital mortality than those with warfarin."
        else:
            return "Supported: Patients with prior use of NOACs have a higher risk of in-hospital mortality than those with warfarin."

def main():
    simulation = Simulation()
    print(simulation.result)

if __name__ == "__main__":
    main()
