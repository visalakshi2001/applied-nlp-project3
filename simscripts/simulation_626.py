
# Claim: Induction of urokinase receptor signaling in podocytes causes foot process effacement and proteinuria.
# The simulation will model podocytes and their response to urokinase receptor signaling.

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

class Podocyte(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "uPAR_signaling": False,
            "foot_process_effacement": False,
            "proteinuria": 0
        }

    def induce_uPAR_signaling(self):
        self.properties["uPAR_signaling"] = True
        self.properties["foot_process_effacement"] = True
        self.properties["proteinuria"] += 1  # Increase proteinuria as a result of signaling

    def tick(self):
        if self.properties["uPAR_signaling"]:
            self.induce_uPAR_signaling()

    def makeDescriptionStr(self):
        description = f"A {self.name} with uPAR signaling: {self.properties['uPAR_signaling']}, "
        description += f"foot process effacement: {self.properties['foot_process_effacement']}, "
        description += f"proteinuria level: {self.properties['proteinuria']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "kidney environment")

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
        podocyte = Podocyte("podocyte_1")
        world.addObject(podocyte)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("induce uPAR signaling", ["induce", self.rootObject.contains[0]])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "induce":
            podocyte = action[1]
            podocyte.induce_uPAR_signaling()
            self.observationStr = f"{podocyte.name} has induced uPAR signaling."

        self.doWorldTick()
        return self.rootObject.makeDescriptionStr()

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    action = "induce uPAR signaling"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

if __name__ == "__main__":
    main()
