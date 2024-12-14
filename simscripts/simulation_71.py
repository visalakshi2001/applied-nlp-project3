
# Claim: Activation of the Rac1 homolog CED-10 kills viable cells in SRGP-1 mutant Caenorhabditis elegans.
# The simulation will model the interaction between CED-10 and SRGP-1 in a simplified environment.

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
        return self.properties.get(propertyName, None)

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent is not None:
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

class Cell(GameObject):
    def __init__(self, name, is_viable=True):
        super().__init__(name)
        self.properties = {
            "is_viable": is_viable,
            "is_cleared": False
        }

    def activateCED10(self):
        if self.properties["is_viable"]:
            self.properties["is_viable"] = False
            return f"{self.name} has been killed by CED-10 activation."
        return f"{self.name} is already non-viable."

class SRGP1(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def regulateEngulfment(self, cell):
        if not cell.properties["is_viable"]:
            cell.properties["is_cleared"] = True
            return f"{cell.name} has been cleared."
        return f"{cell.name} is still viable."

class World(Container):
    def __init__(self):
        super().__init__("environment")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        cell1 = Cell("Cell_1")
        cell2 = Cell("Cell_2", is_viable=False)  # This cell is already non-viable
        srgp1 = SRGP1("SRGP-1")
        world.addObject(cell1)
        world.addObject(cell2)
        world.addObject(srgp1)
        return world

    def step(self):
        # Activate CED-10 on a viable cell
        cell1 = self.rootObject.containsItemWithName("Cell_1")[0]
        activation_result = cell1.activateCED10()

        # SRGP-1 attempts to clear the cells
        srgp1 = self.rootObject.containsItemWithName("SRGP-1")[0]
        clearance_result = srgp1.regulateEngulfment(cell1)
        
        return activation_result, clearance_result

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    activation_result, clearance_result = simulation.step()
    print(activation_result)
    print(clearance_result)

    # Determine if the claim is supported or refuted
    if "killed" in activation_result and "cleared" in clearance_result:
        print("Claim Supported: Activation of CED-10 kills viable cells in SRGP-1 mutant Caenorhabditis elegans.")
    else:
        print("Claim Refuted: Activation of CED-10 does not kill viable cells.")

if __name__ == "__main__":
    main()
