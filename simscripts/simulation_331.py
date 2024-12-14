
# Claim: Deltex interacts with eIF3. There is no known interaction between Deltex and elF3
# The simulation will check if Deltex interacts with eIF3 based on the provided reference text.

from simulation_utils import GameObject, Container

class Protein(GameObject):
    def __init__(self, name, interacts_with=None):
        super().__init__(name)
        self.interacts_with = interacts_with if interacts_with else []

    def add_interaction(self, protein):
        if protein not in self.interacts_with:
            self.interacts_with.append(protein)

    def check_interaction(self, protein):
        return protein in self.interacts_with

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.result = self.check_claim()

    def _initialize_simulation(self):
        world = Container("biological_environment")
        deltex = Protein("Deltex")
        eIF3 = Protein("eIF3")
        
        # According to the reference text, Deltex interacts with eIF3
        deltex.add_interaction(eIF3)

        world.addObject(deltex)
        world.addObject(eIF3)
        return world

    def check_claim(self):
        deltex = self.rootObject.containsItemWithName("Deltex")[0]
        eIF3 = self.rootObject.containsItemWithName("eIF3")[0]

        # Check if Deltex interacts with eIF3
        if deltex.check_interaction(eIF3):
            return "Supported"  # Claim is supported
        else:
            return "Refuted"  # Claim is refuted

def main():
    simulation = Simulation()
    print(simulation.result)

if __name__ == "__main__":
    main()
