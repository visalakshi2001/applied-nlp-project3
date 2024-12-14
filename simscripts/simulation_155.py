
# Claim: BCL-2 activation antagonizes the apoptotic effects of c-Myc.
# The simulation will model the relationship between BCL-2 and c-Myc in a cancer context.

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

    def placeObjectInContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)
        if not (obj.getProperty("isMoveable") == True):
            return ("The " + obj.name + " is not moveable.", None, False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be placed there.", False)
        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    def takeObjectFromContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)
        if not obj.getProperty("isMoveable"):
            return ("The " + obj.name + " is not moveable.", None, False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)
        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)
        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

class BCL2(GameObject):
    def __init__(self):
        super().__init__("BCL-2")
        self.properties = {
            "isActive": True,
            "cellDeath": False
        }

    def tick(self):
        if self.properties["isActive"]:
            self.properties["cellDeath"] = False  # BCL-2 prevents cell death
        else:
            self.properties["cellDeath"] = True  # Without BCL-2, cell death occurs

class cMyc(GameObject):
    def __init__(self):
        super().__init__("c-Myc")
        self.properties = {
            "promotesCellDeath": True
        }

    def tick(self):
        if self.properties["promotesCellDeath"]:
            return "c-Myc promotes cell death."
        return "c-Myc does not promote cell death."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cancer environment")
        bcl2 = BCL2()
        cmyc = cMyc()
        world.addObject(bcl2)
        world.addObject(cmyc)
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
        self.addAction("activate BCL-2", ["activate", allObjects["BCL-2"][0]])
        self.addAction("deactivate BCL-2", ["deactivate", allObjects["BCL-2"][0]])

    def actionActivate(self, bcl2):
        bcl2.properties["isActive"] = True
        return "BCL-2 is activated."

    def actionDeactivate(self, bcl2):
        bcl2.properties["isActive"] = False
        return "BCL-2 is deactivated."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "activate":
            self.observationStr = self.actionActivate(action[1])
        elif actionVerb == "deactivate":
            self.observationStr = self.actionDeactivate(action[1])

        # Call tick for BCL-2 and c-Myc
        for obj in self.rootObject.contains:
            obj.tick()

        # Check the state of BCL-2 and c-Myc
        bcl2 = self.rootObject.containsItemWithName("BCL-2")[0]
        cmyc = self.rootObject.containsItemWithName("c-Myc")[0]
        if bcl2.properties["cellDeath"]:
            self.observationStr += " Cell death occurs due to lack of BCL-2."
        else:
            self.observationStr += " BCL-2 is preventing cell death."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "deactivate BCL-2", "look", "activate BCL-2", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
