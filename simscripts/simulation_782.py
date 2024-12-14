
# Claim: Mice without IFN-γ or its receptor are highly susceptible to EAM induced with α-MyHC/CFA.
# The simulation will model the effects of IFN-γ on the susceptibility of mice to EAM.

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

class Mouse(GameObject):
    def __init__(self, name, ifn_gamma_present=True):
        super().__init__(name)
        self.properties = {
            "ifn_gamma_present": ifn_gamma_present,
            "susceptibility": 0  # 0 means not susceptible, higher means more susceptible
        }

    def tick(self):
        if not self.properties["ifn_gamma_present"]:
            self.properties["susceptibility"] += 10  # Increase susceptibility if IFN-γ is absent

    def makeDescriptionStr(self):
        description = f"A {self.name} with IFN-γ present: {self.properties['ifn_gamma_present']}, susceptibility level: {self.properties['susceptibility']}."
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
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        mouse_with_ifn = Mouse("Mouse with IFN-γ", True)
        mouse_without_ifn = Mouse("Mouse without IFN-γ", False)
        world.addObject(mouse_with_ifn)
        world.addObject(mouse_without_ifn)
        return world

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

        # Do one tick of the environment
        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the susceptibility of the mice
    mouse_without_ifn = simulation.rootObject.containsItemWithName("Mouse without IFN-γ")[0]
    if mouse_without_ifn.properties["susceptibility"] > 0:
        print("Claim Supported: Mice without IFN-γ are highly susceptible to EAM.")
    else:
        print("Claim Refuted: Mice without IFN-γ are not highly susceptible to EAM.")

if __name__ == "__main__":
    main()
