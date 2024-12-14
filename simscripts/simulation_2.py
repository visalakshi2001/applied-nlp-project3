
# Claim: 1 in 5 million in UK have abnormal PrP positivity.
# The simulation will check the prevalence of abnormal PrP positivity based on the provided reference text.

from simulation_utils import GameObject, Container

class PrPPositiveSample(GameObject):
    def __init__(self, name, total_samples, positive_samples):
        super().__init__(name)
        self.total_samples = total_samples
        self.positive_samples = positive_samples
        self.prevalence_per_million = (positive_samples / total_samples) * 1_000_000

    def makeDescriptionStr(self):
        return f"{self.name}: Total samples = {self.total_samples}, Positive samples = {self.positive_samples}, Prevalence = {self.prevalence_per_million:.2f} per million."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("UK PrP Sample Survey")
        # Based on the reference text, we have 32,441 samples with 16 positive for abnormal PrP
        total_samples = 32441
        positive_samples = 16
        prp_sample = PrPPositiveSample("PrP Positive Sample", total_samples, positive_samples)
        world.addObject(prp_sample)
        return world

    def check_claim(self):
        prp_sample = self.rootObject.contains[0]  # Get the PrPPositiveSample object
        prevalence = prp_sample.prevalence_per_million
        if prevalence == 493:
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
