
# Claim: The M2-phenotype in brown adipose tissue macrophages increases brown adipose tissue thermogenic activity.
# This simulation will model the effect of M2-phenotype macrophages on thermogenic activity in brown adipose tissue.

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

class Macrophage(GameObject):
    def __init__(self, name, phenotype):
        super().__init__(name)
        self.properties = {
            "phenotype": phenotype,
            "thermogenic_activity": 0
        }

    def activate(self):
        if self.properties["phenotype"] == "M2":
            self.properties["thermogenic_activity"] += 10  # Arbitrary increase in thermogenic activity
        return self.properties["thermogenic_activity"]

class BrownAdiposeTissue(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "thermogenic_genes_expressed": 0
        }

    def express_thermogenic_genes(self, macrophage):
        if macrophage.properties["phenotype"] == "M2":
            self.properties["thermogenic_genes_expressed"] += macrophage.activate()
        return self.properties["thermogenic_genes_expressed"]

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
        macrophage_m2 = Macrophage("M2 Macrophage", "M2")
        brown_adipose_tissue = BrownAdiposeTissue("Brown Adipose Tissue")
        world.addObject(macrophage_m2)
        world.addObject(brown_adipose_tissue)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("activate M2 macrophage", ["activate", allObjects[0]])  # Assuming M2 macrophage is the first object
        self.addAction("express thermogenic genes", ["express", allObjects[1]])  # Assuming brown adipose tissue is the second object

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "activate":
            macrophage = action[1]
            macrophage.activate()
            self.observationStr = f"{macrophage.name} activated. Current thermogenic activity: {macrophage.properties['thermogenic_activity']}."
        elif actionVerb == "express":
            adipose_tissue = action[1]
            expressed_genes = adipose_tissue.express_thermogenic_genes(action[1])
            self.observationStr = f"Thermogenic genes expressed in {adipose_tissue.name}. Total expressed: {expressed_genes}."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "activate M2 macrophage", "express thermogenic genes"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
