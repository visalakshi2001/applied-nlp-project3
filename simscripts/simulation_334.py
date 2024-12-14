
# Claim: Depletion of nitric oxide is responsible for vasospasm.
# This simulation will test the relationship between nitric oxide levels and the occurrence of vasospasm.

from simulation_utils import GameObject, Container

class NitricOxide(GameObject):
    def __init__(self, name, concentration=0):
        super().__init__(name)
        self.concentration = concentration  # Concentration of nitric oxide

    def tick(self):
        # Simulate the effect of nitric oxide concentration on vasospasm
        if self.concentration < 1:  # Threshold for vasospasm
            self.properties["vasospasm"] = True
        else:
            self.properties["vasospasm"] = False

    def makeDescriptionStr(self):
        return f"{self.name} with concentration {self.concentration} micromol/L, vasospasm: {self.properties.get('vasospasm', False)}."

class Vasospasm(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties["vasospasm"] = False

    def tick(self):
        # Check if vasospasm occurs based on nitric oxide levels
        if self.parent.getProperty("nitricOxide").concentration < 1:
            self.properties["vasospasm"] = True
        else:
            self.properties["vasospasm"] = False

    def makeDescriptionStr(self):
        return f"{self.name}, vasospasm status: {self.properties['vasospasm']}."

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
        nitric_oxide = NitricOxide("Nitric Oxide", concentration=0.4)  # Initial low concentration
        vasospasm = Vasospasm("Cerebral Vasospasm")
        world.addObject(nitric_oxide)
        world.addObject(vasospasm)
        vasospasm.parent = nitric_oxide  # Link vasospasm to nitric oxide
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("increase nitric oxide", ["increase"])
        self.addAction("decrease nitric oxide", ["decrease"])
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def actionIncrease(self):
        nitric_oxide = self.rootObject.containsItemWithName("Nitric Oxide")[0]
        nitric_oxide.concentration += 0.5  # Increase concentration
        return f"Increased nitric oxide concentration to {nitric_oxide.concentration} micromol/L."

    def actionDecrease(self):
        nitric_oxide = self.rootObject.containsItemWithName("Nitric Oxide")[0]
        nitric_oxide.concentration -= 0.5  # Decrease concentration
        return f"Decreased nitric oxide concentration to {nitric_oxide.concentration} micromol/L."

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase":
            self.observationStr = self.actionIncrease()
        elif actionVerb == "decrease":
            self.observationStr = self.actionDecrease()

        # Update the state of the world
        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "decrease nitric oxide", "look", "increase nitric oxide", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
