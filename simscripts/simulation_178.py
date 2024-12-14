
# Claim: Birth-weight is negatively associated with breast cancer.
# The simulation will analyze the relationship between birth weight and breast cancer risk.

from simulation_utils import GameObject, Container

class BirthWeight(GameObject):
    def __init__(self, weight):
        super().__init__("BirthWeight")
        self.weight = weight  # in kg
        self.breast_cancer_risk = self.calculate_risk()

    def calculate_risk(self):
        # Simulating the risk based on weight
        if self.weight < 2.5:
            return 0.96  # Lower risk
        elif 3.0 <= self.weight <= 3.5:
            return 1.0  # Baseline risk
        else:
            return 1.12  # Higher risk

    def makeDescriptionStr(self):
        return f"Birth weight: {self.weight} kg, Breast cancer risk: {self.breast_cancer_risk}"

class BreastCancerRiskSimulation(Container):
    def __init__(self):
        super().__init__("BreastCancerRiskSimulation")
        self.birth_weights = [2.4, 3.0, 3.5, 4.0]  # Different birth weights
        self.results = []

        for weight in self.birth_weights:
            birth_weight_obj = BirthWeight(weight)
            self.addObject(birth_weight_obj)
            self.results.append(birth_weight_obj.breast_cancer_risk)

    def analyze_results(self):
        # Analyzing the results to determine if the claim is supported or refuted
        if all(risk >= 1.0 for risk in self.results[1:]):  # Check if higher weights have higher risks
            return "Claim Refuted: Birth-weight is positively associated with breast cancer."
        else:
            return "Claim Supported: Birth-weight is negatively associated with breast cancer."

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

def main():
    simulation = BreastCancerRiskSimulation()
    print(simulation.makeDescriptionStr())
    result = simulation.analyze_results()
    print(result)

if __name__ == "__main__":
    main()
