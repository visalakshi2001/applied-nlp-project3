
# Claim: Rapamycin delays aging in fruit flies.
# This simulation will test the claim by simulating the effects of rapamycin on the lifespan of fruit flies (Drosophila).

from simulation_utils import GameObject, Container

class FruitFly(GameObject):
    def __init__(self, name, lifespan=30, is_treated=False):
        super().__init__(name)
        self.lifespan = lifespan  # Default lifespan of the fruit fly
        self.is_treated = is_treated  # Whether the fly has been treated with rapamycin

    def tick(self):
        if self.is_treated:
            self.lifespan += 10  # Rapamycin treatment increases lifespan by 10 days
        self.lifespan -= 1  # Each tick represents a day of life

    def makeDescriptionStr(self):
        return f"A {self.name} with a current lifespan of {self.lifespan} days."

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
        untreated_fly = FruitFly("untreated_fly")
        treated_fly = FruitFly("treated_fly", is_treated=True)
        world.addObject(untreated_fly)
        world.addObject(treated_fly)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

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

        if actionVerb == "tick":
            # Simulate the passing of time
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                obj.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate for a number of days to observe the lifespan effects
    for _ in range(15):  # Simulate 15 days
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

    # Check the final lifespans to determine if the claim is supported
    untreated_fly = simulation.rootObject.containsItemWithName("untreated_fly")[0]
    treated_fly = simulation.rootObject.containsItemWithName("treated_fly")[0]

    if treated_fly.lifespan > untreated_fly.lifespan:
        print("Claim Supported: Rapamycin delays aging in fruit flies.")
    else:
        print("Claim Refuted: Rapamycin does not delay aging in fruit flies.")

if __name__ == "__main__":
    main()
