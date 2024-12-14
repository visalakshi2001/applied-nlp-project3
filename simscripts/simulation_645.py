
# Claim: Intake of folic acid (FA) and vitamin B6 (VB6) increases levels of homocysteine.

from simulation_utils import GameObject, Container

class Vitamin(GameObject):
    def __init__(self, name, intake=0):
        super().__init__(name)
        self.intake = intake
        self.homocysteine_level = 0

    def tick(self):
        # Simulate the effect of vitamin intake on homocysteine levels
        self.homocysteine_level = max(0, self.intake - 5)  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        return f"{self.name} intake is {self.intake} and homocysteine level is {self.homocysteine_level}."

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
        folic_acid = Vitamin("Folic Acid", intake=10)  # Initial intake
        vitamin_B6 = Vitamin("Vitamin B6", intake=8)    # Initial intake
        world.addObject(folic_acid)
        world.addObject(vitamin_B6)        
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"increase intake of {objReferent}", ["increase", obj])

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def actionIncrease(self, vitamin):
        if type(vitamin) != Vitamin:
            return f"Cannot increase the intake of {vitamin.name}."
        else:
            vitamin.intake += 2  # Increase intake
            return f"You increase the intake of {vitamin.name} by 2."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb.startswith("increase"):
            self.observationStr = self.actionIncrease(action[1])

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["increase intake of Folic Acid", "increase intake of Vitamin B6", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
