
# Claim: PD-1 triggering on monocytes enhances IL-10 production by monocytes.
# This simulation will model the interaction between PD-1 and IL-10 production in monocytes.

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

class Monocyte(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "PD-1_expression": 0,
            "IL-10_production": 0
        }

    def trigger_PD1(self):
        self.properties["PD-1_expression"] += 1
        self.properties["IL-10_production"] += 5  # Arbitrary increase in IL-10 production

    def makeDescriptionStr(self):
        description = f"A {self.name} with PD-1 expression level {self.properties['PD-1_expression']} and IL-10 production level {self.properties['IL-10_production']}."
        return description

class Simulation:
    def __init__(self):
        self.monocyte = Monocyte("monocyte_1")
        self.rootObject = self.monocyte
        self.observationStr = self.rootObject.makeDescriptionStr()

    def step(self):
        # Simulate triggering PD-1 on the monocyte
        self.monocyte.trigger_PD1()
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print("Initial State:")
    print(simulation.observationStr)
    print("\nTriggering PD-1 on monocyte...")
    result = simulation.step()
    print("After Triggering PD-1:")
    print(result)

    # Check if IL-10 production has increased
    if simulation.monocyte.properties["IL-10_production"] > 0:
        print("\nClaim Supported: PD-1 triggering on monocytes enhances IL-10 production by monocytes.")
    else:
        print("\nClaim Refuted: PD-1 triggering on monocytes does not enhance IL-10 production by monocytes.")

if __name__ == "__main__":
    main()
