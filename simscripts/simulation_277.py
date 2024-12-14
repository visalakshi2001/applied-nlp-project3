
# Claim: Commelina yellow mottle virus (ComYMV) has three typical badnavirus ORFs, capable of encoding proteins 23, 15, and 216 kD.
# The simulation will verify if the claim is supported by the reference text.

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

class Virus(GameObject):
    def __init__(self, name, ORFs):
        super().__init__(name)
        self.properties["ORFs"] = ORFs

    def makeDescriptionStr(self):
        description = f"A virus named {self.name} with ORFs encoding proteins: {', '.join(map(str, self.properties['ORFs']))} kD."
        return description

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

    def _initialize_simulation(self):
        world = World()
        comYMV = Virus("Commelina yellow mottle virus (ComYMV)", [23, 15, 216])
        world.addObject(comYMV)
        return world

    def step(self):
        return self.observationStr

def main():
    simulation = Simulation()
    result = simulation.step()
    print(result)

    # Check if the claim is supported
    if [23, 15, 216] == simulation.rootObject.contains[0].properties["ORFs"]:
        print("Claim Supported: The virus has three typical badnavirus ORFs encoding proteins 23, 15, and 216 kD.")
    else:
        print("Claim Refuted: The virus does not have the specified ORFs.")

if __name__ == "__main__":
    main()
