
# Claim: The deamination of cytidine to uridine on the minus strand of viral DNA can inactivate the viral genome by inducing G-to-A mutations.
# This simulation will model the effect of APOBEC3G on viral DNA and check if it leads to G-to-A mutations.

from simulation_utils import GameObject, Container

class ViralDNA(GameObject):
    def __init__(self, name, mutations=0):
        super().__init__(name)
        self.mutations = mutations  # Number of G-to-A mutations

    def deaminate(self):
        # Simulate the deamination process which induces G-to-A mutations
        self.mutations += 1  # Each deamination leads to one G-to-A mutation

    def makeDescriptionStr(self):
        return f"{self.name} with {self.mutations} G-to-A mutations."

class APOBEC3G(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def exertEffect(self, viral_dna):
        # Simulate the effect of APOBEC3G on viral DNA
        viral_dna.deaminate()  # Induces deamination leading to mutations

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("Viral Environment")
        viral_dna = ViralDNA("Viral DNA")
        apobec3g = APOBEC3G("APOBEC3G")
        world.addObject(viral_dna)
        world.addObject(apobec3g)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "apply APOBEC3G effect": ["apply", self.rootObject.contains[1]],  # Apply effect of APOBEC3G
            "look": ["look"]
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
        elif actionVerb == "apply":
            apobec3g = action[1]
            viral_dna = self.rootObject.contains[0]
            apobec3g.exertEffect(viral_dna)
            self.observationStr = f"{apobec3g.name} applied its effect on {viral_dna.name}."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "apply APOBEC3G effect"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final observation to check the number of mutations
    final_viral_dna = simulation.rootObject.contains[0]
    print(f"Final state: {final_viral_dna.makeDescriptionStr()}")

if __name__ == "__main__":
    main()
