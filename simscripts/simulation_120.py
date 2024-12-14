
# Claim: Antidepressants reduce the severity of migraines.
# This simulation will evaluate the effectiveness of tricyclic antidepressants on migraine severity.

from simulation_utils import GameObject, Container

class Antidepressant(GameObject):
    def __init__(self, name, effectiveness=0):
        super().__init__(name)
        self.effectiveness = effectiveness  # Effectiveness in reducing migraine severity

    def tick(self):
        # Simulate the effect of the antidepressant over time
        self.effectiveness += 0.1  # Increase effectiveness over time

class Migraine(GameObject):
    def __init__(self, name, severity=10):
        super().__init__(name)
        self.severity = severity  # Initial severity of the migraine

    def reduce_severity(self, antidepressant):
        # Reduce severity based on the effectiveness of the antidepressant
        reduction = antidepressant.effectiveness * 2  # Arbitrary factor for severity reduction
        self.severity = max(0, self.severity - reduction)  # Ensure severity doesn't go below 0

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
        antidepressant = Antidepressant("Tricyclic Antidepressant")
        migraine = Migraine("Migraine")
        world.addObject(antidepressant)
        world.addObject(migraine)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("treat migraine", ["treat"])

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
        elif actionVerb == "treat":
            antidepressant = self.rootObject.containsItemWithName("Tricyclic Antidepressant")[0]
            migraine = self.rootObject.containsItemWithName("Migraine")[0]
            migraine.reduce_severity(antidepressant)
            self.observationStr = f"The migraine severity is now {migraine.severity}."

        # Do one tick of the environment
        self.doWorldTick()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if isinstance(obj, Antidepressant):
                obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "treat migraine"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final assessment of the claim based on the last migraine severity
    final_migraine = simulation.rootObject.containsItemWithName("Migraine")[0]
    if final_migraine.severity < 10:  # If severity has reduced from initial
        print("Claim Supported: Antidepressants reduce the severity of migraines.")
    else:
        print("Claim Refuted: Antidepressants do not reduce the severity of migraines.")

if __name__ == "__main__":
    main()
