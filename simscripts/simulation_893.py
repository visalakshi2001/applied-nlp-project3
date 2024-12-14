
# Claim: Osteocytes have an essential role in G-CSF induced HSPC mobilization.
# The simulation will model the interaction between osteocytes and HSPCs in response to G-CSF.

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

class Osteocyte(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "HSPC_mobilization": False
        }

    def respond_to_GCSF(self):
        self.properties["HSPC_mobilization"] = True

class HSPC(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_mobilized": False
        }

    def mobilize(self):
        self.properties["is_mobilized"] = True

class GCSF(GameObject):
    def __init__(self, name):
        super().__init__(name)

class World(Container):
    def __init__(self):
        Container.__init__(self, "bone marrow environment")

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
        osteocyte = Osteocyte("osteocyte_1")
        hspc = HSPC("HSPC_1")
        gcsf = GCSF("G-CSF")
        world.addObject(osteocyte)
        world.addObject(hspc)
        world.addObject(gcsf)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("administer G-CSF", ["administer", "G-CSF"])

    def administer_GCSF(self):
        osteocyte = self.rootObject.containsItemWithName("osteocyte_1")[0]
        hspc = self.rootObject.containsItemWithName("HSPC_1")[0]
        osteocyte.respond_to_GCSF()
        if osteocyte.properties["HSPC_mobilization"]:
            hspc.mobilize()
            return "G-CSF administered. Osteocyte responded and HSPC is mobilized."
        else:
            return "G-CSF administered. Osteocyte did not respond."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "administer":
            self.observationStr = self.administer_GCSF()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "administer G-CSF"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check if the claim is supported or refuted
    osteocyte = simulation.rootObject.containsItemWithName("osteocyte_1")[0]
    hspc = simulation.rootObject.containsItemWithName("HSPC_1")[0]
    if osteocyte.properties["HSPC_mobilization"] and hspc.properties["is_mobilized"]:
        print("Claim Supported: Osteocytes have an essential role in G-CSF induced HSPC mobilization.")
    else:
        print("Claim Refuted: Osteocytes do not have an essential role in G-CSF induced HSPC mobilization.")

if __name__ == "__main__":
    main()
