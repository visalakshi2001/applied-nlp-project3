
# Claim: Gastric infection with Helicobacter pylori decreases risk of gastric cancer in humans.
# The simulation will model the relationship between Helicobacter pylori infection and gastric cancer risk.

from simulation_utils import GameObject, Container

class Infection(GameObject):
    def __init__(self, name, is_infected=False):
        super().__init__(name)
        self.is_infected = is_infected

    def tick(self):
        # Simulate the effect of infection on cancer risk
        if self.is_infected:
            self.properties["cancer_risk"] = 2.77  # Odds ratio indicating increased risk
        else:
            self.properties["cancer_risk"] = 1.0  # Baseline risk

    def makeDescriptionStr(self):
        infection_status = "infected" if self.is_infected else "not infected"
        return f"{self.name} is {infection_status} with Helicobacter pylori, cancer risk is {self.properties.get('cancer_risk', 1.0)}."

class CancerRiskSimulation(Container):
    def __init__(self):
        super().__init__("Cancer Risk Simulation Environment")
        self.infection = Infection("Helicobacter pylori Infection", is_infected=True)
        self.addObject(self.infection)

    def makeDescriptionStr(self):
        return f"In the {self.name}, you have: \n" + self.infection.makeDescriptionStr() + "\n"

class Simulation:
    def __init__(self):
        self.rootObject = CancerRiskSimulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def run_simulation(self):
        # Simulate the effect of infection on cancer risk
        self.rootObject.infection.tick()
        self.observationStr += self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
