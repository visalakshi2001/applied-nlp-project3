
# Claim: Female carriers of the Apolipoprotein E4 (APOE4) allele have shorter lifetime exposure to estrogen due to a decreased reproductive period.
# This simulation will model the relationship between reproductive years and dementia risk in APOE4 carriers.

from simulation_utils import GameObject, Container

class Woman(GameObject):
    def __init__(self, name, reproductive_years=0, is_APOE4_carrier=False):
        super().__init__(name)
        self.reproductive_years = reproductive_years
        self.is_APOE4_carrier = is_APOE4_carrier
        self.dementia_risk = 0

    def calculate_dementia_risk(self):
        if self.is_APOE4_carrier:
            if self.reproductive_years > 39:
                self.dementia_risk = 4.20  # High risk for >39 reproductive years
            elif self.reproductive_years < 34:
                self.dementia_risk = 1.0  # Baseline risk for <34 reproductive years
            else:
                self.dementia_risk = 2.0  # Moderate risk for 34-39 reproductive years
        else:
            self.dementia_risk = 1.0  # No increased risk for non-carriers

    def makeDescriptionStr(self):
        return f"{self.name} is {'an APOE4 carrier' if self.is_APOE4_carrier else 'not an APOE4 carrier'} with {self.reproductive_years} reproductive years and a dementia risk of {self.dementia_risk}."

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
        woman1 = Woman("Woman 1", reproductive_years=40, is_APOE4_carrier=True)
        woman2 = Woman("Woman 2", reproductive_years=30, is_APOE4_carrier=True)
        woman3 = Woman("Woman 3", reproductive_years=35, is_APOE4_carrier=False)
        world.addObject(woman1)
        world.addObject(woman2)
        world.addObject(woman3)
        return world

    def run_simulation(self):
        allWomen = self.rootObject.getAllContainedObjectsRecursive()
        for woman in allWomen:
            woman.calculate_dementia_risk()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
