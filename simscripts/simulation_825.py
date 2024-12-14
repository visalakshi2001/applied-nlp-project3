
# Claim: N348I mutations reduce resistance to nevirapine.
# The simulation will analyze the effect of N348I mutation on nevirapine susceptibility.

from simulation_utils import GameObject, Container

class Virus(GameObject):
    def __init__(self, name, nevirapine_susceptibility=1.0):
        super().__init__(name)
        self.nevirapine_susceptibility = nevirapine_susceptibility

    def apply_mutation(self, mutation_factor):
        self.nevirapine_susceptibility *= mutation_factor

    def makeDescriptionStr(self):
        return f"A {self.name} virus with nevirapine susceptibility of {self.nevirapine_susceptibility}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("environment")
        wild_type_virus = Virus("wild_type_virus", nevirapine_susceptibility=1.0)
        n348i_mutant_virus = Virus("n348i_mutant_virus", nevirapine_susceptibility=1.0)

        # Apply N348I mutation which decreases susceptibility to nevirapine by 7.4-fold
        n348i_mutant_virus.apply_mutation(1/7.4)

        world.addObject(wild_type_virus)
        world.addObject(n348i_mutant_virus)
        return world

    def analyze_results(self):
        allViruses = self.rootObject.getAllContainedObjectsRecursive()
        wild_type_susceptibility = None
        n348i_susceptibility = None

        for virus in allViruses:
            if virus.name == "wild_type_virus":
                wild_type_susceptibility = virus.nevirapine_susceptibility
            elif virus.name == "n348i_mutant_virus":
                n348i_susceptibility = virus.nevirapine_susceptibility

        if n348i_susceptibility < wild_type_susceptibility:
            return "Claim Supported: N348I mutations reduce resistance to nevirapine."
        else:
            return "Claim Refuted: N348I mutations do not reduce resistance to nevirapine."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.analyze_results()
    print(result)

if __name__ == "__main__":
    main()
