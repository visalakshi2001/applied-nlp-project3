
# Claim: Active caspase-11 participate in regulating phagosome-lysosome fusion.

# simulation_utils.py
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

    def placeObjectInContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)

        if not (obj.getProperty("isMoveable") == True):
            return ("The " + obj.name + " is not moveable.", None, False)

        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be placed there.", False)

        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    def takeObjectFromContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)

        if not obj.getProperty("isMoveable"):
            return ("The " + obj.name + " is not moveable.", None, False)

        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)

        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)

        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

class Caspase(GameObject):
    def __init__(self, name, active=False):
        super().__init__(name)
        self.properties = {
            "active": active
        }

    def activate(self):
        self.properties["active"] = True

    def deactivate(self):
        self.properties["active"] = False

    def isActive(self):
        return self.properties["active"]

class Phagosome(GameObject):
    def __init__(self, name):
        super().__init__(name)

class Lysosome(GameObject):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.checkCaspaseRole()

    def _initialize_simulation(self):
        world = Container("cell")
        caspase11 = Caspase("caspase-11", active=True)
        phagosome = Phagosome("phagosome")
        lysosome = Lysosome("lysosome")
        
        world.addObject(caspase11)
        world.addObject(phagosome)
        world.addObject(lysosome)
        
        return world

    def checkCaspaseRole(self):
        caspase11 = self.rootObject.containsItemWithName("caspase-11")[0]
        if caspase11.isActive():
            # Simulating the role of caspase-11 in phagosome-lysosome fusion
            # According to the reference text, caspase-11 is dispensable for fusion with nonpathogenic bacteria
            self.result = "Refuted: Active caspase-11 does not regulate phagosome-lysosome fusion with nonpathogenic bacteria."
        else:
            self.result = "Supported: Active caspase-11 regulates phagosome-lysosome fusion."

def main():
    simulation = Simulation()
    print(simulation.result)

if __name__ == "__main__":
    main()
