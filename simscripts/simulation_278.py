
# Claim: Commelina yellow mottle virus' (ComYMV) genome consists of 2140 base pairs.
# The reference text indicates that the genome size is 7489 bp, which refutes the claim.

from simulation_utils import GameObject, Container

class Virus(GameObject):
    def __init__(self, name, genome_size):
        super().__init__(name)
        self.properties = {
            "genome_size": genome_size
        }

    def makeDescriptionStr(self):
        return f"A virus named {self.name} with a genome size of {self.properties['genome_size']} base pairs."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("environment")
        comYMV = Virus("Commelina yellow mottle virus", 7489)  # Genome size from reference text
        world.addObject(comYMV)
        return world

    def check_claim(self):
        virus = self.rootObject.contains[0]  # Assuming the first object is the virus
        if virus.properties["genome_size"] == 2140:
            return "Claim Supported: The genome size is 2140 base pairs."
        else:
            return "Claim Refuted: The genome size is not 2140 base pairs."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
