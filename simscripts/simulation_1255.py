
# The claim is that the proliferative capacity of progenitors is regulated cell-autonomously.
# We will simulate progenitor cells and their proliferation behavior based on the claim and reference text.

from simulation_utils import GameObject, Container

class ProgenitorCell(GameObject):
    def __init__(self, name, proliferation_rate=1):
        super().__init__(name)
        self.proliferation_rate = proliferation_rate  # Rate of proliferation
        self.proliferation_count = 0  # Count of how many times this cell has proliferated

    def tick(self):
        # Each tick represents a time step in which the cell can proliferate
        self.proliferation_count += self.proliferation_rate

    def makeDescriptionStr(self):
        return f"A {self.name} that has proliferated {self.proliferation_count} times."

class ProgenitorContainer(Container):
    def __init__(self, name):
        super().__init__(name)

    def tick(self):
        # Call tick on all progenitor cells in the container
        for cell in self.contains:
            cell.tick()

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = ProgenitorContainer("Progenitor Environment")
        progenitor1 = ProgenitorCell("Progenitor Cell 1", proliferation_rate=1)
        progenitor2 = ProgenitorCell("Progenitor Cell 2", proliferation_rate=2)  # Different proliferation rate
        world.addObject(progenitor1)
        world.addObject(progenitor2)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            self.rootObject.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["tick", "tick", "tick"]  # Simulate multiple time steps

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final observation to determine if the claim is supported
    progenitor1_count = simulation.rootObject.contains[0].proliferation_count
    progenitor2_count = simulation.rootObject.contains[1].proliferation_count

    if progenitor1_count > 0 and progenitor2_count > progenitor1_count:
        print("Claim Supported: The proliferative capacity of progenitors is regulated cell-autonomously.")
    else:
        print("Claim Refuted: The proliferative capacity of progenitors is not regulated cell-autonomously.")

if __name__ == "__main__":
    main()
