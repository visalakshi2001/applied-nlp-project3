
# Claim: MafA ubiquitination decreases the recruitment of coactivator P/CAF by MafA.
# The simulation will model the relationship between MafA, its ubiquitination, and the recruitment of P/CAF.

class GameObject():
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            return
        self.constructorsRun = ["GameObject"]
        self.name = name
        self.parent = None
        self.contains = []
        self.properties = {}

    def getProperty(self, propertyName):
        return self.properties.get(propertyName, None)

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent is not None:
            self.parent.removeObject(self)

    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            outList.append(obj)
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

    def makeDescriptionStr(self):
        return self.name

class Container(GameObject):
    def __init__(self, name):
        if hasattr(self, "constructorsRun"):
            if "Container" in self.constructorsRun:
                return
        GameObject.__init__(self, name)
        self.constructorsRun.append("Container")
        self.properties["isContainer"] = True
        self.properties["isOpenable"] = False
        self.properties["isOpen"] = True

class MafA(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "isUbiquitinated": False,
            "PCAF_recruitment": True
        }

    def ubiquitinate(self):
        self.properties["isUbiquitinated"] = True
        self.properties["PCAF_recruitment"] = False  # Ubiquitination decreases recruitment

    def makeDescriptionStr(self):
        return f"{self.name} - Ubiquitinated: {self.properties['isUbiquitinated']}, P/CAF Recruitment: {self.properties['PCAF_recruitment']}"

class PCAF(GameObject):
    def __init__(self, name):
        super().__init__(name)

class World(Container):
    def __init__(self):
        Container.__init__(self, "MafA Environment")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        mafA = MafA("MafA")
        pcaf = PCAF("P/CAF")
        world.addObject(mafA)
        world.addObject(pcaf)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("ubiquitinate MafA", ["ubiquitinate", self.rootObject.contains[0]])  # MafA is the first object

    def addAction(self, actionStr, actionArgs):
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
        elif actionVerb == "ubiquitinate":
            mafA = action[1]
            mafA.ubiquitinate()
            self.observationStr = f"{mafA.name} has been ubiquitinated."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "ubiquitinate MafA", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
