
# Claim: Primary cervical cytology screening with HPV detection has higher longitudinal sensitivity to detect severe cervical intraepithelial neoplasia than conventional cytology.
# The simulation will compare the rates of CIN III+ detection between HPV screening and conventional cytology.

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

class ScreeningTest(GameObject):
    def __init__(self, name, CIN_rate):
        super().__init__(name)
        self.properties["CIN_rate"] = CIN_rate  # Rate of detecting CIN III+

    def makeDescriptionStr(self):
        return f"{self.name} with CIN III+ detection rate of {self.properties['CIN_rate']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.compare_results()

    def _initialize_simulation(self):
        world = Container("Cervical Screening Environment")
        hpvscreening = ScreeningTest("HPV Screening", 1.44)  # Based on the relative rate from the reference text
        conventionalcytology = ScreeningTest("Conventional Cytology", 1.0)  # Baseline for comparison
        world.addObject(hpvscreening)
        world.addObject(conventionalcytology)
        return world

    def compare_results(self):
        hpvscreening = self.rootObject.containsItemWithName("HPV Screening")[0]
        conventionalcytology = self.rootObject.containsItemWithName("Conventional Cytology")[0]

        if hpvscreening.getProperty("CIN_rate") > conventionalcytology.getProperty("CIN_rate"):
            self.observationStr += "\nResult: Supported - HPV screening has higher sensitivity."
        else:
            self.observationStr += "\nResult: Refuted - HPV screening does not have higher sensitivity."

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
