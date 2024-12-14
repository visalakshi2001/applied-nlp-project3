
# Claim: RUNX1 is downregulated or mutated in TLX1 T-ALL.
# The simulation will check if RUNX1 is identified as a tumor-suppressor gene and if mutations are present in T-ALL.

from simulation_utils import GameObject, Container

class Gene(GameObject):
    def __init__(self, name, is_tumor_suppressor=False, is_mutated=False):
        super().__init__(name)
        self.properties = {
            "is_tumor_suppressor": is_tumor_suppressor,
            "is_mutated": is_mutated
        }

    def makeDescriptionStr(self):
        description = f"{self.name} is a gene. "
        if self.properties["is_tumor_suppressor"]:
            description += "It is identified as a tumor-suppressor gene. "
        if self.properties["is_mutated"]:
            description += "It has mutations present."
        return description

class TLX1(GameObject):
    def __init__(self):
        super().__init__("TLX1")
        self.properties = {
            "is_oncogene": True
        }

class TALL(GameObject):
    def __init__(self):
        super().__init__("T-ALL")
        self.properties = {
            "is_leukemia": True
        }

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("environment")
        tlx1 = TLX1()
        runx1 = Gene("RUNX1", is_tumor_suppressor=True, is_mutated=True)
        tall = TALL()

        world.addObject(tlx1)
        world.addObject(runx1)
        world.addObject(tall)

        return world

    def step(self):
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    result = simulation.step()
    print(result)

    # Check if the claim is supported or refuted
    if "RUNX1 is a gene. It is identified as a tumor-suppressor gene. It has mutations present." in result:
        print("Claim Supported: RUNX1 is downregulated or mutated in TLX1 T-ALL.")
    else:
        print("Claim Refuted: RUNX1 is not downregulated or mutated in TLX1 T-ALL.")

if __name__ == "__main__":
    main()
