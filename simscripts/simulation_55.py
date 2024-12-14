
# Claim: AMP-activated protein kinase (AMPK) activation reduces inflammation-related fibrosis in the lungs.
# The simulation will model the effects of AMPK activation on fibrotic activity in lung myofibroblasts.

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

class Myofibroblast(GameObject):
    def __init__(self, name, fibrotic_activity=1):
        super().__init__(name)
        self.fibrotic_activity = fibrotic_activity

    def activate_AMPK(self):
        self.fibrotic_activity -= 0.5  # AMPK activation reduces fibrotic activity

    def makeDescriptionStr(self):
        return f"{self.name} with fibrotic activity level: {self.fibrotic_activity}"

class Lung(Container):
    def __init__(self):
        super().__init__("Lung")
        self.myofibroblasts = [Myofibroblast(f"myofibroblast_{i}") for i in range(1, 4)]
        for mf in self.myofibroblasts:
            self.addObject(mf)

    def activate_AMPK_in_myofibroblasts(self):
        for mf in self.myofibroblasts:
            mf.activate_AMPK()

class Simulation:
    def __init__(self):
        self.lung = Lung()
        self.observationStr = self.lung.makeDescriptionStr()
        self.lung.activate_AMPK_in_myofibroblasts()

    def run(self):
        return self.lung.makeDescriptionStr()

def main():
    simulation = Simulation()
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
