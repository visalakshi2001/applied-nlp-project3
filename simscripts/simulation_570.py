
# Claim: In breast cancer, the loss of myoepithelial cells promotes the transition of ductal carcinoma in situ to invasive carcinoma.
# The simulation will model the interaction between myoepithelial cells and the progression of ductal carcinoma in situ (DCIS) to invasive carcinoma.

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

class MyoepithelialCell(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "isNormal": True,
            "inhibitsInvasion": True
        }

class Fibroblast(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "promotesInvasion": True
        }

class DuctalCarcinomaInSitu(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "isInvasive": False
        }

    def transitionToInvasive(self):
        if not self.properties["isInvasive"]:
            self.properties["isInvasive"] = True
            return True
        return False

class World(Container):
    def __init__(self):
        Container.__init__(self, "breast_cancer_environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        myoepithelial_cell = MyoepithelialCell("normal_myoepithelial_cell")
        fibroblast = Fibroblast("fibroblast")
        dcis = DuctalCarcinomaInSitu("ductal_carcinoma_in_situ")

        world.addObject(myoepithelial_cell)
        world.addObject(fibroblast)
        world.addObject(dcis)

        return world

    def run_simulation(self):
        myoepithelial_cell = self.rootObject.containsItemWithName("normal_myoepithelial_cell")[0]
        dcis = self.rootObject.containsItemWithName("ductal_carcinoma_in_situ")[0]

        # Simulate the loss of myoepithelial cells
        myoepithelial_cell.properties["isNormal"] = False
        myoepithelial_cell.properties["inhibitsInvasion"] = False

        # Check if DCIS transitions to invasive carcinoma
        if not myoepithelial_cell.properties["isNormal"]:
            transition_result = dcis.transitionToInvasive()
            if transition_result:
                return "Claim Supported: Loss of myoepithelial cells promotes transition to invasive carcinoma."
            else:
                return "Claim Refuted: Loss of myoepithelial cells does not promote transition to invasive carcinoma."
        return "Claim Refuted: Myoepithelial cells are still present."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.result)

if __name__ == "__main__":
    main()
