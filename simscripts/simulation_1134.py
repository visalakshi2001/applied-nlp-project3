
# Claim: TNFAIP3 is a glioblastoma tumor enhancer.
# The simulation will model the effects of TNFAIP3 (A20) on glioblastoma stem cells (GSCs) growth and survival.

from simulation_utils import GameObject, Container

class GlioblastomaStemCell(GameObject):
    def __init__(self, name, A20_expression=0):
        super().__init__(name)
        self.properties = {
            "A20_expression": A20_expression,  # Level of A20 expression
            "growth": 1,  # Initial growth rate
            "survival": 1  # Initial survival rate
        }

    def tick(self):
        # Simulate the effect of A20 expression on growth and survival
        if self.properties["A20_expression"] > 0:
            self.properties["growth"] *= 1.1  # Growth increases with A20
            self.properties["survival"] *= 1.2  # Survival increases with A20
        else:
            self.properties["growth"] *= 0.9  # Growth decreases without A20
            self.properties["survival"] *= 0.8  # Survival decreases without A20

    def makeDescriptionStr(self):
        return f"{self.name} with A20 expression level {self.properties['A20_expression']}, growth rate {self.properties['growth']}, and survival rate {self.properties['survival']}."

class A20Regulator(Container):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = A20Regulator("A20 Regulation Environment")
        gsc_high_A20 = GlioblastomaStemCell("GSC High A20", A20_expression=1)  # High A20 expression
        gsc_low_A20 = GlioblastomaStemCell("GSC Low A20", A20_expression=0)  # Low A20 expression
        world.addObject(gsc_high_A20)
        world.addObject(gsc_low_A20)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "tick": ["tick"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "tick":
            # Perform a tick to simulate the growth and survival effects
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate multiple ticks to observe the effects
    for _ in range(5):
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
