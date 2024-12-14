
# Claim: Sildenafil worsens erectile function in men who experience sexual dysfunction as a result of the use of SSRI antidepressants.
# The simulation will assess the effects of sildenafil on erectile function in men with sexual dysfunction due to SSRI use.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, erectile_function=0, on_ssri=False):
        super().__init__(name)
        self.properties = {
            "erectile_function": erectile_function,  # Scale from 0 (worst) to 10 (best)
            "on_ssri": on_ssri,  # Whether the patient is on SSRI antidepressants
            "treatment": None  # Treatment received (sildenafil or placebo)
        }

    def receive_treatment(self, treatment):
        self.properties["treatment"] = treatment
        if treatment == "sildenafil":
            self.properties["erectile_function"] += 5  # Sildenafil improves erectile function
        elif treatment == "placebo":
            self.properties["erectile_function"] += 1  # Placebo has minimal effect

    def makeDescriptionStr(self):
        return f"{self.name} has an erectile function score of {self.properties['erectile_function']}."

class Simulation:
    def __init__(self):
        self.patients = self._initialize_simulation()
        self.results = self.evaluate_treatment()

    def _initialize_simulation(self):
        # Create patients with sexual dysfunction due to SSRI use
        patient1 = Patient("Patient 1", erectile_function=2, on_ssri=True)  # Low erectile function
        patient2 = Patient("Patient 2", erectile_function=3, on_ssri=True)  # Low erectile function
        patient3 = Patient("Patient 3", erectile_function=5, on_ssri=True)  # Moderate erectile function
        return [patient1, patient2, patient3]

    def evaluate_treatment(self):
        # Treat half with sildenafil and half with placebo
        for i, patient in enumerate(self.patients):
            if i % 2 == 0:
                patient.receive_treatment("sildenafil")
            else:
                patient.receive_treatment("placebo")
        return [(patient.name, patient.properties["erectile_function"]) for patient in self.patients]

def main():
    simulation = Simulation()
    results = simulation.results
    for name, score in results:
        print(f"{name}: Erectile function score after treatment is {score}.")
    
    # Check if the claim is supported or refuted
    if all(score >= 5 for _, score in results if score > 3):  # If all treated with sildenafil improved significantly
        print("Claim is Refuted: Sildenafil does not worsen erectile function.")
    else:
        print("Claim is Supported: Sildenafil improves erectile function.")

if __name__ == "__main__":
    main()
