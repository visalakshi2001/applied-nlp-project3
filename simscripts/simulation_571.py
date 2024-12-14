
# Claim: In breast cancer, the loss of myoepithelial cells slows the transition of ductal carcinoma in situ to invasive carcinoma.
# The simulation will model the interaction between myoepithelial cells and the progression of ductal carcinoma in situ (DCIS) to invasive carcinoma.

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

class MyoepithelialCell(GameObject):
    def __init__(self, name, is_present=True):
        super().__init__(name)
        self.properties["is_present"] = is_present

class Fibroblast(GameObject):
    def __init__(self, name):
        super().__init__(name)

class DuctalCarcinomaInSitu(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties["is_invasive"] = False

    def transition_to_invasive(self, myoepithelial_cells):
        if not myoepithelial_cells.getProperty("is_present"):
            self.properties["is_invasive"] = True

class World(Container):
    def __init__(self):
        Container.__init__(self, "breast_tissue")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        myoepithelial_cells = MyoepithelialCell("myoepithelial_cells", is_present=True)
        fibroblast = Fibroblast("fibroblast")
        dcis = DuctalCarcinomaInSitu("ductal_carcinoma_in_situ")

        world.addObject(myoepithelial_cells)
        world.addObject(fibroblast)
        world.addObject(dcis)

        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("check transition", ["check"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "check":
            myoepithelial_cells = self.rootObject.containsItemWithName("myoepithelial_cells")[0]
            dcis = self.rootObject.containsItemWithName("ductal_carcinoma_in_situ")[0]
            dcis.transition_to_invasive(myoepithelial_cells)
            if dcis.getProperty("is_invasive"):
                return "The transition to invasive carcinoma has occurred."
            else:
                return "The transition to invasive carcinoma has not occurred."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.step("check transition")
    print(result)

if __name__ == "__main__":
    main()
