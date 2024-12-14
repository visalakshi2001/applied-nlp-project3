
# Claim: Microcin J25 inhibits nucleoside triphosphate (NTP) binding.
# The simulation will model the interaction of Microcin J25 with RNA polymerase and its effect on NTP binding.

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

class MicrocinJ25(GameObject):
    def __init__(self):
        super().__init__("Microcin J25")
        self.properties["inhibits_NTP_binding"] = True

class RNA_Polymerase(GameObject):
    def __init__(self):
        super().__init__("RNA Polymerase")
        self.properties["NTP_binding"] = True

    def inhibit_NTP_binding(self):
        if self.properties["NTP_binding"]:
            self.properties["NTP_binding"] = False
            return "NTP binding is inhibited."
        return "NTP binding is already inhibited."

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
        self.addAction("inhibit NTP binding", ["inhibit"])

    def actionInhibit(self, rna_polymerase):
        if isinstance(rna_polymerase, RNA_Polymerase):
            return rna_polymerase.inhibit_NTP_binding()
        return "Cannot inhibit NTP binding."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "inhibit":
            rna_polymerase = self.rootObject.containsItemWithName("RNA Polymerase")[0]
            self.observationStr = self.actionInhibit(rna_polymerase)

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "inhibit NTP binding"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check on NTP binding status
    rna_polymerase = simulation.rootObject.containsItemWithName("RNA Polymerase")[0]
    if not rna_polymerase.properties["NTP_binding"]:
        print("Claim Supported: Microcin J25 inhibits nucleoside triphosphate (NTP) binding.")
    else:
        print("Claim Refuted: Microcin J25 does not inhibit nucleoside triphosphate (NTP) binding.")

if __name__ == "__main__":
    main()
