
# Claim: Omnivores produce more trimethylamine N-oxide from dietary I-carnitine than vegetarians.
# This simulation will compare the TMAO production between omnivores and vegetarians based on the claim.

from simulation_utils import GameObject, Container

class Human(GameObject):
    def __init__(self, name, diet_type):
        super().__init__(name)
        self.diet_type = diet_type
        self.TMAO_production = 0

    def consume_L_carnitine(self):
        if self.diet_type == "omnivore":
            self.TMAO_production += 10  # Omnivores produce more TMAO
        elif self.diet_type == "vegetarian":
            self.TMAO_production += 5   # Vegetarians produce less TMAO

    def makeDescriptionStr(self):
        return f"{self.name} is a {self.diet_type} with TMAO production level: {self.TMAO_production}."

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
        self.simulate_consumption()

    def _initialize_simulation(self):
        world = World()
        omnivore = Human("Omnivore", "omnivore")
        vegetarian = Human("Vegetarian", "vegetarian")
        world.addObject(omnivore)
        world.addObject(vegetarian)
        return world

    def simulate_consumption(self):
        for human in self.rootObject.contains:
            human.consume_L_carnitine()

    def check_claim(self):
        omnivore = self.rootObject.contains[0]
        vegetarian = self.rootObject.contains[1]
        if omnivore.TMAO_production > vegetarian.TMAO_production:
            return "Claim Supported: Omnivores produce more TMAO than vegetarians."
        else:
            return "Claim Refuted: Omnivores do not produce more TMAO than vegetarians."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
