
# Claim: TNFAIP3 is a glioblastoma tumor suppressor.
# The simulation will model the effects of TNFAIP3 (A20) on glioblastoma stem cells (GSCs) growth and survival.

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

class GSC(GameObject):
    def __init__(self, name, growth_rate=1, survival_rate=1):
        super().__init__(name)
        self.properties = {
            "growth_rate": growth_rate,
            "survival_rate": survival_rate,
            "A20_expression": 1  # 1 indicates normal expression
        }

    def tick(self):
        # Simulate the effect of A20 expression on growth and survival
        if self.properties["A20_expression"] > 0:
            self.properties["growth_rate"] *= 1.1  # Growth increases with A20
            self.properties["survival_rate"] *= 1.1  # Survival increases with A20
        else:
            self.properties["growth_rate"] *= 0.9  # Growth decreases without A20
            self.properties["survival_rate"] *= 0.9  # Survival decreases without A20

    def makeDescriptionStr(self):
        description = f"{self.name} with growth rate {self.properties['growth_rate']} and survival rate {self.properties['survival_rate']}."
        return description

class A20(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "expression_level": 1  # 1 indicates normal expression
        }

    def knockdown(self):
        self.properties["expression_level"] = 0  # Knockdown A20 expression

    def makeDescriptionStr(self):
        return f"{self.name} with expression level {self.properties['expression_level']}."

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
        gsc = GSC("Glioblastoma Stem Cell")
        a20 = A20("A20 (TNFAIP3)")
        world.addObject(gsc)
        world.addObject(a20)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("knockdown A20", ["knockdown", allObjects[1]])  # Knockdown A20 expression

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "knockdown":
            action[1].knockdown()
            self.observationStr = f"{action[1].name} expression knocked down."

        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "knockdown A20"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
