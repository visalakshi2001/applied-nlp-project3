
# Claim: Increased microtubule acetylation repairs interference of axonal transport caused by LRRK2 Roc-COR domain mutations.
# The simulation will model the effects of microtubule acetylation on axonal transport in the presence of LRRK2 mutations.

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
            "transport_status": "impaired"  # Initial state is impaired due to LRRK2 mutations
        }

    def increaseAcetylation(self):
        self.properties["acetylation_level"] += 1
        if self.properties["acetylation_level"] > 0:
            self.properties["transport_status"] = "restored"  # Transport is restored with increased acetylation

    def makeDescriptionStr(self):
        return f"A microtubule named {self.name} with acetylation level {self.properties['acetylation_level']} and transport status {self.properties['transport_status']}."

class LRRK2(GameObject):
    def __init__(self, name, mutation_status=False):
        super().__init__(name)
        self.properties = {
            "mutation_status": mutation_status  # True if mutated
        }

    def makeDescriptionStr(self):
        return f"LRRK2 protein named {self.name} with mutation status {'mutated' if self.properties['mutation_status'] else 'normal'}."

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
        microtubule = Microtubule("microtubule_1")
        lrrk2 = LRRK2("LRRK2_mutant", mutation_status=True)
        world.addObject(microtubule)
        world.addObject(lrrk2)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("increase acetylation of microtubule_1", ["increase", self.rootObject.contains[0]])  # microtubule

    def actionIncreaseAcetylation(self, microtubule):
        if type(microtubule) != Microtubule:
            return f"Cannot increase acetylation of {microtubule.name}."
        else:
            microtubule.increaseAcetylation()
            return f"You increase the acetylation of {microtubule.name}."

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
            self.observationStr = self.actionIncreaseAcetylation(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "increase acetylation of microtubule_1"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check to determine if the claim is supported or refuted
    microtubule = simulation.rootObject.contains[0]  # Accessing the microtubule object
    if microtubule.properties["transport_status"] == "restored":
        print("Claim Supported: Increased microtubule acetylation repairs interference of axonal transport.")
    else:
        print("Claim Refuted: Increased microtubule acetylation does not repair interference of axonal transport.")

if __name__ == "__main__":
    main()
