
# Claim: Chenodeoxycholic acid treatment increases brown adipose tissue activity.
# The simulation will test the effect of chenodeoxycholic acid (CDCA) on brown adipose tissue (BAT) activity.

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

class BrownAdiposeTissue(GameObject):
    def __init__(self, name, activity_level=0):
        super().__init__(name)
        self.activity_level = activity_level
        self.properties = {
            "activity_level": activity_level
        }

    def increase_activity(self):
        self.activity_level += 1
        self.properties["activity_level"] = self.activity_level

    def makeDescriptionStr(self):
        return f"{self.name} with activity level: {self.activity_level}"

class ChenodeoxycholicAcid(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def treat(self, bat):
        bat.increase_activity()

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

    def _initialize_simulation(self):
        world = World()
        bat = BrownAdiposeTissue("Brown Adipose Tissue")
        cdca = ChenodeoxycholicAcid("Chenodeoxycholic Acid")
        world.addObject(bat)
        world.addObject(cdca)
        return world

    def step(self):
        # Simulate the treatment with CDCA
        cdca = self.rootObject.containsItemWithName("Chenodeoxycholic Acid")[0]
        bat = self.rootObject.containsItemWithName("Brown Adipose Tissue")[0]
        cdca.treat(bat)

    def run(self):
        self.step()
        return self.rootObject.makeDescriptionStr()

def main():
    simulation = Simulation()
    print("Before treatment:")
    print(simulation.observationStr)
    print("After treatment:")
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
