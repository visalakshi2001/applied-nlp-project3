
# Claim: There is no known interaction between Pioneer factor OCT3/4 and major chromatin remodeling factors.
# The simulation will check for interactions between OCT3/4 and chromatin remodeling factors.

from simulation_utils import GameObject, Container

class Protein(GameObject):
    def __init__(self, name, interacts_with=None):
        super().__init__(name)
        self.interacts_with = interacts_with if interacts_with else []

    def add_interaction(self, protein):
        self.interacts_with.append(protein)

    def check_interaction(self, protein):
        return protein in self.interacts_with

class Oct4(Protein):
    def __init__(self):
        super().__init__("OCT3/4")

class ChromatinRemodelingFactor(Protein):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.oct4 = Oct4()
        self.chromatin_factors = [
            ChromatinRemodelingFactor("SWI/SNF"),
            ChromatinRemodelingFactor("ISWI"),
            ChromatinRemodelingFactor("CHD"),
            ChromatinRemodelingFactor("INO80")
        ]
        self.setup_interactions()

    def setup_interactions(self):
        # According to the reference text, Oct4 interacts with several proteins
        # Here we simulate that it does interact with some chromatin remodeling factors
        self.oct4.add_interaction(self.chromatin_factors[0])  # SWI/SNF

    def check_claim(self):
        # Check if OCT3/4 interacts with any major chromatin remodeling factors
        for factor in self.chromatin_factors:
            if self.oct4.check_interaction(factor):
                return "Refuted: OCT3/4 interacts with chromatin remodeling factor " + factor.name
        return "Supported: No interactions found between OCT3/4 and chromatin remodeling factors."

def main():
    simulation = Simulation()
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
