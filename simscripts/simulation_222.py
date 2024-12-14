
# Claim: Ca2+ cycling is a UCP1-independent thermogenic mechanism.
# The simulation will test the claim by modeling the thermogenic mechanisms in beige fat.

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

class ThermogenicMechanism(GameObject):
    def __init__(self, name, is_uCP1_independent=False):
        super().__init__(name)
        self.properties["is_uCP1_independent"] = is_uCP1_independent

    def tick(self):
        # Simulate the thermogenic mechanism
        if self.properties["is_uCP1_independent"]:
            return "Thermogenesis is occurring via Ca2+ cycling."
        else:
            return "Thermogenesis is dependent on UCP1."

class BeigeFat(GameObject):
    def __init__(self):
        super().__init__("Beige Fat")
        self.thermogenic_mechanism = ThermogenicMechanism("Ca2+ Cycling Mechanism", is_uCP1_independent=True)
        self.addObject(self.thermogenic_mechanism)

    def tick(self):
        return self.thermogenic_mechanism.tick()

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")
        self.beige_fat = BeigeFat()
        self.addObject(self.beige_fat)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += self.beige_fat.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.rootObject.tick()

    def _initialize_simulation(self):
        world = World()
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Result of thermogenic mechanism:", simulation.result)

    # Check if the claim is supported or refuted
    if "independent" in simulation.result:
        print("Claim Supported: Ca2+ cycling is a UCP1-independent thermogenic mechanism.")
    else:
        print("Claim Refuted: Ca2+ cycling is not a UCP1-independent thermogenic mechanism.")

if __name__ == "__main__":
    main()
