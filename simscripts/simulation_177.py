
# Claim: Binding of p53 to enhancer regions (p53BERs) regulates the activity of p53 transcription and cell cycle arrest through the production of p53-dependent eRNAs.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class p53BER(GameObject):
    def __init__(self, name, eRNA_production=0):
        super().__init__(name)
        self.properties = {
            "eRNA_production": eRNA_production,
            "transcription_enhancement": False,
            "cell_cycle_arrest": False
        }

    def produce_eRNA(self):
        self.properties["eRNA_production"] += 1
        self.properties["transcription_enhancement"] = True
        self.properties["cell_cycle_arrest"] = True

    def makeDescriptionStr(self):
        description = f"A {self.name} with eRNA production level at {self.properties['eRNA_production']}. "
        description += f"Transcription enhancement: {self.properties['transcription_enhancement']}. "
        description += f"Cell cycle arrest: {self.properties['cell_cycle_arrest']}."
        return description

class p53(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def bind_to_enhancer(self, enhancer):
        enhancer.produce_eRNA()

class World(Container):
    def __init__(self):
        Container.__init__(self, "cell environment")

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
        p53_enhancer = p53BER("p53BER")
        p53_protein = p53("p53 Protein")
        
        # Simulating the binding of p53 to the enhancer
        p53_protein.bind_to_enhancer(p53_enhancer)
        
        world.addObject(p53_enhancer)
        world.addObject(p53_protein)
        return world

    def step(self):
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
