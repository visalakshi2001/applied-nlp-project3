
# Claim: Androgenetic haploid mouse embryonic stem cells (ESCs) can be derived and genetically manipulated in vitro.
# The simulation will check if AG-haESCs can be derived and manipulated based on the reference text.

from simulation_utils import GameObject, Container

class HaploidESC(GameObject):
    def __init__(self, name, can_be_derived=False, can_be_manipulated=False):
        super().__init__(name)
        self.properties = {
            "can_be_derived": can_be_derived,
            "can_be_manipulated": can_be_manipulated
        }

    def tick(self):
        # Simulate the derivation and manipulation process
        if self.properties["can_be_derived"]:
            self.properties["can_be_manipulated"] = True  # If derived, they can be manipulated

    def makeDescriptionStr(self):
        description = f"{self.name} - Derived: {self.properties['can_be_derived']}, Manipulated: {self.properties['can_be_manipulated']}."
        return description

class World(Container):
    def __init__(self):
        super().__init__("lab")
        self.haploid_esc = HaploidESC("AG-haESC", can_be_derived=True)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += self.haploid_esc.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        return world

    def run_simulation(self):
        # Simulate the process of derivation and manipulation
        self.rootObject.haploid_esc.tick()

    def check_claim(self):
        if self.rootObject.haploid_esc.properties["can_be_derived"] and self.rootObject.haploid_esc.properties["can_be_manipulated"]:
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
