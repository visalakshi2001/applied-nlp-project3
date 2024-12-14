
# Claim: Antiretroviral therapy increases rates of tuberculosis across a broad range of CD4 strata.
# The simulation will test the relationship between antiretroviral therapy and tuberculosis incidence across different CD4 strata.

from simulation_utils import GameObject, Container

class AntiretroviralTherapy(GameObject):
    def __init__(self, name, effectiveness=0):
        super().__init__(name)
        self.effectiveness = effectiveness  # Effectiveness in reducing tuberculosis incidence

    def tick(self):
        # The effectiveness of the therapy is constant in this simulation
        pass

    def makeDescriptionStr(self):
        return f"{self.name} with effectiveness in reducing tuberculosis incidence: {self.effectiveness}"

class CD4Stratum(GameObject):
    def __init__(self, name, incidence_rate):
        super().__init__(name)
        self.incidence_rate = incidence_rate  # Incidence rate of tuberculosis in this CD4 stratum

    def apply_therapy(self, therapy):
        # Apply antiretroviral therapy and reduce incidence rate based on therapy effectiveness
        self.incidence_rate *= therapy.effectiveness

    def makeDescriptionStr(self):
        return f"{self.name} with tuberculosis incidence rate: {self.incidence_rate}"

class World(Container):
    def __init__(self):
        super().__init__("HIV and Tuberculosis Environment")

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
        therapy = AntiretroviralTherapy("Antiretroviral Therapy", effectiveness=0.35)  # 35% reduction in incidence
        cd4_stratum1 = CD4Stratum("CD4 < 200 cells/µl", incidence_rate=100)  # Initial incidence rate
        cd4_stratum2 = CD4Stratum("CD4 200-350 cells/µl", incidence_rate=80)
        cd4_stratum3 = CD4Stratum("CD4 > 350 cells/µl", incidence_rate=60)

        # Apply therapy to each CD4 stratum
        cd4_stratum1.apply_therapy(therapy)
        cd4_stratum2.apply_therapy(therapy)
        cd4_stratum3.apply_therapy(therapy)

        world.addObject(therapy)
        world.addObject(cd4_stratum1)
        world.addObject(cd4_stratum2)
        world.addObject(cd4_stratum3)

        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
