
# The tissue surrounding the granuloma in an immune cell induces an anti-inflammatory immune response.

from simulation_utils import GameObject, Container

class Granuloma(GameObject):
    def __init__(self, name, pro_inflammatory=0, anti_inflammatory=0):
        super().__init__(name)
        self.properties = {
            "pro_inflammatory": pro_inflammatory,
            "anti_inflammatory": anti_inflammatory
        }

    def tick(self):
        # Simulate the environment of the granuloma
        # The surrounding tissue has an anti-inflammatory signature
        self.properties["anti_inflammatory"] = 1  # Represents the anti-inflammatory response
        self.properties["pro_inflammatory"] = 0   # Represents the lack of pro-inflammatory response

    def makeDescriptionStr(self):
        description = f"A {self.name} with pro-inflammatory response: {self.properties['pro_inflammatory']} and anti-inflammatory response: {self.properties['anti_inflammatory']}."
        return description

class ImmuneCell(GameObject):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("granuloma_environment")
        granuloma = Granuloma("granuloma")
        immune_cell = ImmuneCell("immune_cell")
        world.addObject(granuloma)
        world.addObject(immune_cell)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

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

    # Check the properties of the granuloma to determine if the claim is supported or refuted
    granuloma = simulation.rootObject.containsItemWithName("granuloma")[0]
    if granuloma.properties["anti_inflammatory"] > 0 and granuloma.properties["pro_inflammatory"] == 0:
        print("Claim Supported: The tissue surrounding the granuloma induces an anti-inflammatory immune response.")
    else:
        print("Claim Refuted: The tissue surrounding the granuloma does not induce an anti-inflammatory immune response.")

if __name__ == "__main__":
    main()
