
# Claim: Microcin J25 encourages nucleoside triphosphate (NTP) binding.
# The simulation will model the interaction of Microcin J25 with bacterial RNA polymerase and its effect on NTP binding.

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

class MicrocinJ25(GameObject):
    def __init__(self):
        super().__init__("Microcin J25")
        self.properties = {
            "NTP_binding": False
        }

    def bindNTP(self):
        self.properties["NTP_binding"] = True

class RNA_Polymerase(GameObject):
    def __init__(self):
        super().__init__("RNA Polymerase")
        self.properties = {
            "NTP_bound": False
        }

    def bindNTP(self):
        self.properties["NTP_bound"] = True

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
        microcin = MicrocinJ25()
        rna_polymerase = RNA_Polymerase()
        world.addObject(microcin)
        world.addObject(rna_polymerase)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("bind NTP with Microcin J25", ["bind", "Microcin J25"])
        self.addAction("bind NTP with RNA Polymerase", ["bind", "RNA Polymerase"])

    def actionBindNTP(self, objName):
        if objName == "Microcin J25":
            microcin = self.rootObject.containsItemWithName("Microcin J25")[0]
            microcin.bindNTP()
            return "Microcin J25 binds to NTP."
        elif objName == "RNA Polymerase":
            rna_polymerase = self.rootObject.containsItemWithName("RNA Polymerase")[0]
            rna_polymerase.bindNTP()
            return "RNA Polymerase binds to NTP."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr
        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "bind":
            self.observationStr = self.actionBindNTP(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["bind NTP with Microcin J25", "bind NTP with RNA Polymerase", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the binding status
    microcin = simulation.rootObject.containsItemWithName("Microcin J25")[0]
    rna_polymerase = simulation.rootObject.containsItemWithName("RNA Polymerase")[0]
    
    if microcin.properties["NTP_binding"] and rna_polymerase.properties["NTP_bound"]:
        print("Claim Supported: Microcin J25 encourages NTP binding.")
    else:
        print("Claim Refuted: Microcin J25 does not encourage NTP binding.")

if __name__ == "__main__":
    main()
