
# Claim: Anthrax spores remain deadly until affected areas are decontaminated.
# The simulation will model the presence of anthrax spores and their viability over time.

from simulation_utils import GameObject, Container

class AnthraxSpore(GameObject):
    def __init__(self, name, viability=100):
        super().__init__(name)
        self.viability = viability  # Represents the viability of the spore (0-100)

    def tick(self):
        # Simulate the decay of viability over time
        if self.viability > 0:
            self.viability -= 10  # Decrease viability by 10 each tick

    def makeDescriptionStr(self):
        return f"{self.name} with viability at {self.viability}%."

class Environment(Container):
    def __init__(self):
        super().__init__("Contaminated Area")
        self.decontaminated = False

    def decontaminate(self):
        self.decontaminated = True
        for spore in self.contains:
            spore.viability = 0  # Decontamination sets viability to 0

    def makeDescriptionStr(self):
        status = "decontaminated" if self.decontaminated else "contaminated"
        return f"In the {self.name}, the area is currently {status}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        environment = Environment()
        anthrax_spore1 = AnthraxSpore("Anthrax Spore 1")
        anthrax_spore2 = AnthraxSpore("Anthrax Spore 2")
        environment.addObject(anthrax_spore1)
        environment.addObject(anthrax_spore2)
        return environment

    def generatePossibleActions(self):
        self.possibleActions = {
            "look": ["look"],
            "decontaminate": ["decontaminate"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "decontaminate":
            self.rootObject.decontaminate()
            self.observationStr = "The area has been decontaminated."

        # Update the viability of spores
        for spore in self.rootObject.contains:
            spore.tick()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["look", "decontaminate", "look"]
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
