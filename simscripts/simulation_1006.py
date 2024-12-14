
# Claim: RTEL1 interacts with TRF2 through a C4C4 motif
# The simulation will check if the interaction between RTEL1 and TRF2 is mediated by a C4C4 motif.

from simulation_utils import GameObject, Container

class Protein(GameObject):
    def __init__(self, name, interacts_with=None, motif=None):
        super().__init__(name)
        self.properties = {
            "interacts_with": interacts_with,
            "motif": motif
        }

    def check_interaction(self):
        if self.properties["interacts_with"] and self.properties["motif"] == "C4C4":
            return True
        return False

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.check_claim()

    def _initialize_simulation(self):
        world = Container("environment")
        rtel1 = Protein("RTEL1", interacts_with="TRF2", motif="C4C4")
        trf2 = Protein("TRF2", interacts_with="RTEL1", motif=None)
        world.addObject(rtel1)
        world.addObject(trf2)
        return world

    def check_claim(self):
        rtel1 = self.rootObject.containsItemWithName("RTEL1")[0]
        if rtel1.check_interaction():
            return "Supported"
        else:
            return "Refuted"

    def makeDescriptionStr(self):
        return f"In the {self.rootObject.name}, we have: {', '.join([obj.name for obj in self.rootObject.contains])}."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Claim Verification Result:", simulation.result)

if __name__ == "__main__":
    main()
