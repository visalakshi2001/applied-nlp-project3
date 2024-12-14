
# Claim: A deficiency of folate increases blood levels of homocysteine.
# This simulation will test the relationship between folate dosage and homocysteine levels.

from simulation_utils import GameObject, Container

class Folate(GameObject):
    def __init__(self, dosage=0):
        super().__init__("Folate")
        self.dosage = dosage  # Dosage in mg/d
        self.homocysteine_level = 10  # Baseline homocysteine level in micromol/L

    def tick(self):
        # The effect of folate on homocysteine levels
        if self.dosage > 0:
            reduction = min(self.dosage * 3, self.homocysteine_level)  # Arbitrary reduction factor
            self.homocysteine_level -= reduction

class Patient(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.folate = Folate()
    
    def set_folate_dosage(self, dosage):
        self.folate.dosage = dosage

    def get_homocysteine_level(self):
        return self.folate.homocysteine_level

class Simulation:
    def __init__(self):
        self.patient = Patient("Patient 1")
        self.results = []

    def run_simulation(self, dosages):
        for dosage in dosages:
            self.patient.set_folate_dosage(dosage)
            self.patient.folate.tick()  # Update homocysteine level based on folate dosage
            self.results.append((dosage, self.patient.get_homocysteine_level()))

    def analyze_results(self):
        for i in range(1, len(self.results)):
            if self.results[i][1] < self.results[i-1][1]:
                continue
            else:
                return "Refuted: Homocysteine levels did not decrease with increased folate dosage."
        return "Supported: Homocysteine levels decreased with increased folate dosage."

def main():
    simulation = Simulation()
    dosages = [0, 0.2, 0.4, 0.6, 0.8, 1.0]  # Different dosages of folate
    simulation.run_simulation(dosages)
    result = simulation.analyze_results()
    print(result)

if __name__ == "__main__":
    main()
