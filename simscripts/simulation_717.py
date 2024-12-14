
# Claim: Low nucleosome occupancy correlates with high methylation levels across species.
# The simulation will model the relationship between nucleosome occupancy and methylation levels.

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

class Nucleosome(GameObject):
    def __init__(self, name, occupancy):
        super().__init__(name)
        self.properties["occupancy"] = occupancy  # Low occupancy means high value

class Methylation(GameObject):
    def __init__(self, name, level):
        super().__init__(name)
        self.properties["level"] = level  # High level means high value

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
        self.checkCorrelation()

    def _initialize_simulation(self):
        world = World()
        # Create nucleosomes with varying occupancy
        nucleosome1 = Nucleosome("Nucleosome 1", occupancy=0.2)  # Low occupancy
        nucleosome2 = Nucleosome("Nucleosome 2", occupancy=0.8)  # High occupancy
        # Create methylation levels
        methylation1 = Methylation("Methylation 1", level=0.9)  # High methylation
        methylation2 = Methylation("Methylation 2", level=0.3)  # Low methylation
        # Add objects to the world
        world.addObject(nucleosome1)
        world.addObject(nucleosome2)
        world.addObject(methylation1)
        world.addObject(methylation2)
        return world

    def checkCorrelation(self):
        nucleosome_low = self.rootObject.contains[0]  # Nucleosome 1
        nucleosome_high = self.rootObject.contains[1]  # Nucleosome 2
        methylation_high = self.rootObject.contains[2]  # Methylation 1
        methylation_low = self.rootObject.contains[3]  # Methylation 2

        # Check correlation
        if (nucleosome_low.getProperty("occupancy") < 0.5 and methylation_high.getProperty("level") > 0.5) and \
           (nucleosome_high.getProperty("occupancy") > 0.5 and methylation_low.getProperty("level") < 0.5):
            self.result = "Supported"
        else:
            self.result = "Refuted"

    def printResult(self):
        return f"The claim is {self.result}."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.printResult())

if __name__ == "__main__":
    main()
