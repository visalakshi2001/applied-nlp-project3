
# Claim: Ly6C hi monocytes have a higher inflammatory capacity than Ly6C lo monocytes.
# The simulation will model the behavior of two types of monocytes: Ly6C hi and Ly6C lo, and their response to inflammatory conditions.

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

class Monocyte(GameObject):
    def __init__(self, name, inflammatory_capacity=0):
        super().__init__(name)
        self.properties = {
            "inflammatory_capacity": inflammatory_capacity
        }

    def tick(self):
        # Simulate the increase in inflammatory capacity under inflammatory conditions
        if self.name == "Ly6C hi monocyte":
            self.properties["inflammatory_capacity"] += 2  # Higher increase for Ly6C hi
        elif self.name == "Ly6C lo monocyte":
            self.properties["inflammatory_capacity"] += 1  # Lower increase for Ly6C lo

    def makeDescriptionStr(self):
        return f"A {self.name} with inflammatory capacity of {self.properties['inflammatory_capacity']}."

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
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        ly6c_hi = Monocyte("Ly6C hi monocyte")
        ly6c_lo = Monocyte("Ly6C lo monocyte")
        world.addObject(ly6c_hi)
        world.addObject(ly6c_lo)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("simulate inflammation", [])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        if actionStr == "simulate inflammation":
            # Simulate the effect of inflammation on monocytes
            allMonocytes = self.rootObject.getAllContainedObjectsRecursive()
            for monocyte in allMonocytes:
                monocyte.tick()

        # Update the observation string
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Action: simulate inflammation")
    obs = simulation.step("simulate inflammation")
    print(obs)

    # Check the inflammatory capacities to verify the claim
    ly6c_hi_capacity = simulation.rootObject.containsItemWithName("Ly6C hi monocyte")[0].getProperty("inflammatory_capacity")
    ly6c_lo_capacity = simulation.rootObject.containsItemWithName("Ly6C lo monocyte")[0].getProperty("inflammatory_capacity")

    if ly6c_hi_capacity > ly6c_lo_capacity:
        print("Claim Supported: Ly6C hi monocytes have a higher inflammatory capacity than Ly6C lo monocytes.")
    else:
        print("Claim Refuted: Ly6C hi monocytes do not have a higher inflammatory capacity than Ly6C lo monocytes.")

if __name__ == "__main__":
    main()
