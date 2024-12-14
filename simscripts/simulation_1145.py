
# Claim: Taxation of sugar-sweetened beverages reduced the incidence rate of type II diabetes in India.
# The simulation will model the impact of a 20% tax on sugar-sweetened beverages (SSBs) on the incidence of type II diabetes.

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

class SSB(GameObject):
    def __init__(self, name, price, consumption_rate):
        super().__init__(name)
        self.properties = {
            "price": price,
            "consumption_rate": consumption_rate,
            "tax_rate": 0.20,  # 20% tax
            "diabetes_incidence": 100  # baseline incidence
        }

    def applyTax(self):
        self.properties["price"] *= (1 + self.properties["tax_rate"])
        self.properties["consumption_rate"] *= (1 - 0.03)  # 3% reduction in consumption due to tax

    def calculateDiabetesIncidence(self):
        # 1.6% reduction in diabetes incidence due to tax
        reduction = self.properties["diabetes_incidence"] * 0.016
        self.properties["diabetes_incidence"] -= reduction
        return self.properties["diabetes_incidence"]

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = Container("India")
        ssb = SSB("Sugar-Sweetened Beverage", price=10, consumption_rate=100)
        world.addObject(ssb)
        return world

    def run(self):
        ssb = self.rootObject.containsItemWithName("Sugar-Sweetened Beverage")[0]
        ssb.applyTax()
        new_diabetes_incidence = ssb.calculateDiabetesIncidence()
        return f"New diabetes incidence after tax: {new_diabetes_incidence}"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.run()
    print(result)

if __name__ == "__main__":
    main()
