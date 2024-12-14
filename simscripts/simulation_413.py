
# Claim: Female carriers of the Apolipoprotein E4 (APOE4) allele have decreased risk for dementia.
# The simulation will evaluate the relationship between reproductive years and dementia risk in APOE4 carriers.

from simulation_utils import GameObject, Container

class Woman(GameObject):
    def __init__(self, name, reproductive_years, is_APOE4_carrier):
        super().__init__(name)
        self.reproductive_years = reproductive_years
        self.is_APOE4_carrier = is_APOE4_carrier
        self.dementia_risk = self.calculate_dementia_risk()

    def calculate_dementia_risk(self):
        # Risk increases with reproductive years for APOE4 carriers
        if self.is_APOE4_carrier:
            if self.reproductive_years > 39:
                return 4.20  # High risk
            elif self.reproductive_years < 34:
                return 1.0  # Baseline risk
            else:
                return 2.0  # Moderate risk
        else:
            return 1.0  # No increased risk for non-carriers

    def makeDescriptionStr(self):
        return f"{self.name} has {self.reproductive_years} reproductive years and a dementia risk factor of {self.dementia_risk}."

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

    def _initialize_simulation(self):
        world = World()
        woman1 = Woman("Woman A", reproductive_years=40, is_APOE4_carrier=True)  # APOE4 carrier
        woman2 = Woman("Woman B", reproductive_years=30, is_APOE4_carrier=False)  # Non-carrier
        world.addObject(woman1)
        world.addObject(woman2)
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Evaluate the claim based on the simulation results
    if simulation.rootObject.contains[0].dementia_risk > 1.0:
        print("Claim Refuted: Female carriers of the APOE4 allele have increased risk for dementia.")
    else:
        print("Claim Supported: Female carriers of the APOE4 allele have decreased risk for dementia.")

if __name__ == "__main__":
    main()
