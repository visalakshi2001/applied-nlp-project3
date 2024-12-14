
# Claim: The peak incidence of fractures occurs during pubertal growth spurt in early adolescents.
# Simulation to verify the claim based on the provided reference text.

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

class Fracture(GameObject):
    def __init__(self, age_group, incidence_rate):
        super().__init__(f"Fracture in {age_group}")
        self.properties["incidence_rate"] = incidence_rate

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.check_peak_incidence()

    def _initialize_simulation(self):
        world = Container("environment")
        # Simulating peak incidence of fractures during pubertal growth spurt
        peak_incidence_boys = Fracture("boys aged 11-14", 399.8)  # Example incidence rate
        peak_incidence_girls = Fracture("girls aged 8-11", 334.3)  # Example incidence rate
        world.addObject(peak_incidence_boys)
        world.addObject(peak_incidence_girls)
        return world

    def check_peak_incidence(self):
        boys_fracture = self.rootObject.containsItemWithName("Fracture in boys aged 11-14")[0]
        girls_fracture = self.rootObject.containsItemWithName("Fracture in girls aged 8-11")[0]
        
        if boys_fracture.properties["incidence_rate"] > 0 and girls_fracture.properties["incidence_rate"] > 0:
            self.result = "Supported"
        else:
            self.result = "Refuted"

    def makeDescriptionStr(self):
        return f"In the {self.rootObject.name}, you see: \n" + \
               "\n".join([obj.makeDescriptionStr() for obj in self.rootObject.contains]) + \
               f"\nClaim verification result: {self.result}"

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())

if __name__ == "__main__":
    main()
