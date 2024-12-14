
# Claim: Natriuretic peptides protect against diabetes.
# This simulation will analyze the relationship between NT-pro-BNP levels and the risk of type 2 diabetes (T2D).

from simulation_utils import GameObject, Container

class NatriureticPeptide(GameObject):
    def __init__(self, name, level):
        super().__init__(name)
        self.properties = {
            "level": level,  # NT-pro-BNP level
            "risk_decrease": 0.21  # 21% decreased risk of T2D per SD increase
        }

    def calculate_diabetes_risk(self):
        # Calculate the risk of diabetes based on NT-pro-BNP level
        risk = 1 - self.properties["risk_decrease"] * self.properties["level"]
        return risk

class Population(Container):
    def __init__(self):
        super().__init__("Population")
        self.natriuretic_peptides = []

    def add_natriuretic_peptide(self, peptide):
        self.addObject(peptide)
        self.natriuretic_peptides.append(peptide)

    def analyze_risk(self):
        results = []
        for peptide in self.natriuretic_peptides:
            risk = peptide.calculate_diabetes_risk()
            results.append((peptide.name, risk))
        return results

class Simulation:
    def __init__(self):
        self.population = self._initialize_simulation()
        self.results = self.population.analyze_risk()

    def _initialize_simulation(self):
        population = Population()
        # Simulating different levels of NT-pro-BNP in the population
        population.add_natriuretic_peptide(NatriureticPeptide("Peptide A", 1))  # 1 SD increase
        population.add_natriuretic_peptide(NatriureticPeptide("Peptide B", 2))  # 2 SD increase
        return population

def main():
    simulation = Simulation()
    for peptide_name, risk in simulation.results:
        print(f"{peptide_name} has a diabetes risk of {risk:.2f}")

    # Check if the claim is supported or refuted based on the results
    if all(risk < 1 for _, risk in simulation.results):
        print("Claim Supported: Natriuretic peptides protect against diabetes.")
    else:
        print("Claim Refuted: Natriuretic peptides do not protect against diabetes.")

if __name__ == "__main__":
    main()
