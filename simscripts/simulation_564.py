
# Claim: In British Men, haplogroup I increases risk of cardiovascular disease by 50%.

from simulation_utils import GameObject, Container

class Man(GameObject):
    def __init__(self, name, haplogroup, age_adjusted_risk):
        super().__init__(name)
        self.haplogroup = haplogroup
        self.age_adjusted_risk = age_adjusted_risk

    def makeDescriptionStr(self):
        return f"{self.name} with haplogroup {self.haplogroup} has an age-adjusted risk of {self.age_adjusted_risk} for cardiovascular disease."

class Study(Container):
    def __init__(self, name):
        super().__init__(name)

    def calculate_risk_increase(self, haplogroup):
        if haplogroup == "I":
            return 1.5  # 50% increase
        else:
            return 1.0  # baseline risk

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        study = Study("Cardiovascular Disease Study")
        man1 = Man("British Man 1", "I", 1.75)  # Risk for haplogroup I
        man2 = Man("British Man 2", "R1b1b2", 1.0)  # Baseline risk for other haplogroup
        study.addObject(man1)
        study.addObject(man2)
        return study

    def check_claim(self):
        man1 = self.rootObject.contains[0]  # British Man 1
        man2 = self.rootObject.contains[1]  # British Man 2
        risk_increase = man1.age_adjusted_risk / man2.age_adjusted_risk
        if risk_increase >= 1.5:
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
