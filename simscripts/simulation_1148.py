
# Claim: Ten percent (10%) of kidney cancers in the UK are attributable to excess weight.
# The simulation will check if the claim is supported by the evidence provided in the reference text.

from simulation_utils import GameObject, Container

class CancerRisk(GameObject):
    def __init__(self, name, attributable_percentage=0):
        super().__init__(name)
        self.attributable_percentage = attributable_percentage

    def makeDescriptionStr(self):
        return f"{self.name} has an attributable percentage of {self.attributable_percentage}% to excess weight."

class Population(Container):
    def __init__(self):
        super().__init__("UK Population")
        self.kidney_cancer = CancerRisk("Kidney Cancer", 10)  # Setting the attributable percentage to 10%

    def makeDescriptionStr(self):
        outStr = super().makeDescriptionStr()
        outStr += f"\nIn the {self.name}, we have:\n"
        outStr += f"\t{self.kidney_cancer.makeDescriptionStr()}\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        population = Population()
        return population

    def check_claim(self):
        # Check if the kidney cancer attributable percentage is 10% or more
        if self.rootObject.kidney_cancer.attributable_percentage >= 10:
            return "Claim Supported: The claim that 10% of kidney cancers in the UK are attributable to excess weight is supported."
        else:
            return "Claim Refuted: The claim is not supported."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
