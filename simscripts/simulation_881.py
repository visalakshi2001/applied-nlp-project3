
# Claim: Omnivores produce less trimethylamine N-oxide from dietary I-carnitine than vegans.
# The simulation will compare TMAO production between omnivores and vegans.

from simulation_utils import GameObject, Container

class Diet(GameObject):
    def __init__(self, name, l_carnitine_intake=0):
        super().__init__(name)
        self.l_carnitine_intake = l_carnitine_intake
        self.tmao_production = 0

    def metabolize(self):
        # Omnivores produce more TMAO than vegans
        if self.name == "omnivore":
            self.tmao_production = self.l_carnitine_intake * 2  # Arbitrary multiplier for omnivores
        elif self.name == "vegan":
            self.tmao_production = self.l_carnitine_intake * 1  # Arbitrary multiplier for vegans

    def makeDescriptionStr(self):
        return f"A {self.name} with L-carnitine intake of {self.l_carnitine_intake} produces TMAO: {self.tmao_production}."

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
        self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        omnivore = Diet("omnivore", l_carnitine_intake=5)  # Example intake
        vegan = Diet("vegan", l_carnitine_intake=5)        # Same intake for comparison
        world.addObject(omnivore)
        world.addObject(vegan)
        return world

    def run_simulation(self):
        # Metabolize to produce TMAO
        for obj in self.rootObject.getAllContainedObjectsRecursive():
            if isinstance(obj, Diet):
                obj.metabolize()

    def check_claim(self):
        omnivore_tmao = self.rootObject.contains[0].tmao_production
        vegan_tmao = self.rootObject.contains[1].tmao_production
        if omnivore_tmao > vegan_tmao:
            return "Claim Refuted: Omnivores produce more TMAO than vegans."
        else:
            return "Claim Supported: Omnivores produce less TMAO than vegans."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
