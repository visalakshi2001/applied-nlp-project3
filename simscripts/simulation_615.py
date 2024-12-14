
# Claim: Increased microtubule acetylation worsens interference of axonal transport caused by LRRK2 Roc-COR domain mutations.
# This simulation will test the effects of microtubule acetylation on axonal transport in the context of LRRK2 mutations.

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

class Microtubule(GameObject):
    def __init__(self, name, acetylation_level=0):
        super().__init__(name)
        self.properties = {
            "acetylation_level": acetylation_level,
            "transport_efficiency": 100  # 100% efficiency at baseline
        }

    def tick(self):
        # Simulate the effect of acetylation on transport efficiency
        if self.properties["acetylation_level"] > 0:
            self.properties["transport_efficiency"] -= self.properties["acetylation_level"] * 10  # Arbitrary reduction
            if self.properties["transport_efficiency"] < 0:
                self.properties["transport_efficiency"] = 0

class LRRK2(GameObject):
    def __init__(self, name, mutation_effect=0):
        super().__init__(name)
        self.properties = {
            "mutation_effect": mutation_effect,
            "transport_interference": 0  # No interference at baseline
        }

    def tick(self):
        # Simulate the effect of LRRK2 mutations on transport interference
        self.properties["transport_interference"] += self.properties["mutation_effect"]

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("cell environment")
        microtubule = Microtubule("microtubule_1", acetylation_level=5)  # Increased acetylation
        lrrk2 = LRRK2("LRRK2_mutant", mutation_effect=20)  # Mutation effect
        world.addObject(microtubule)
        world.addObject(lrrk2)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
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

        if (actionVerb == "look"):
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
    simulation.step("look")
    microtubule = simulation.rootObject.containsItemWithName("microtubule_1")[0]
    lrrk2 = simulation.rootObject.containsItemWithName("LRRK2_mutant")[0]
    
    # Check the transport efficiency and interference
    transport_efficiency = microtubule.properties["transport_efficiency"]
    transport_interference = lrrk2.properties["transport_interference"]

    if transport_efficiency < 100 and transport_interference > 0:
        result = "Supported: Increased microtubule acetylation worsens interference of axonal transport."
    else:
        result = "Refuted: Increased microtubule acetylation does not worsen interference of axonal transport."

    print(result)

if __name__ == "__main__":
    main()
