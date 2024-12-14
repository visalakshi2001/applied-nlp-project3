
# Claim: Incidence of 10/66 dementia is lower than the incidence of DSM-IV dementia.
# The simulation will compare the incidence rates of 10/66 dementia and DSM-IV dementia.

from simulation_utils import GameObject, Container

class DementiaIncidence(GameObject):
    def __init__(self, name, incidence_rate):
        super().__init__(name)
        self.incidence_rate = incidence_rate

    def makeDescriptionStr(self):
        return f"{self.name} has an incidence rate of {self.incidence_rate} per 1000 person-years."

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.compare_incidence()

    def _initialize_simulation(self):
        world = World()
        dementia_10_66 = DementiaIncidence("10/66 dementia", (18.2 + 30.4) / 2)  # Average incidence
        dementia_dsm_iv = DementiaIncidence("DSM-IV dementia", (9.9 + 15.7) / 2)  # Average incidence
        world.addObject(dementia_10_66)
        world.addObject(dementia_dsm_iv)
        return world

    def compare_incidence(self):
        incidence_10_66 = self.rootObject.contains[0].incidence_rate
        incidence_dsm_iv = self.rootObject.contains[1].incidence_rate
        
        if incidence_10_66 < incidence_dsm_iv:
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
