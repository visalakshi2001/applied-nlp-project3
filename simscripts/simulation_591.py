
# Claim: Incidence of 10/66 dementia is higher than the incidence of DSM-IV dementia.
# The simulation will compare the incidence rates of 10/66 dementia and DSM-IV dementia.

from simulation_utils import GameObject, Container

class DementiaIncidence(GameObject):
    def __init__(self, name, incidence_rate):
        super().__init__(name)
        self.incidence_rate = incidence_rate

    def makeDescriptionStr(self):
        return f"{self.name} has an incidence rate of {self.incidence_rate} per 1000 person-years."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.compare_incidence()

    def _initialize_simulation(self):
        world = Container("Dementia Incidence Comparison")
        incidence_1066 = DementiaIncidence("10/66 Dementia", (18.2 + 30.4) / 2)  # Average of the range
        incidence_dsm_iv = DementiaIncidence("DSM-IV Dementia", (9.9 + 15.7) / 2)  # Average of the range
        world.addObject(incidence_1066)
        world.addObject(incidence_dsm_iv)
        return world

    def compare_incidence(self):
        incidence_1066 = self.rootObject.containsItemWithName("10/66 Dementia")[0].incidence_rate
        incidence_dsm_iv = self.rootObject.containsItemWithName("DSM-IV Dementia")[0].incidence_rate
        
        if incidence_1066 > incidence_dsm_iv:
            self.result = "Supported: Incidence of 10/66 dementia is higher than the incidence of DSM-IV dementia."
        else:
            self.result = "Refuted: Incidence of 10/66 dementia is not higher than the incidence of DSM-IV dementia."

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        outStr += self.result
        return outStr

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
