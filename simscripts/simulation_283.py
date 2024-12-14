
# Claim: Consumption of whole fruits increases the risk of type 2 diabetes.
# The simulation will evaluate the relationship between whole fruit consumption and type 2 diabetes risk.

from simulation_utils import GameObject, Container

class Fruit(GameObject):
    def __init__(self, name, servings_per_week):
        super().__init__(name)
        self.servings_per_week = servings_per_week
        self.risk_factor = self.calculate_risk_factor()

    def calculate_risk_factor(self):
        # Based on the reference text, we know that greater consumption of specific whole fruits is associated with lower risk
        if self.name in ["blueberries", "grapes", "apples"]:
            return 0.74  # Lower risk
        elif self.name in ["strawberries", "cantaloupe"]:
            return 1.10  # Higher risk
        else:
            return 1.0  # Neutral risk

    def tick(self):
        # Update risk factor based on servings
        if self.servings_per_week > 0:
            self.risk_factor *= (1 - (self.servings_per_week * 0.01))  # Arbitrary adjustment for simulation

class DiabetesRiskAssessment(Container):
    def __init__(self):
        super().__init__("Diabetes Risk Assessment")
        self.fruits = [
            Fruit("blueberries", 3),
            Fruit("grapes", 3),
            Fruit("apples", 3),
            Fruit("strawberries", 3),
            Fruit("cantaloupe", 3)
        ]
        for fruit in self.fruits:
            self.addObject(fruit)

    def assess_risk(self):
        total_risk = 1.0
        for fruit in self.contains:
            total_risk *= fruit.risk_factor
        return total_risk

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        assessment = DiabetesRiskAssessment()
        return assessment

    def run_assessment(self):
        risk = self.rootObject.assess_risk()
        if risk < 1.0:
            return "Supported: Greater consumption of specific whole fruits is associated with a lower risk of type 2 diabetes."
        else:
            return "Refuted: Consumption of whole fruits increases the risk of type 2 diabetes."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.run_assessment()
    print(result)

if __name__ == "__main__":
    main()
