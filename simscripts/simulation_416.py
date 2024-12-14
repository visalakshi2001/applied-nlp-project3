
# Claim: Female carriers of the Apolipoprotein E4 (APOE4) allele have longer lifetime exposure to estrogen due to an increased reproductive period.
# This simulation will model the relationship between reproductive period and risk of dementia in APOE4 carriers.

from simulation_utils import GameObject, Container

class Woman(GameObject):
    def __init__(self, name, reproductive_years, is_APOE4_carrier):
        super().__init__(name)
        self.reproductive_years = reproductive_years
        self.is_APOE4_carrier = is_APOE4_carrier
        self.dementia_risk = 0

    def calculate_dementia_risk(self):
        if self.is_APOE4_carrier:
            if self.reproductive_years > 39:
                self.dementia_risk = 4.20  # High risk for >39 reproductive years
            elif self.reproductive_years < 34:
                self.dementia_risk = 1.0  # Baseline risk
            else:
                self.dementia_risk = 1.78  # Moderate risk for 34-39 reproductive years
        else:
            self.dementia_risk = 1.0  # No increased risk for non-carriers

    def makeDescriptionStr(self):
        return f"{self.name} has {self.reproductive_years} reproductive years and a dementia risk of {self.dementia_risk}."

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
        woman1 = Woman("Woman A", 40, True)  # APOE4 carrier
        woman2 = Woman("Woman B", 30, True)  # APOE4 carrier
        woman3 = Woman("Woman C", 35, False) # Non-carrier
        world.addObject(woman1)
        world.addObject(woman2)
        world.addObject(woman3)
        return world

    def run_simulation(self):
        for obj in self.rootObject.getAllContainedObjectsRecursive():
            if isinstance(obj, Woman):
                obj.calculate_dementia_risk()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
