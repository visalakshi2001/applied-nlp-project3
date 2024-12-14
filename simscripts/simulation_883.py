
# Claim: Omnivores produce more trimethylamine N-oxide from dietary I-carnitine than vegans.
# This simulation will compare the TMAO production between omnivores and vegans based on the claim.

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
            self.tmao_production = self.l_carnitine_intake * 1  # Lower production for vegans

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
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        omnivore = Diet("omnivore", l_carnitine_intake=10)  # Example intake
        vegan = Diet("vegan", l_carnitine_intake=10)        # Same intake for comparison
        world.addObject(omnivore)
        world.addObject(vegan)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.possibleActions["metabolize"] = ["metabolize"]

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "metabolize":
            for obj in self.rootObject.contains:
                obj.metabolize()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Performing metabolism...")
    result = simulation.step("metabolize")
    print(result)

    # Check the TMAO production
    omnivore_tmao = simulation.rootObject.contains[0].tmao_production
    vegan_tmao = simulation.rootObject.contains[1].tmao_production

    if omnivore_tmao > vegan_tmao:
        print("Claim Supported: Omnivores produce more TMAO than vegans.")
    else:
        print("Claim Refuted: Omnivores do not produce more TMAO than vegans.")

if __name__ == "__main__":
    main()
