
# Claim: JMJD6 catalyzes the hydroxylation of C-terminal lysine and suppresses transcriptional activity.

# Importing necessary classes from the base template
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

class JMJD6(GameObject):
    def __init__(self):
        super().__init__("JMJD6")
        self.properties = {
            "hydroxylation": False,
            "transcriptional_activity": "suppressed"
        }

    def catalyze_hydroxylation(self):
        self.properties["hydroxylation"] = True

    def suppress_transcriptional_activity(self):
        self.properties["transcriptional_activity"] = "suppressed"

class P53(GameObject):
    def __init__(self):
        super().__init__("p53")
        self.properties = {
            "hydroxylated": False,
            "transcriptional_activity": "active"
        }

    def hydroxylate(self):
        self.properties["hydroxylated"] = True
        self.transcriptional_activity = "suppressed"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cell")
        jmjd6 = JMJD6()
        p53 = P53()
        world.addObject(jmjd6)
        world.addObject(p53)
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
                if isinstance(obj, JMJD6):
                    self.addAction(f"catalyze hydroxylation with {objReferent}", ["catalyze", obj])
                if isinstance(obj, P53):
                    self.addAction(f"check {objReferent} activity", ["check", obj])

    def actionCatalyze(self, jmjd6):
        if isinstance(jmjd6, JMJD6):
            jmjd6.catalyze_hydroxylation()
            jmjd6.suppress_transcriptional_activity()
            return f"{jmjd6.name} has catalyzed hydroxylation and suppressed transcriptional activity."
        return "Invalid action."

    def actionCheck(self, p53):
        if isinstance(p53, P53):
            if p53.properties["hydroxylated"]:
                return f"{p53.name} is hydroxylated and transcriptional activity is {p53.properties['transcriptional_activity']}."
            else:
                return f"{p53.name} is not hydroxylated."
        return "Invalid action."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]
        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "catalyze":
            self.observationStr = self.actionCatalyze(action[1])
        elif actionVerb == "check":
            self.observationStr = self.actionCheck(action[1])
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["catalyze hydroxylation with JMJD6", "check p53 activity"]
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
