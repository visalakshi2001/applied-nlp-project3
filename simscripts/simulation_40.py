
# Claim: A diminished ovarian reserve is a very strong indicator of infertility, even in an a priori non-infertile population.
# The simulation will test the relationship between ovarian reserve biomarkers and fertility outcomes.

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

class OvarianReserve(GameObject):
    def __init__(self, name, AMH, FSH):
        super().__init__(name)
        self.properties = {
            "AMH": AMH,  # Antimüllerian hormone level
            "FSH": FSH   # Follicle-stimulating hormone level
        }

class Woman(GameObject):
    def __init__(self, name, AMH, FSH):
        super().__init__(name)
        self.ovarian_reserve = OvarianReserve(name + "_ovarian_reserve", AMH, FSH)
        self.properties["fertility_status"] = None  # Will be determined based on AMH and FSH levels

    def assess_fertility(self):
        if self.ovarian_reserve.properties["AMH"] < 0.7 or self.ovarian_reserve.properties["FSH"] > 10:
            self.properties["fertility_status"] = "low"
        else:
            self.properties["fertility_status"] = "normal"

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
        self.run_assessment()

    def _initialize_simulation(self):
        world = World()
        woman1 = Woman("woman_1", AMH=0.5, FSH=12)  # Diminished ovarian reserve
        woman2 = Woman("woman_2", AMH=1.0, FSH=8)   # Normal ovarian reserve
        world.addObject(woman1)
        world.addObject(woman2)
        return world

    def run_assessment(self):
        for woman in self.rootObject.getAllContainedObjectsRecursive():
            if isinstance(woman, Woman):
                woman.assess_fertility()

    def check_fertility_outcomes(self):
        results = {}
        for woman in self.rootObject.getAllContainedObjectsRecursive():
            if isinstance(woman, Woman):
                results[woman.name] = woman.properties["fertility_status"]
        return results

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    fertility_outcomes = simulation.check_fertility_outcomes()
    print("Fertility Outcomes:")
    for woman, status in fertility_outcomes.items():
        print(f"{woman}: {status}")

    # Determine if the claim is supported or refuted
    if fertility_outcomes["woman_1"] == "low" and fertility_outcomes["woman_2"] == "normal":
        print("Claim Supported: Diminished ovarian reserve is a strong indicator of infertility.")
    else:
        print("Claim Refuted: Diminished ovarian reserve is not a strong indicator of infertility.")

if __name__ == "__main__":
    main()
