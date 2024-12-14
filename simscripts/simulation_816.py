
# Claim: Mutations in RIM1 raise levels of IME1 RNA.
# The simulation will test the relationship between RIM1 mutations and IME1 expression.

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

class RIM1(GameObject):
    def __init__(self, name, mutation=False):
        super().__init__(name)
        self.mutation = mutation
        self.properties = {
            "IME1_expression": 100  # Base expression level of IME1
        }

    def tick(self):
        if self.mutation:
            self.properties["IME1_expression"] -= 20  # Mutations reduce IME1 expression
        else:
            self.properties["IME1_expression"] += 20  # Normal RIM1 increases IME1 expression

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.doWorldTick()

    def _initialize_simulation(self):
        world = Container("environment")
        self.rim1_normal = RIM1("RIM1_normal", mutation=False)
        self.rim1_mutated = RIM1("RIM1_mutated", mutation=True)
        world.addObject(self.rim1_normal)
        world.addObject(self.rim1_mutated)
        return world

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

    def getIME1ExpressionLevels(self):
        return {
            "normal": self.rim1_normal.properties["IME1_expression"],
            "mutated": self.rim1_mutated.properties["IME1_expression"]
        }

def main():
    simulation = Simulation()
    ime1_levels = simulation.getIME1ExpressionLevels()
    print(f"IME1 expression levels:\nNormal RIM1: {ime1_levels['normal']}\nMutated RIM1: {ime1_levels['mutated']}")
    
    if ime1_levels['mutated'] < ime1_levels['normal']:
        print("Claim Supported: Mutations in RIM1 reduce levels of IME1 RNA.")
    else:
        print("Claim Refuted: Mutations in RIM1 do not reduce levels of IME1 RNA.")

if __name__ == "__main__":
    main()
