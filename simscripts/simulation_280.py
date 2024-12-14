
# Claim: Comparative transcriptome analysis identified new platelet proteins with structural features suggesting a role in platelet function.
# The simulation will analyze the presence of newly identified platelet proteins and their potential roles.

from simulation_utils import GameObject, Container

class PlateletProtein(GameObject):
    def __init__(self, name, structural_features, function_suggested):
        super().__init__(name)
        self.structural_features = structural_features
        self.function_suggested = function_suggested

    def makeDescriptionStr(self):
        return f"{self.name} with structural features: {self.structural_features} and suggested function: {self.function_suggested}."

class Platelet(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.proteins = []

    def addProtein(self, protein):
        self.proteins.append(protein)

    def makeDescriptionStr(self):
        description = f"A {self.name} containing the following proteins:\n"
        for protein in self.proteins:
            description += "\t" + protein.makeDescriptionStr() + "\n"
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("Platelet Environment")
        platelet = Platelet("Platelet")
        
        # Adding new proteins identified in the claim
        g6b = PlateletProtein("G6b", "Transmembrane domain", "Modulation of platelet function")
        g6f = PlateletProtein("G6f", "Transmembrane domain", "Modulation of platelet function")
        lrrc32 = PlateletProtein("LRRC32", "Transmembrane domain", "Modulation of platelet function")
        suc_nr1 = PlateletProtein("SUCNR1", "G protein-coupled receptor", "Potentiation of platelet agonists")

        platelet.addProtein(g6b)
        platelet.addProtein(g6f)
        platelet.addProtein(lrrc32)
        platelet.addProtein(suc_nr1)

        world.addObject(platelet)
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
