
# Claim: Citrullinated proteins externalized in neutrophil extracellular traps act indirectly to perpetuate the inflammatory cycle via induction of autoantibodies.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class Autoantibody(GameObject):
    def __init__(self, name, induced=False):
        super().__init__(name)
        self.properties = {
            "induced": induced
        }

    def induce(self):
        self.properties["induced"] = True

    def makeDescriptionStr(self):
        return f"An autoantibody named {self.name}, induced: {self.properties['induced']}."

class CitrullinatedProtein(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def makeDescriptionStr(self):
        return f"A citrullinated protein named {self.name}."

class Neutrophil(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.externalized_proteins = []

    def externalize(self, protein):
        self.externalized_proteins.append(protein)

    def makeDescriptionStr(self):
        return f"A neutrophil named {self.name} that has externalized proteins: {[protein.name for protein in self.externalized_proteins]}."

class InflammatoryCycle(Container):
    def __init__(self):
        super().__init__("Inflammatory Cycle")
        self.autoantibodies = []
        self.neutrophils = []

    def addAutoantibody(self, autoantibody):
        self.autoantibodies.append(autoantibody)

    def addNeutrophil(self, neutrophil):
        self.neutrophils.append(neutrophil)

    def checkInduction(self):
        for neutrophil in self.neutrophils:
            for protein in neutrophil.externalized_proteins:
                if isinstance(protein, CitrullinatedProtein):
                    # Induce autoantibodies if citrullinated proteins are externalized
                    autoantibody = Autoantibody(f"Autoantibody against {protein.name}")
                    autoantibody.induce()
                    self.addAutoantibody(autoantibody)

    def makeDescriptionStr(self):
        outStr = super().makeDescriptionStr() + "\n"
        outStr += "Autoantibodies present: " + ", ".join([ab.name for ab in self.autoantibodies]) + "\n"
        outStr += "Neutrophils present: " + ", ".join([neutrophil.name for neutrophil in self.neutrophils]) + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.inflammatory_cycle = InflammatoryCycle()
        self.setup_simulation()

    def setup_simulation(self):
        # Create neutrophils
        neutrophil1 = Neutrophil("Neutrophil 1")
        neutrophil2 = Neutrophil("Neutrophil 2")

        # Create citrullinated proteins
        protein1 = CitrullinatedProtein("Citrullinated Vimentin")
        protein2 = CitrullinatedProtein("Citrullinated Fibrinogen")

        # Externalize proteins in neutrophils
        neutrophil1.externalize(protein1)
        neutrophil2.externalize(protein2)

        # Add neutrophils to the inflammatory cycle
        self.inflammatory_cycle.addNeutrophil(neutrophil1)
        self.inflammatory_cycle.addNeutrophil(neutrophil2)

        # Check for induction of autoantibodies
        self.inflammatory_cycle.checkInduction()

    def run(self):
        print(self.inflammatory_cycle.makeDescriptionStr())
        if self.inflammatory_cycle.autoantibodies:
            return "Claim Supported: Citrullinated proteins externalized in neutrophil extracellular traps act indirectly to perpetuate the inflammatory cycle via induction of autoantibodies."
        else:
            return "Claim Refuted: No autoantibodies induced."

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
