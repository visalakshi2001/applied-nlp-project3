
# Claim: BCL-2 promotes the apoptotic effects of c-Myc.
# The simulation will test the relationship between BCL-2 and c-Myc in a cancer model.

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

class BCL2(GameObject):
    def __init__(self):
        super().__init__("BCL-2")
        self.properties = {
            "apoptotic_effect": 0
        }

    def tick(self):
        # Simulate the effect of BCL-2 on apoptosis
        self.properties["apoptotic_effect"] += 1  # BCL-2 promotes survival, so we increase the apoptotic effect

class cMyc(GameObject):
    def __init__(self):
        super().__init__("c-Myc")
        self.properties = {
            "apoptotic_signal": 0
        }

    def tick(self):
        # Simulate the effect of c-Myc on apoptosis
        self.properties["apoptotic_signal"] += 2  # c-Myc promotes apoptosis

class CancerCell(GameObject):
    def __init__(self):
        super().__init__("Cancer Cell")
        self.properties = {
            "is_alive": True,
            "apoptosis": 0
        }

    def tick(self, bcl2, cmyc):
        # Calculate the net effect of BCL-2 and c-Myc on the cancer cell
        self.properties["apoptosis"] += cmyc.properties["apoptotic_signal"] - bcl2.properties["apoptotic_effect"]
        if self.properties["apoptosis"] > 0:
            self.properties["is_alive"] = False  # Cell undergoes apoptosis

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
        bcl2 = BCL2()
        cmyc = cMyc()
        cancer_cell = CancerCell()
        world.addObject(bcl2)
        world.addObject(cmyc)
        world.addObject(cancer_cell)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."
        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            # Perform a tick in the simulation
            allObjects = self.rootObject.getAllContainedObjectsRecursive()
            for obj in allObjects:
                if isinstance(obj, (BCL2, cMyc, CancerCell)):
                    obj.tick()
            return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    for _ in range(5):  # Simulate for 5 ticks
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)

if __name__ == "__main__":
    main()
