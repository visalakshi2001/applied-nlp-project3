
# Claim: G-CSF increases the expansion and infiltration of MDSCs into tumors.
# This simulation will model the relationship between G-CSF and MDSC accumulation in tumors.

from simulation_utils import GameObject, Container

class MDSC(GameObject):
    def __init__(self, name, gcsf_level=0):
        super().__init__(name)
        self.gcsf_level = gcsf_level
        self.properties = {
            "gcsf_level": gcsf_level,
            "infiltration": 0
        }

    def tick(self):
        # MDSC infiltration increases with G-CSF levels
        self.properties["infiltration"] = self.gcsf_level * 2  # Arbitrary multiplier for simulation

    def makeDescriptionStr(self):
        return f"A {self.name} with G-CSF level {self.gcsf_level} and infiltration level {self.properties['infiltration']}."

class Tumor(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.gcsf_level = 0

    def increase_gcsf(self, amount):
        self.gcsf_level += amount
        return f"G-CSF level increased to {self.gcsf_level}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        tumor = Tumor("tumor_1")
        mdsc = MDSC("MDSC_1")
        world.addObject(tumor)
        world.addObject(mdsc)
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

        for objReferent, objs in allObjects.items():
            for obj in objs:
                if isinstance(obj, Tumor):
                    self.addAction(f"increase G-CSF of {objReferent}", ["increase_gcsf", obj, 5])  # Increase G-CSF by 5
                if isinstance(obj, MDSC):
                    self.addAction(f"tick {objReferent}", ["tick", obj])

    def actionIncreaseGCSF(self, tumor, amount):
        return tumor.increase_gcsf(amount)

    def actionTick(self, mdsc):
        mdsc.tick()
        return f"{mdsc.name} ticked. Current infiltration: {mdsc.properties['infiltration']}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase_gcsf":
            self.observationStr = self.actionIncreaseGCSF(action[1], action[2])
        elif actionVerb == "tick":
            self.observationStr = self.actionTick(action[1])

        # Do one tick of the environment
        self.doWorldTick()
        self.generatePossibleActions()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if isinstance(obj, MDSC):
                obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["increase G-CSF of tumor_1", "tick MDSC_1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
