
# Claim: siRNA knockdown of A20 accelerates tumor progression in an in vivo murine xenograft model.
# The simulation will test the effect of A20 knockdown on tumor growth in a murine model.

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

class Tumor(GameObject):
    def __init__(self, name, growth_rate=1):
        super().__init__(name)
        self.properties = {
            "growth_rate": growth_rate,
            "size": 0
        }

    def tick(self):
        self.properties["size"] += self.properties["growth_rate"]

    def makeDescriptionStr(self):
        return f"A tumor named {self.name} with size {self.properties['size']}."

class A20Knockdown(GameObject):
    def __init__(self, name, effect_on_growth=0):
        super().__init__(name)
        self.properties = {
            "effect_on_growth": effect_on_growth
        }

    def apply_effect(self, tumor):
        tumor.properties["growth_rate"] += self.properties["effect_on_growth"]

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
        tumor = Tumor("glioma_tumor")
        a20_knockdown = A20Knockdown("A20_knockdown", effect_on_growth=-2)  # Knockdown effect reduces growth rate
        world.addObject(tumor)
        world.addObject(a20_knockdown)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

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

        if actionVerb == "tick":
            tumor = self.rootObject.containsItemWithName("glioma_tumor")[0]
            a20_knockdown = self.rootObject.containsItemWithName("A20_knockdown")[0]
            a20_knockdown.apply_effect(tumor)
            tumor.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    for _ in range(5):  # Simulate 5 time steps
        print("Action: tick")
        obs = simulation.step("tick")
        print(obs)
        print()

if __name__ == "__main__":
    main()
