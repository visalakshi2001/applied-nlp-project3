
# Claim: CD28 initiates tonic signaling in conventional T cells, which causes an exhaustion phenotype and limited efficiency.
# The simulation will model T cells and the effects of CD28 costimulation on exhaustion.

from simulation_utils import GameObject, Container

class TCell(GameObject):
    def __init__(self, name, exhaustion_level=0):
        super().__init__(name)
        self.exhaustion_level = exhaustion_level
        self.properties = {
            "exhaustion_level": exhaustion_level
        }

    def tick(self):
        # Simulate the effect of tonic signaling from CD28
        self.properties["exhaustion_level"] += 1  # Increase exhaustion level over time

    def makeDescriptionStr(self):
        return f"A T cell named {self.name} with an exhaustion level of {self.properties['exhaustion_level']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("T Cell Environment")
        t_cell_cd28 = TCell("TCell_CD28")
        t_cell_no_cd28 = TCell("TCell_No_CD28")
        world.addObject(t_cell_cd28)
        world.addObject(t_cell_no_cd28)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            # Perform a tick to simulate time passing
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate multiple ticks to observe the exhaustion levels
    for _ in range(5):
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
