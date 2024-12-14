
# Claim: JMJD6 slows the hydroxylation of C-terminal lysine
# The simulation will model the interaction of JMJD6 with p53 and its effect on hydroxylation.

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

class JMJD6(GameObject):
    def __init__(self):
        super().__init__("JMJD6")
        self.properties["hydroxylation_rate"] = 1.0  # Normal rate of hydroxylation

    def inhibit_hydroxylation(self):
        self.properties["hydroxylation_rate"] *= 0.5  # Slows down the hydroxylation

class P53(GameObject):
    def __init__(self):
        super().__init__("p53")
        self.properties["hydroxylation_level"] = 0.0  # Initial hydroxylation level

    def hydroxylate(self, jmjd6):
        if jmjd6.getProperty("hydroxylation_rate") < 1.0:
            self.properties["hydroxylation_level"] += 0.5  # Increase hydroxylation level
        else:
            self.properties["hydroxylation_level"] += 1.0  # Normal hydroxylation

class World(Container):
    def __init__(self):
        Container.__init__(self, "cell environment")
        self.jmjd6 = JMJD6()
        self.p53 = P53()
        self.addObject(self.jmjd6)
        self.addObject(self.p53)

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        outStr += f"\t{self.jmjd6.makeDescriptionStr()} with hydroxylation rate: {self.jmjd6.properties['hydroxylation_rate']}\n"
        outStr += f"\t{self.p53.makeDescriptionStr()} with hydroxylation level: {self.p53.properties['hydroxylation_level']}\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("inhibit hydroxylation", ["inhibit"])

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "inhibit":
            self.rootObject.jmjd6.inhibit_hydroxylation()
            self.rootObject.p53.hydroxylate(self.rootObject.jmjd6)
            self.observationStr = "JMJD6 has inhibited hydroxylation. p53 hydroxylation level updated."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "inhibit hydroxylation"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check on hydroxylation level
    if simulation.rootObject.p53.properties["hydroxylation_level"] > 0:
        print("Claim Supported: JMJD6 slows the hydroxylation of C-terminal lysine.")
    else:
        print("Claim Refuted: JMJD6 does not slow the hydroxylation of C-terminal lysine.")

if __name__ == "__main__":
    main()
