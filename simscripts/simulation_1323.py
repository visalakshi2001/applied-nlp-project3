
# Claim: Treatment with a protein named FN impairs regenerative abilities of aged muscles.
# The simulation will model the effects of fibronectin (FN) on muscle stem cells (MuSCs) in aged muscles.

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

class MuscleStemCell(GameObject):
    def __init__(self, name, fn_level=0):
        super().__init__(name)
        self.properties = {
            "fn_level": fn_level,
            "is_regenerative": True
        }

    def tick(self):
        if self.properties["fn_level"] > 0:
            self.properties["is_regenerative"] = False  # FN impairs regeneration

class AgedMuscle(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.contains = [MuscleStemCell("MuSC_1", fn_level=1), MuscleStemCell("MuSC_2", fn_level=1)]  # FN present

class YoungMuscle(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.contains = [MuscleStemCell("MuSC_1", fn_level=0), MuscleStemCell("MuSC_2", fn_level=0)]  # No FN

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")
        self.addObject(AgedMuscle("Aged Muscle"))
        self.addObject(YoungMuscle("Young Muscle"))

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
            for cell in obj.contains:
                outStr += f"\t\t{cell.makeDescriptionStr()} - Regenerative: {cell.properties['is_regenerative']}\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
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
    print("Claim Verification:")
    if any(cell.properties["is_regenerative"] for cell in simulation.rootObject.contains[0].contains):
        print("Claim Refuted: Aged muscle stem cells are still regenerative.")
    else:
        print("Claim Supported: Aged muscle stem cells are not regenerative due to FN.")

if __name__ == "__main__":
    main()
