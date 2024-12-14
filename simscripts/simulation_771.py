
# Claim: Metastatic colorectal cancer treated with a single agent fluoropyrimidines resulted in similar efficacy and better quality of life when compared with oxaliplatin-based chemotherapy in elderly patients.

from simulation_utils import GameObject, Container

class Treatment(GameObject):
    def __init__(self, name, efficacy, quality_of_life):
        super().__init__(name)
        self.efficacy = efficacy  # Measured in months of progression-free survival
        self.quality_of_life = quality_of_life  # Percentage of patients reporting improvement in QoL

    def compare(self, other):
        efficacy_comparison = "similar" if self.efficacy == other.efficacy else "better" if self.efficacy > other.efficacy else "worse"
        qol_comparison = "better" if self.quality_of_life > other.quality_of_life else "similar"
        return efficacy_comparison, qol_comparison

class Simulation:
    def __init__(self):
        self.fluoropyrimidines = Treatment("Fluoropyrimidines", efficacy=4.5, quality_of_life=56)  # Example values
        self.oxaliplatin = Treatment("Oxaliplatin-based chemotherapy", efficacy=5.8, quality_of_life=56)  # Example values

    def run(self):
        efficacy_comparison, qol_comparison = self.fluoropyrimidines.compare(self.oxaliplatin)
        if efficacy_comparison == "similar" and qol_comparison == "better":
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
