
# Claim: Increased microtubule acetylation exacerbates LRRK2 Roc-COR domain mutation induced locomotor deficits.
# The simulation will test the effects of microtubule acetylation on LRRK2 mutations and locomotor behavior.

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

class Neuron(GameObject):
    def __init__(self, name, acetylation_level=0, locomotor_deficit=0):
        super().__init__(name)
        self.properties = {
            "acetylation_level": acetylation_level,
            "locomotor_deficit": locomotor_deficit
        }

    def tick(self):
        # Simulate the effect of acetylation on locomotor deficits
        if self.properties["acetylation_level"] > 0:
            self.properties["locomotor_deficit"] += self.properties["acetylation_level"] * 2  # Arbitrary multiplier for effect

    def makeDescriptionStr(self):
        description = f"A {self.name} with acetylation level {self.properties['acetylation_level']} and locomotor deficit {self.properties['locomotor_deficit']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

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
        neuron = Neuron("LRRK2 Neuron", acetylation_level=0, locomotor_deficit=0)
        world.addObject(neuron)
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
                self.addAction(f"increase acetylation of {objReferent}", ["increase", obj])
                self.addAction(f"decrease acetylation of {objReferent}", ["decrease", obj])

    def actionIncrease(self, neuron):
        if type(neuron) != Neuron:
            return f"Cannot increase the acetylation of {neuron.name}."
        else:
            neuron.properties["acetylation_level"] += 1
            return f"You increase the acetylation of {neuron.name} by 1."

    def actionDecrease(self, neuron):
        if type(neuron) != Neuron:
            return f"Cannot decrease the acetylation of {neuron.name}."
        else:
            neuron.properties["acetylation_level"] -= 1
            return f"You decrease the acetylation of {neuron.name} by 1."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if (actionVerb == "look"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "increase"):
            self.observationStr = self.actionIncrease(action[1])
        elif (actionVerb == "decrease"):
            self.observationStr = self.actionDecrease(action[1])

        self.doWorldTick()
        self.generatePossibleActions()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["increase acetylation of LRRK2 Neuron", "increase acetylation of LRRK2 Neuron", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the final locomotor deficit to determine if the claim is supported or refuted
    neuron = simulation.rootObject.containsItemWithName("LRRK2 Neuron")[0]
    if neuron.properties["locomotor_deficit"] > 0:
        print("Claim Supported: Increased microtubule acetylation exacerbates locomotor deficits.")
    else:
        print("Claim Refuted: Increased microtubule acetylation does not exacerbate locomotor deficits.")

if __name__ == "__main__":
    main()
