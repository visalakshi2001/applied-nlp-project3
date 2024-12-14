
# Claim: Varenicline monotherapy is more effective after 26 weeks of treatment compared to combination nicotine replacement therapies with varenicline or bupropion.

from simulation_utils import GameObject, Container

class Treatment(GameObject):
    def __init__(self, name, weeks, abstinence_rate):
        super().__init__(name)
        self.weeks = weeks
        self.abstinence_rate = abstinence_rate

    def makeDescriptionStr(self):
        return f"{self.name} treatment for {self.weeks} weeks with an abstinence rate of {self.abstinence_rate}%."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.verify_claim()

    def _initialize_simulation(self):
        world = Container("treatment_environment")
        varenicline_monotherapy = Treatment("Varenicline Monotherapy", 26, 27.6)  # 27.6% abstinence rate
        combination_therapy = Treatment("Combination Therapy", 26, 36.6)  # 36.6% abstinence rate
        world.addObject(varenicline_monotherapy)
        world.addObject(combination_therapy)
        return world

    def verify_claim(self):
        varenicline_rate = self.rootObject.contains[0].abstinence_rate
        combination_rate = self.rootObject.contains[1].abstinence_rate
        
        if varenicline_rate < combination_rate:
            return "Refuted"
        else:
            return "Supported"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(f"Claim Verification Result: {simulation.result}")

if __name__ == "__main__":
    main()
