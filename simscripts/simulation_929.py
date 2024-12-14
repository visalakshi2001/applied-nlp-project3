
# Claim: Patients with microcytosis and higher erythrocyte count were more resistant to severe malarial anaemia when infected with Plasmodium falciparum.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, microcytosis, erythrocyte_count, has_severe_malarial_anaemia):
        super().__init__(name)
        self.properties = {
            "microcytosis": microcytosis,
            "erythrocyte_count": erythrocyte_count,
            "has_severe_malarial_anaemia": has_severe_malarial_anaemia
        }

    def assess_resistance(self):
        # Patients with microcytosis and higher erythrocyte count are more resistant
        if self.properties["microcytosis"] and self.properties["erythrocyte_count"] > 5.0:  # Arbitrary threshold for higher count
            return "resistant"
        else:
            return "not resistant"

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.results = self.evaluate_patients()

    def _initialize_simulation(self):
        # Create patients with different properties
        patient1 = Patient("Patient A", True, 6.0, False)  # Microcytosis, higher erythrocyte count
        patient2 = Patient("Patient B", True, 4.5, True)   # Microcytosis, lower erythrocyte count
        patient3 = Patient("Patient C", False, 5.5, True)  # No microcytosis, higher erythrocyte count
        patient4 = Patient("Patient D", True, 5.0, True)   # Microcytosis, borderline erythrocyte count

        return [patient1, patient2, patient3, patient4]

    def evaluate_patients(self):
        results = {}
        for patient in self.patients:
            resistance_status = patient.assess_resistance()
            results[patient.name] = {
                "resistance_status": resistance_status,
                "has_severe_malarial_anaemia": patient.properties["has_severe_malarial_anaemia"]
            }
        return results

def main():
    simulation = Simulation()
    for patient_name, result in simulation.results.items():
        print(f"{patient_name}: Resistance Status - {result['resistance_status']}, Has Severe Malarial Anaemia - {result['has_severe_malarial_anaemia']}")

    # Check if the claim is supported or refuted
    claim_supported = all(result['resistance_status'] == "resistant" for result in simulation.results.values() if result['has_severe_malarial_anaemia'])
    if claim_supported:
        print("Claim Supported: Patients with microcytosis and higher erythrocyte count are more resistant to severe malarial anaemia.")
    else:
        print("Claim Refuted: Not all patients with microcytosis and higher erythrocyte count are resistant to severe malarial anaemia.")

if __name__ == "__main__":
    main()
