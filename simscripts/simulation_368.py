
# Claim: Early patent ductus ateriosus (PDA) screening increases in-hospital mortality.
# The simulation will evaluate the relationship between early screening for PDA and in-hospital mortality rates.

from simulation_utils import GameObject, Container

class Infant(GameObject):
    def __init__(self, name, screened=False):
        super().__init__(name)
        self.screened = screened
        self.mortality_rate = 0.0  # Default mortality rate

    def evaluate_mortality(self):
        if self.screened:
            self.mortality_rate = 14.2  # Mortality rate for screened infants
        else:
            self.mortality_rate = 18.5  # Mortality rate for non-screened infants

    def makeDescriptionStr(self):
        return f"{self.name} (Screened: {self.screened}, Mortality Rate: {self.mortality_rate}%)"

class World(Container):
    def __init__(self):
        super().__init__("hospital environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.evaluate_mortality_rates()

    def _initialize_simulation(self):
        world = World()
        infant1 = Infant("Infant 1", screened=True)
        infant2 = Infant("Infant 2", screened=False)
        world.addObject(infant1)
        world.addObject(infant2)
        return world

    def evaluate_mortality_rates(self):
        for infant in self.rootObject.getAllContainedObjectsRecursive():
            infant.evaluate_mortality()

    def check_claim(self):
        screened_mortality = self.rootObject.contains[0].mortality_rate
        non_screened_mortality = self.rootObject.contains[1].mortality_rate
        if screened_mortality < non_screened_mortality:
            return "Claim Refuted: Early screening is associated with lower in-hospital mortality."
        else:
            return "Claim Supported: Early screening is associated with higher in-hospital mortality."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
