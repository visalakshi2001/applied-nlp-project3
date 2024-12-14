
# Claim: Female carriers of the Apolipoprotein E4 (APOE4) allele have increased risk for Alzheimer's disease.
# The simulation will model the relationship between reproductive years and the risk of dementia and Alzheimer's disease in female carriers of the APOE4 allele.

from simulation_utils import GameObject, Container

class FemaleCarrier(GameObject):
    def __init__(self, name, reproductive_years=0, has_APOE4=False):
        super().__init__(name)
        self.reproductive_years = reproductive_years
        self.has_APOE4 = has_APOE4
        self.dementia_risk = 1.0  # baseline risk

    def calculate_dementia_risk(self):
        if self.has_APOE4:
            if self.reproductive_years > 39:
                self.dementia_risk *= 4.20  # increased risk for high reproductive years
            elif self.reproductive_years < 34:
                self.dementia_risk *= 1.0  # baseline risk
            else:
                self.dementia_risk *= 1.04 ** (self.reproductive_years - 34)  # incremental risk
        else:
            self.dementia_risk *= 1.0  # no increased risk for non-carriers

    def makeDescriptionStr(self):
        return f"{self.name} is a {'carrier' if self.has_APOE4 else 'non-carrier'} with {self.reproductive_years} reproductive years and a dementia risk of {self.dementia_risk:.2f}."

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
        self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        carrier = FemaleCarrier("Carrier1", reproductive_years=40, has_APOE4=True)
        non_carrier = FemaleCarrier("NonCarrier1", reproductive_years=30, has_APOE4=False)
        world.addObject(carrier)
        world.addObject(non_carrier)
        return world

    def run_simulation(self):
        for obj in self.rootObject.getAllContainedObjectsRecursive():
            if isinstance(obj, FemaleCarrier):
                obj.calculate_dementia_risk()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
