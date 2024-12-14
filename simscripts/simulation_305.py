
# Claim: DRD1 proteins enable Pol V transcription in vivo.
# The simulation will check if Pol V transcription is dependent on the presence of DRD1 proteins.

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

class DRD1(GameObject):
    def __init__(self):
        super().__init__("DRD1 Protein")
        self.properties["enabled"] = False

    def enable_transcription(self):
        self.properties["enabled"] = True

class PolV(GameObject):
    def __init__(self):
        super().__init__("Pol V")
        self.properties["transcribing"] = False

    def start_transcription(self, drd1):
        if drd1.getProperty("enabled"):
            self.properties["transcribing"] = True
            return "Pol V transcription has started."
        else:
            return "Pol V transcription cannot start without DRD1."

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        drd1 = DRD1()
        pol_v = PolV()
        world.addObject(drd1)
        world.addObject(pol_v)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "enable DRD1": ["enable", self.rootObject.contains[0]],  # DRD1
            "start Pol V transcription": ["start", self.rootObject.contains[1]]  # Pol V
        }

    def step(self, actionStr):
        action = self.possibleActions.get(actionStr)
        if action:
            actionVerb = action[0]
            target = action[1]

            if actionVerb == "enable":
                target.enable_transcription()
                return "DRD1 has been enabled."
            elif actionVerb == "start":
                result = target.start_transcription(self.rootObject.contains[0])  # Pass DRD1 to Pol V
                return result
        else:
            return "Unknown action."

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    actions = ["enable DRD1", "start Pol V transcription"]
    for action in actions:
        print(f"Action: {action}")
        result = simulation.step(action)
        print(result)

if __name__ == "__main__":
    main()
