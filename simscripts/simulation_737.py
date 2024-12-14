
# Claim: MICAL redox enzymes regulate actin dynamics in many cell types.
# This simulation will test the claim by simulating the role of MICAL proteins in regulating actin dynamics.

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

class MICAL(GameObject):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type
        self.properties = {
            "actin_regulation": True,
            "reactive_oxygen_species": 0
        }

    def generateReactiveOxygenSpecies(self):
        self.properties["reactive_oxygen_species"] += 1

    def regulateActinDynamics(self):
        if self.properties["reactive_oxygen_species"] > 0:
            return f"{self.name} regulates actin dynamics."
        else:
            return f"{self.name} cannot regulate actin dynamics without reactive oxygen species."

class World(Container):
    def __init__(self):
        Container.__init__(self, "cell environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        mical1 = MICAL("MICAL1", "isoform")
        mical2 = MICAL("MICAL2", "isoform")
        mical3 = MICAL("MICAL3", "isoform")
        world.addObject(mical1)
        world.addObject(mical2)
        world.addObject(mical3)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("generate reactive oxygen species for MICAL1", ["generate", "MICAL1"])
        self.addAction("regulate actin dynamics for MICAL1", ["regulate", "MICAL1"])
        self.addAction("generate reactive oxygen species for MICAL2", ["generate", "MICAL2"])
        self.addAction("regulate actin dynamics for MICAL2", ["regulate", "MICAL2"])
        self.addAction("generate reactive oxygen species for MICAL3", ["generate", "MICAL3"])
        self.addAction("regulate actin dynamics for MICAL3", ["regulate", "MICAL3"])

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
        mical_name = action[1]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "generate":
            mical = self.rootObject.containsItemWithName(mical_name)[0]
            mical.generateReactiveOxygenSpecies()
            self.observationStr = f"{mical_name} generated reactive oxygen species."
        elif actionVerb == "regulate":
            mical = self.rootObject.containsItemWithName(mical_name)[0]
            self.observationStr = mical.regulateActinDynamics()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = [
        "look",
        "generate reactive oxygen species for MICAL1",
        "regulate actin dynamics for MICAL1",
        "generate reactive oxygen species for MICAL2",
        "regulate actin dynamics for MICAL2",
        "generate reactive oxygen species for MICAL3",
        "regulate actin dynamics for MICAL3"
    ]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
