
# Claim: In British Men, haplogroup I decreases risk of cardiovascular disease.
# The simulation will evaluate the relationship between haplogroup I and cardiovascular disease risk.

from simulation_utils import GameObject, Container

class Man(GameObject):
    def __init__(self, name, haplogroup, age_adjusted_risk):
        super().__init__(name)
        self.haplogroup = haplogroup
        self.age_adjusted_risk = age_adjusted_risk  # Higher value indicates higher risk

    def makeDescriptionStr(self):
        return f"{self.name} with haplogroup {self.haplogroup} has an age-adjusted risk of {self.age_adjusted_risk} for cardiovascular disease."

class Population(Container):
    def __init__(self, name):
        super().__init__(name)

    def calculate_average_risk(self):
        total_risk = 0
        count = 0
        for man in self.contains:
            total_risk += man.age_adjusted_risk
            count += 1
        return total_risk / count if count > 0 else 0

class Simulation:
    def __init__(self):
        self.population = self._initialize_simulation()
        self.observationStr = self.population.makeDescriptionStr()
        self.average_risk = self.population.calculate_average_risk()

    def _initialize_simulation(self):
        population = Population("British Men")
        # Adding men with different haplogroups and their associated risks
        population.addObject(Man("Man 1", "I", 1.75))  # Higher risk for haplogroup I
        population.addObject(Man("Man 2", "R1b1b2", 1.0))  # Lower risk for other haplogroup
        population.addObject(Man("Man 3", "I", 1.56))  # Another man with haplogroup I
        population.addObject(Man("Man 4", "R1b1b2", 1.0))  # Another man with lower risk
        return population

    def evaluate_claim(self):
        # If the average risk of haplogroup I is higher than others, the claim is refuted
        haplogroup_I_risk = sum(man.age_adjusted_risk for man in self.population.contains if man.haplogroup == "I")
        other_haplogroup_risk = sum(man.age_adjusted_risk for man in self.population.contains if man.haplogroup != "I")
        
        if haplogroup_I_risk > other_haplogroup_risk:
            return "Claim Refuted: Haplogroup I is associated with increased risk of cardiovascular disease."
        else:
            return "Claim Supported: Haplogroup I is associated with decreased risk of cardiovascular disease."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.evaluate_claim()
    print(result)

if __name__ == "__main__":
    main()
