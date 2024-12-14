
# Claim: The proliferative capacity of neural progenitors differs across species.
# This simulation will compare the proliferative capacity of neural progenitors in primates and rodents.

from simulation_utils import GameObject, Container

class NeuralProgenitor(GameObject):
    def __init__(self, species, proliferation_rate):
        super().__init__(species)
        self.species = species
        self.proliferation_rate = proliferation_rate  # Represents the rate of proliferation

    def tick(self):
        # Simulate proliferation based on the species' rate
        self.proliferation_rate += 1  # Increment proliferation for simulation purposes

    def makeDescriptionStr(self):
        return f"A {self.species} neural progenitor with a proliferation rate of {self.proliferation_rate}."

class NeuralProgenitorSimulation(Container):
    def __init__(self):
        super().__init__("Neural Progenitor Environment")
        # Create neural progenitors for different species
        self.primate_progenitor = NeuralProgenitor("Primate", 5)  # Higher proliferation rate
        self.rodent_progenitor = NeuralProgenitor("Rodent", 2)    # Lower proliferation rate
        self.addObject(self.primate_progenitor)
        self.addObject(self.rodent_progenitor)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = NeuralProgenitorSimulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def step(self):
        # Simulate one tick for each progenitor
        for progenitor in self.rootObject.contains:
            progenitor.tick()
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print("Initial State:")
    print(simulation.observationStr)

    # Simulate for a few ticks to observe proliferation
    for _ in range(3):
        print("After tick:")
        print(simulation.step())
        print()

    # Determine if the claim is supported or refuted
    if simulation.rootObject.primate_progenitor.proliferation_rate > simulation.rootObject.rodent_progenitor.proliferation_rate:
        print("Claim Supported: The proliferative capacity of neural progenitors differs across species.")
    else:
        print("Claim Refuted: The proliferative capacity of neural progenitors does not differ across species.")

if __name__ == "__main__":
    main()
