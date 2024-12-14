
# Claim: Neutrophils produce IL-1β in response to large particles.
# The simulation will model neutrophils and their response to different sizes of microbes.

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

class Neutrophil(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "IL-1β": 0,
            "response": ""
        }

    def respond_to_microbe(self, size):
        if size == "large":
            self.properties["IL-1β"] += 1
            self.properties["response"] = "IL-1β produced in response to large particles."
        else:
            self.properties["response"] = "No IL-1β produced."

    def makeDescriptionStr(self):
        return f"A {self.name} with IL-1β level: {self.properties['IL-1β']} and response: {self.properties['response']}."

class Microbe(GameObject):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

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
        self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        neutrophil = Neutrophil("neutrophil_1")
        large_microbe = Microbe("large_microbe", "large")
        small_microbe = Microbe("small_microbe", "small")
        world.addObject(neutrophil)
        world.addObject(large_microbe)
        world.addObject(small_microbe)
        return world

    def run_simulation(self):
        neutrophil = self.rootObject.containsItemWithName("neutrophil_1")[0]
        large_microbe = self.rootObject.containsItemWithName("large_microbe")[0]
        small_microbe = self.rootObject.containsItemWithName("small_microbe")[0]

        # Neutrophil responds to large microbe
        neutrophil.respond_to_microbe(large_microbe.size)
        # Neutrophil responds to small microbe
        neutrophil.respond_to_microbe(small_microbe.size)

    def print_results(self):
        print(self.observationStr)

def main():
    simulation = Simulation()
    simulation.print_results()

if __name__ == "__main__":
    main()
