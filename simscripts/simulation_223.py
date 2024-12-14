
# Claim: Cancer cells can stimulate the accumulation of intra-tumoural myeloid-derived suppressor cells by promoting granulocyte colony stimulating factor production.

# Base template code
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

class CancerCell(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "GCSF_production": 0
        }

    def produce_GCSF(self):
        self.properties["GCSF_production"] += 1

class MDSC(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "accumulated": 0
        }

    def accumulate(self):
        self.properties["accumulated"] += 1

class Tumor(Container):
    def __init__(self, name):
        super().__init__(name)
        self.cancer_cells = CancerCell("Cancer Cell")
        self.addObject(self.cancer_cells)
        self.mdsc = MDSC("MDSC")
        self.addObject(self.mdsc)

    def tick(self):
        self.cancer_cells.produce_GCSF()
        if self.cancer_cells.properties["GCSF_production"] > 0:
            self.mdsc.accumulate()

class World(Container):
    def __init__(self):
        super().__init__("Tumor Environment")
        self.tumor = Tumor("Tumor")
        self.addObject(self.tumor)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += "\t" + self.tumor.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        return World()

    def run_simulation(self):
        for _ in range(5):  # Simulate for 5 ticks
            self.rootObject.tick()

    def check_claim(self):
        gcsf_production = self.rootObject.tumor.cancer_cells.properties["GCSF_production"]
        mdsc_accumulated = self.rootObject.tumor.mdsc.properties["accumulated"]
        if gcsf_production > 0 and mdsc_accumulated > 0:
            return "Claim Supported: Cancer cells stimulate MDSC accumulation through G-CSF production."
        else:
            return "Claim Refuted: No evidence of MDSC accumulation from cancer cell G-CSF production."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.check_claim()
    print(result)

if __name__ == "__main__":
    main()
