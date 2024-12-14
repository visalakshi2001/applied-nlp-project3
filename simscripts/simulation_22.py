
# Claim: 76-85% of people with severe mental disorder receive no treatment in low and middle income countries.
# The simulation will model the treatment status of individuals with severe mental disorders in low and middle income countries.

from simulation_utils import GameObject, Container

class Individual(GameObject):
    def __init__(self, name, has_severe_disorder=False, received_treatment=False):
        super().__init__(name)
        self.properties = {
            "has_severe_disorder": has_severe_disorder,
            "received_treatment": received_treatment
        }

    def tick(self):
        # Simulate treatment status based on the severity of the disorder
        if self.properties["has_severe_disorder"] and not self.properties["received_treatment"]:
            # 76.3% to 85.4% of severe cases receive no treatment
            import random
            if random.random() < 0.8:  # 80% chance of not receiving treatment
                self.properties["received_treatment"] = False
            else:
                self.properties["received_treatment"] = True

    def makeDescriptionStr(self):
        treatment_status = "received treatment" if self.properties["received_treatment"] else "did not receive treatment"
        return f"{self.name}, has severe disorder: {self.properties['has_severe_disorder']}, {treatment_status}."

class World(Container):
    def __init__(self):
        super().__init__("environment")

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
        # Create individuals with severe mental disorders
        for i in range(100):  # Simulating 100 individuals
            individual = Individual(f"Individual_{i+1}", has_severe_disorder=True)
            world.addObject(individual)
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
