
# Claim: MafA ubiquitination increases the recruitment of coactivator P/CAF by MafA.
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
        if propertyName in self.properties:
            return self.properties[propertyName]
        else:
            return None

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent != None:
            self.parent.removeObject(self)

    def getAllContainedObjectsRecursive(self):
        outList = []
        for obj in self.contains:
            outList.append(obj)
            outList.extend(obj.getAllContainedObjectsRecursive())
        return outList

    def containsItemWithName(self, name):
        foundObjects = []
        for obj in self.contains:
            if obj.name == name:
                foundObjects.append(obj)
        return foundObjects

    def tick(self):
        pass

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
        self.properties["containerPrefix"] = "in"

    def openContainer(self):
        if not self.getProperty("isOpenable"):
            return ("The " + self.name + " can't be opened.", False)
        if self.getProperty("isOpen"):
            return ("The " + self.name + " is already open.", False)
        self.properties["isOpen"] = True
        return ("The " + self.name + " is now open.", True)

    def closeContainer(self):
        if not (self.getProperty("isOpenable") == True):
            return ("The " + self.name + " can't be closed.", False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is already closed.", False)
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

class MafA(GameObject):
    def __init__(self):
        super().__init__("MafA")
        self.properties = {
            "isUbiquitinated": False,
            "PCAF_recruited": False
        }

    def ubiquitinate(self):
        self.properties["isUbiquitinated"] = True
        self.properties["PCAF_recruited"] = True  # Simulating that ubiquitination leads to recruitment of P/CAF

class PCAF(GameObject):
    def __init__(self):
        super().__init__("P/CAF")

class World(Container):
    def __init__(self):
        Container.__init__(self, "cell")
        self.mafa = MafA()
        self.pcaf = PCAF()
        self.addObject(self.mafa)
        self.addObject(self.pcaf)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += f"\t{self.mafa.makeDescriptionStr()} (Ubiquitinated: {self.mafa.properties['isUbiquitinated']}, P/CAF recruited: {self.mafa.properties['PCAF_recruited']})\n"
        outStr += f"\t{self.pcaf.makeDescriptionStr()}\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("ubiquitinate MafA", ["ubiquitinate", self.rootObject.mafa])

    def actionUbiquitinate(self, mafa):
        if type(mafa) != MafA:
            return f"Cannot ubiquitinate {mafa.name}."
        else:
            mafa.ubiquitate()
            return f"{mafa.name} has been ubiquitinated and P/CAF has been recruited."

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
            self.observationStr = self.actionUbiquitinate(action[1])

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
