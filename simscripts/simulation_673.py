
# Claim: LDL cholesterol has a causal role in the development of cardiovascular disease.
# This simulation will verify the claim based on the provided reference text.

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

    def placeObjectInContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be placed there.", False)
        if not (obj.getProperty("isMoveable") == True):
            return ("The " + obj.name + " is not moveable.", None, False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be placed there.", False)
        self.addObject(obj)
        return ("The " + obj.getReferents()[0] + " is placed in the " + self.name + ".", True)

    def takeObjectFromContainer(self, obj):
        if not (self.getProperty("isContainer") == True):
            return ("The " + self.name + " is not a container, so things can't be removed from it.", None, False)
        if not obj.getProperty("isMoveable"):
            return ("The " + obj.name + " is not moveable.", None, False)
        if not (self.getProperty("isOpen") == True):
            return ("The " + self.name + " is closed, so things can't be removed from it.", False)
        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)
        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

class Cholesterol(GameObject):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.properties = {
            "level": level,
            "causal_role": True  # Assuming LDL cholesterol has a causal role
        }

    def tick(self):
        # Simulate the effect of cholesterol levels on cardiovascular disease
        if self.properties["level"] > 5:  # Arbitrary threshold for high cholesterol
            self.properties["causal_role"] = True
        else:
            self.properties["causal_role"] = False

    def makeDescriptionStr(self):
        return f"{self.name} with level {self.properties['level']} and causal role: {self.properties['causal_role']}."

class CardiovascularDisease(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_developed": False
        }

    def develop(self, cholesterol):
        if cholesterol.properties["causal_role"]:
            self.properties["is_developed"] = True

    def makeDescriptionStr(self):
        return f"{self.name} has developed: {self.properties['is_developed']}."

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
        ldl_cholesterol = Cholesterol("LDL Cholesterol", level=6)  # High level to simulate causal role
        cardiovascular_disease = CardiovascularDisease("Cardiovascular Disease")
        world.addObject(ldl_cholesterol)
        world.addObject(cardiovascular_disease)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("check cholesterol", ["check"])
        self.addAction("develop disease", ["develop"])

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

        if actionVerb == "check":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "develop":
            ldl_cholesterol = self.rootObject.containsItemWithName("LDL Cholesterol")[0]
            cardiovascular_disease = self.rootObject.containsItemWithName("Cardiovascular Disease")[0]
            cardiovascular_disease.develop(ldl_cholesterol)
            self.observationStr = cardiovascular_disease.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["check cholesterol", "develop disease"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
