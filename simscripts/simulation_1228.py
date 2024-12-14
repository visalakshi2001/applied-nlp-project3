
# Claim: The mean suicide rate in women is lower after miscarriage than live birth.
# The simulation will compare the suicide rates associated with live birth and miscarriage.

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

class PregnancyOutcome(GameObject):
    def __init__(self, name, suicide_rate):
        super().__init__(name)
        self.properties["suicide_rate"] = suicide_rate

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.compare_suicide_rates()

    def _initialize_simulation(self):
        world = Container("environment")
        live_birth = PregnancyOutcome("Live Birth", 5.9)
        miscarriage = PregnancyOutcome("Miscarriage", 18.1)
        world.addObject(live_birth)
        world.addObject(miscarriage)
        return world

    def compare_suicide_rates(self):
        live_birth_rate = self.rootObject.containsItemWithName("Live Birth")[0].properties["suicide_rate"]
        miscarriage_rate = self.rootObject.containsItemWithName("Miscarriage")[0].properties["suicide_rate"]

        if miscarriage_rate > live_birth_rate:
            self.result = "Refuted: The mean suicide rate in women is lower after miscarriage than live birth."
        else:
            self.result = "Supported: The mean suicide rate in women is lower after miscarriage than live birth."

def main():
    simulation = Simulation()
    print(simulation.result)

if __name__ == "__main__":
    main()
