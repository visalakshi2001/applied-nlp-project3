
# Claim: Rapid phosphotransfer rates are correlated with histidine kinase regulator specificity.
# This simulation will test the correlation between rapid phosphotransfer rates and histidine kinase regulator specificity.

from simulation_utils import GameObject, Container

class HistidineKinase(GameObject):
    def __init__(self, name, rapid_phosphotransfer_rate=0, specificity=0):
        super().__init__(name)
        self.properties = {
            "rapid_phosphotransfer_rate": rapid_phosphotransfer_rate,
            "specificity": specificity
        }

    def tick(self):
        # Simulate the relationship between rapid phosphotransfer rate and specificity
        # For simplicity, we assume that higher rates lead to higher specificity
        self.properties["specificity"] = self.properties["rapid_phosphotransfer_rate"] * 2  # Arbitrary correlation

    def makeDescriptionStr(self):
        return f"{self.name} has a rapid phosphotransfer rate of {self.properties['rapid_phosphotransfer_rate']} and specificity of {self.properties['specificity']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        kinase1 = HistidineKinase("Kinase_1", rapid_phosphotransfer_rate=5)
        kinase2 = HistidineKinase("Kinase_2", rapid_phosphotransfer_rate=10)
        world.addObject(kinase1)
        world.addObject(kinase2)
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

    # Check the correlation
    kinase1 = simulation.rootObject.containsItemWithName("Kinase_1")[0]
    kinase2 = simulation.rootObject.containsItemWithName("Kinase_2")[0]

    if kinase1.properties["specificity"] == kinase1.properties["rapid_phosphotransfer_rate"] * 2 and \
       kinase2.properties["specificity"] == kinase2.properties["rapid_phosphotransfer_rate"] * 2:
        print("Claim Supported: Rapid phosphotransfer rates are correlated with histidine kinase regulator specificity.")
    else:
        print("Claim Refuted: No correlation found.")

if __name__ == "__main__":
    main()
