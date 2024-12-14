
# Claim: Cellular clocks are not predictive of mitosis timing in NIH 3T3 cells.
# The simulation will test the relationship between circadian cycles and cell division timing in NIH 3T3 cells.

from simulation_utils import GameObject, Container

class Cell(GameObject):
    def __init__(self, name, circadian_cycle_time=24, division_time=0):
        super().__init__(name)
        self.properties = {
            "circadian_cycle_time": circadian_cycle_time,  # in hours
            "division_time": division_time  # time of division in hours
        }

    def tick(self):
        # Simulate the cell division occurring 5 hours before the peak of the circadian cycle
        self.properties["division_time"] = (self.properties["circadian_cycle_time"] - 5) % 24

    def makeDescriptionStr(self):
        description = f"A {self.name}, with a circadian cycle time of {self.properties['circadian_cycle_time']} hours, divides at {self.properties['division_time']} hours."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "cellular environment")

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
        cell1 = Cell("NIH 3T3 Cell 1", circadian_cycle_time=24)
        cell2 = Cell("NIH 3T3 Cell 2", circadian_cycle_time=24)
        world.addObject(cell1)
        world.addObject(cell2)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        # Do one tick of the environment
        self.doWorldTick()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
