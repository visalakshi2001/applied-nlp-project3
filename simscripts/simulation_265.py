
# Claim: Clathrin stabilizes the spindle fiber apparatus during mitosis.
# The simulation will model the effect of clathrin on the stability of spindle fibers during mitosis.

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

class Clathrin(GameObject):
    def __init__(self):
        super().__init__("Clathrin")
        self.properties = {
            "stabilizes_spindle": True,
            "is_depleted": False
        }

    def deplete(self):
        self.properties["is_depleted"] = True

class SpindleFiber(GameObject):
    def __init__(self):
        super().__init__("Spindle Fiber")
        self.properties = {
            "is_stable": True
        }

    def destabilize(self):
        self.properties["is_stable"] = False

class MitosisSimulation:
    def __init__(self):
        self.clathrin = Clathrin()
        self.spindle_fiber = SpindleFiber()
        self.mitosis_complete = False

    def perform_mitosis(self):
        if self.clathrin.getProperty("is_depleted"):
            self.spindle_fiber.destabilize()
            self.mitosis_complete = False
        else:
            self.mitosis_complete = True

    def deplete_clathrin(self):
        self.clathrin.deplete()

    def check_results(self):
        if self.mitosis_complete and self.spindle_fiber.getProperty("is_stable"):
            return "Claim Supported: Clathrin stabilizes the spindle fiber apparatus during mitosis."
        else:
            return "Claim Refuted: Clathrin does not stabilize the spindle fiber apparatus during mitosis."

def main():
    simulation = MitosisSimulation()
    
    # Perform mitosis with clathrin present
    simulation.perform_mitosis()
    print(simulation.check_results())  # Should support the claim

    # Now deplete clathrin and perform mitosis again
    simulation.deplete_clathrin()
    simulation.perform_mitosis()
    print(simulation.check_results())  # Should refute the claim

if __name__ == "__main__":
    main()
