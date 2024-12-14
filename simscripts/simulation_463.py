
# Claim: Genomic aberrations of metastases provide information for targeted therapy.
# The simulation will model the relationship between genetic mutations in tumors and their implications for targeted therapy.

from simulation_utils import GameObject, Container

class Tumor(GameObject):
    def __init__(self, name, mutations=None):
        super().__init__(name)
        self.mutations = mutations if mutations is not None else []

    def addMutation(self, mutation):
        self.mutations.append(mutation)

    def makeDescriptionStr(self):
        mutation_str = ", ".join(self.mutations) if self.mutations else "no mutations"
        return f"A {self.name} with mutations: {mutation_str}."

class Metastasis(Tumor):
    def __init__(self, name, mutations=None):
        super().__init__(name, mutations)

class PrimaryTumor(Tumor):
    def __init__(self, name, mutations=None):
        super().__init__(name, mutations)

class Simulation:
    def __init__(self):
        self.primary_tumor = PrimaryTumor("Primary Tumor", ["A-to-T", "G-to-T"])
        self.metastasis = Metastasis("Metastasis", ["G-to-T"])
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("Tumor Environment")
        world.addObject(self.primary_tumor)
        world.addObject(self.metastasis)
        return world

    def makeDescriptionStr(self):
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())
    
    # Check if the claim is supported
    if "A-to-T" in simulation.primary_tumor.mutations and "G-to-T" in simulation.metastasis.mutations:
        result = "Supported"
    else:
        result = "Refuted"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
