
# Claim: The relationship between a breast cancer patient's capacity to metabolize tamoxifen and treatment outcome is independent of the patient's genetic make-up.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, CYP2D6_genotype, tamoxifen_metabolism):
        super().__init__(name)
        self.properties = {
            "CYP2D6_genotype": CYP2D6_genotype,  # Genotype of the patient
            "tamoxifen_metabolism": tamoxifen_metabolism,  # Metabolism level (extensive, intermediate, poor)
            "recurrence_rate": 0.0,  # Recurrence rate based on metabolism
            "event_free_survival": 0.0,  # Event-free survival based on metabolism
            "disease_free_survival": 0.0,  # Disease-free survival based on metabolism
        }

    def calculate_outcomes(self):
        # Simulating outcomes based on CYP2D6 genotype
        if self.properties["tamoxifen_metabolism"] == "extensive":
            self.properties["recurrence_rate"] = 14.9
            self.properties["event_free_survival"] = 1.0  # 100% event-free survival
            self.properties["disease_free_survival"] = 1.0  # 100% disease-free survival
        elif self.properties["tamoxifen_metabolism"] == "intermediate":
            self.properties["recurrence_rate"] = 20.9
            self.properties["event_free_survival"] = 0.75  # 75% event-free survival
            self.properties["disease_free_survival"] = 0.75  # 75% disease-free survival
        elif self.properties["tamoxifen_metabolism"] == "poor":
            self.properties["recurrence_rate"] = 29.0
            self.properties["event_free_survival"] = 0.5  # 50% event-free survival
            self.properties["disease_free_survival"] = 0.5  # 50% disease-free survival

class Simulation:
    def __init__(self):
        self.patients = [
            Patient("Patient A", "CYP2D6*1/*1", "extensive"),
            Patient("Patient B", "CYP2D6*10/*1", "intermediate"),
            Patient("Patient C", "CYP2D6*3/*4", "poor"),
        ]
        self.results = []

    def run_simulation(self):
        for patient in self.patients:
            patient.calculate_outcomes()
            self.results.append({
                "name": patient.name,
                "recurrence_rate": patient.properties["recurrence_rate"],
                "event_free_survival": patient.properties["event_free_survival"],
                "disease_free_survival": patient.properties["disease_free_survival"],
            })

    def analyze_results(self):
        # Analyzing the results to determine if the claim is supported or refuted
        extensive = self.results[0]["recurrence_rate"]
        intermediate = self.results[1]["recurrence_rate"]
        poor = self.results[2]["recurrence_rate"]

        if (intermediate > extensive) and (poor > extensive):
            return "Refuted: The outcomes are dependent on the patient's genetic make-up."
        else:
            return "Supported: The outcomes are independent of the patient's genetic make-up."

def main():
    simulation = Simulation()
    simulation.run_simulation()
    result = simulation.analyze_results()
    print(result)

if __name__ == "__main__":
    main()
