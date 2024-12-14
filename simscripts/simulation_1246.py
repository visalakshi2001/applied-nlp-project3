
# Claim: The one-child policy has created a hospitable environment for female infants.
# The simulation will assess the early neonatal mortality rates of boys and girls to determine the impact of the one-child policy.

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

class Infant(GameObject):
    def __init__(self, name, gender, mortality_rate):
        super().__init__(name)
        self.properties = {
            "gender": gender,
            "mortality_rate": mortality_rate
        }

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        # Early neonatal mortality rates per 1000 live births
        boy_mortality_rate = 29
        girl_mortality_rate = 69
        
        # Create infant objects
        boy = Infant("boy_infant", "male", boy_mortality_rate)
        girl = Infant("girl_infant", "female", girl_mortality_rate)
        
        world.addObject(boy)
        world.addObject(girl)
        
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
            self.observationStr += f"\nBoy mortality rate: {self.rootObject.contains[0].properties['mortality_rate']} per 1000 live births."
            self.observationStr += f"\nGirl mortality rate: {self.rootObject.contains[1].properties['mortality_rate']} per 1000 live births."
            if self.rootObject.contains[1].properties['mortality_rate'] > self.rootObject.contains[0].properties['mortality_rate']:
                self.observationStr += "\nThe claim is refuted: The one-child policy has not created a hospitable environment for female infants."
            else:
                self.observationStr += "\nThe claim is supported: The one-child policy has created a hospitable environment for female infants."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.step("look"))

if __name__ == "__main__":
    main()
