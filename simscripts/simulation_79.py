
# Claim: Active caspase-11 protein promotes pyroptosis.
# The simulation will test the role of active caspase-11 in promoting pyroptosis by observing its interaction with bacteria.

from simulation_utils import GameObject, Container

class Caspase(GameObject):
    def __init__(self, name, active=False):
        super().__init__(name)
        self.active = active

    def promote_pyroptosis(self, bacteria):
        if self.active:
            return f"{self.name} promotes pyroptosis in {bacteria.name}."
        else:
            return f"{self.name} does not promote pyroptosis in {bacteria.name}."

class Bacteria(GameObject):
    def __init__(self, name):
        super().__init__(name)

# The world is the root object of the game object tree.
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
        caspase11 = Caspase("Caspase-11", active=True)  # Active caspase-11
        bacteria1 = Bacteria("L. pneumophila")  # Bacteria that caspase-11 interacts with
        world.addObject(caspase11)
        world.addObject(bacteria1)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("test pyroptosis", ["test"])

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

        if actionVerb == "test":
            caspase11 = self.rootObject.containsItemWithName("Caspase-11")[0]
            bacteria1 = self.rootObject.containsItemWithName("L. pneumophila")[0]
            self.observationStr = caspase11.promote_pyroptosis(bacteria1)

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.step("test pyroptosis")
    print(result)

if __name__ == "__main__":
    main()
