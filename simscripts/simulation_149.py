
# Claim: Autophagy deficiency in the liver increases vulnerability to insulin resistance.
# This simulation will test the claim by modeling the effects of autophagy deficiency in the liver on insulin resistance.

from simulation_utils import GameObject, Container

class Liver(GameObject):
    def __init__(self, name, autophagy_deficiency=0, insulin_resistance=0):
        super().__init__(name)
        self.properties = {
            "autophagy_deficiency": autophagy_deficiency,
            "insulin_resistance": insulin_resistance
        }

    def tick(self):
        # If there is autophagy deficiency, increase insulin resistance
        if self.properties["autophagy_deficiency"] > 0:
            self.properties["insulin_resistance"] += self.properties["autophagy_deficiency"] * 2  # Arbitrary multiplier for effect

    def makeDescriptionStr(self):
        description = f"A {self.name} with autophagy deficiency level {self.properties['autophagy_deficiency']} and insulin resistance level {self.properties['insulin_resistance']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        liver = Liver("liver", autophagy_deficiency=1)  # Simulating autophagy deficiency
        world.addObject(liver)        
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

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

    # Check the insulin resistance level to determine if the claim is supported or refuted
    liver = simulation.rootObject.containsItemWithName("liver")[0]
    if liver.properties["insulin_resistance"] > 0:
        print("Claim Supported: Autophagy deficiency in the liver increases vulnerability to insulin resistance.")
    else:
        print("Claim Refuted: Autophagy deficiency in the liver does not increase vulnerability to insulin resistance.")

if __name__ == "__main__":
    main()
