
# Claim: Systemic immunosuppressive (IS) therapy does not enhance the chance of cancer mortality in patients with inflammatory eye disease (IED)

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, immunosuppressive_drug=None, cancer_mortality_rate=0):
        super().__init__(name)
        self.immunosuppressive_drug = immunosuppressive_drug
        self.cancer_mortality_rate = cancer_mortality_rate

    def assess_mortality(self):
        if self.immunosuppressive_drug:
            if self.immunosuppressive_drug in ["azathioprine", "methotrexate", "mycophenolate mofetil", "ciclosporin", "systemic corticosteroids", "dapsone"]:
                self.cancer_mortality_rate = 1.0  # Similar to non-users
            elif self.immunosuppressive_drug == "tumour necrosis factor inhibitors":
                self.cancer_mortality_rate = 3.83  # Increased risk
            else:
                self.cancer_mortality_rate = 1.0  # Default to non-increased risk
        else:
            self.cancer_mortality_rate = 1.0  # No drug, no increased risk

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.results = self.assess_mortality()

    def _initialize_simulation(self):
        # Create patients with different drug exposures
        patient1 = Patient("Patient 1", "azathioprine")
        patient2 = Patient("Patient 2", "tumour necrosis factor inhibitors")
        patient3 = Patient("Patient 3", None)  # No drug
        return [patient1, patient2, patient3]

    def assess_mortality(self):
        results = {}
        for patient in self.patients:
            patient.assess_mortality()
            results[patient.name] = patient.cancer_mortality_rate
        return results

def main():
    simulation = Simulation()
    print("Cancer Mortality Rates:")
    for patient, rate in simulation.results.items():
        print(f"{patient}: {rate}")

    # Determine if the claim is supported or refuted
    if all(rate <= 1.0 for rate in simulation.results.values()):
        print("Claim Supported: Systemic immunosuppressive therapy does not enhance the chance of cancer mortality.")
    else:
        print("Claim Refuted: Systemic immunosuppressive therapy enhances the chance of cancer mortality.")

if __name__ == "__main__":
    main()
