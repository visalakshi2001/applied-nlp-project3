
# Claim: Mouse models can be generated using "artificial spermatids."
# The simulation will check if live mice can be obtained from AG-haESCs, which are derived from artificial spermatids.

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

class Mouse(GameObject):
    def __init__(self, name, has_genetic_traits=False):
        super().__init__(name)
        self.properties["has_genetic_traits"] = has_genetic_traits

    def makeDescriptionStr(self):
        description = f"A {self.name} that {'has' if self.properties['has_genetic_traits'] else 'does not have'} genetic traits."
        return description

class Oocyte(GameObject):
    def __init__(self, name):
        super().__init__(name)

class AGhaESC(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def inject_into_oocyte(self, oocyte):
        # Simulate the injection of AG-haESCs into an oocyte
        return Mouse("Mouse", has_genetic_traits=True)

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
        ag_haesc = AGhaESC("AG-haESC")
        oocyte = Oocyte("MII Oocyte")
        world.addObject(ag_haesc)
        world.addObject(oocyte)

        # Simulate the injection of AG-haESCs into the oocyte
        live_mouse = ag_haesc.inject_into_oocyte(oocyte)
        world.addObject(live_mouse)

        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    live_mouse = simulation.rootObject.containsItemWithName("Mouse")
    if live_mouse and live_mouse[0].properties["has_genetic_traits"]:
        print("Claim Supported: Live mice can be generated using AG-haESCs.")
    else:
        print("Claim Refuted: Live mice cannot be generated.")

if __name__ == "__main__":
    main()
