
# Claim: There is a relation between Erythromycin use and hypertrophic pyloric stenosis.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class Macrolide(GameObject):
    def __init__(self, name, usage_period, associated_risk):
        super().__init__(name)
        self.usage_period = usage_period  # e.g., "0-13 days", "14-120 days", "during pregnancy"
        self.associated_risk = associated_risk  # Risk ratio for IHPS

    def makeDescriptionStr(self):
        return f"{self.name} used during {self.usage_period} has an associated risk ratio of {self.associated_risk} for IHPS."

class Infant(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.macrolide_usage = None

    def use_macrolide(self, macrolide):
        self.macrolide_usage = macrolide

    def makeDescriptionStr(self):
        if self.macrolide_usage:
            return f"{self.name} has used {self.macrolide_usage.name}."
        else:
            return f"{self.name} has not used any macrolide."

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

    def _initialize_simulation(self):
        world = World()
        erythromycin = Macrolide("Erythromycin", "0-13 days after birth", 29.8)
        infant1 = Infant("Infant_1")
        infant2 = Infant("Infant_2")
        
        # Simulating macrolide usage
        infant1.use_macrolide(erythromycin)
        
        world.addObject(erythromycin)
        world.addObject(infant1)
        world.addObject(infant2)
        
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
