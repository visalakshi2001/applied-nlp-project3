
# Claim: Systemic immunosuppressive (IS) therapy increases the chance of cancer mortality in patients with inflammatory eye disease (IED)

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, is_immunosuppressive=False, cancer_mortality_rate=0):
        super().__init__(name)
        self.is_immunosuppressive = is_immunosuppressive
        self.cancer_mortality_rate = cancer_mortality_rate

    def tick(self):
        # Simulate the effect of immunosuppressive therapy on cancer mortality
        if self.is_immunosuppressive:
            # If the patient is on immunosuppressive therapy, increase cancer mortality rate
            self.cancer_mortality_rate += 0.1  # Arbitrary increase for simulation purposes

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.results = self.evaluate_mortality()

    def _initialize_simulation(self):
        # Create a group of patients, some with and some without immunosuppressive therapy
        patients = []
        for i in range(100):  # Total of 100 patients
            if i < 50:  # First 50 patients are on immunosuppressive therapy
                patients.append(Patient(f"Patient_{i}", is_immunosuppressive=True))
            else:  # Last 50 patients are not on immunosuppressive therapy
                patients.append(Patient(f"Patient_{i}", is_immunosuppressive=False))
        return patients

    def evaluate_mortality(self):
        # Evaluate cancer mortality rates
        cancer_mortality_with_IS = sum(p.cancer_mortality_rate for p in self.patients if p.is_immunosuppressive)
        cancer_mortality_without_IS = sum(p.cancer_mortality_rate for p in self.patients if not p.is_immunosuppressive)
        
        # Return the results for comparison
        return {
            "with_IS": cancer_mortality_with_IS,
            "without_IS": cancer_mortality_without_IS
        }

def main():
    simulation = Simulation()
    results = simulation.results
    print(f"Cancer mortality with immunosuppressive therapy: {results['with_IS']}")
    print(f"Cancer mortality without immunosuppressive therapy: {results['without_IS']}")

    # Determine if the claim is supported or refuted
    if results['with_IS'] > results['without_IS']:
        print("Claim Supported: Systemic immunosuppressive therapy increases the chance of cancer mortality.")
    else:
        print("Claim Refuted: Systemic immunosuppressive therapy does not increase the chance of cancer mortality.")

if __name__ == "__main__":
    main()
