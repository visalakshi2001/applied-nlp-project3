
# Claim: Nonhypertensive people who are 55 years old have a 90% chance of developing hypertension during their lifetime.
# The simulation will check the lifetime risk of developing hypertension for 55-year-old individuals.

from simulation_utils import GameObject, Container

class Individual(GameObject):
    def __init__(self, age, has_hypertension=False):
        super().__init__(f"Individual aged {age}")
        self.age = age
        self.has_hypertension = has_hypertension
        self.lifetime_hypertension_risk = 0.9  # 90% risk as per the claim

    def develop_hypertension(self):
        if not self.has_hypertension:
            self.has_hypertension = True
            return True
        return False

    def check_hypertension_risk(self):
        return self.lifetime_hypertension_risk

class World(Container):
    def __init__(self):
        super().__init__("environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.check_claim()

    def _initialize_simulation(self):
        world = World()
        individual = Individual(age=55)
        world.addObject(individual)
        return world

    def check_claim(self):
        individual = self.rootObject.contains[0]  # Get the individual
        risk = individual.check_hypertension_risk()
        if risk == 0.9:
            self.result = "Supported"
        else:
            self.result = "Refuted"

    def get_result(self):
        return self.result

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(f"Claim verification result: {simulation.get_result()}")

if __name__ == "__main__":
    main()
