
# Claim: The innate immune response struggles to remove small numbers of parasites.
# This simulation will model the innate immune response and its effectiveness against varying doses of parasites.

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

class Parasite(GameObject):
    def __init__(self, name, dose):
        super().__init__(name)
        self.properties = {
            "dose": dose,
            "removed": False
        }

class ImmuneResponse(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "capacity": 0,
            "successful_removals": 0
        }

    def respond_to_parasite(self, parasite):
        if parasite.getProperty("dose") > self.properties["capacity"]:
            return False  # Unable to remove
        else:
            self.properties["successful_removals"] += 1
            parasite.properties["removed"] = True
            return True  # Successfully removed

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
        immune_response = ImmuneResponse("Innate Immune Response")
        world.addObject(immune_response)

        # Simulating different doses of parasites
        for dose in [1, 5, 10]:  # Small doses
            parasite = Parasite(f"Parasite with dose {dose}", dose)
            immune_response.properties["capacity"] = 5  # Set capacity to 5
            world.addObject(parasite)
            immune_response.respond_to_parasite(parasite)  # Test response

        return world

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"]}

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."
        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Claim Verification:")
    print("The innate immune response struggles to remove small numbers of parasites.")
    print("Results of immune response against parasites with doses 1, 5, and 10:")
    for obj in simulation.rootObject.contains:
        if isinstance(obj, Parasite):
            print(f"{obj.name} removed: {obj.properties['removed']}")

if __name__ == "__main__":
    main()
