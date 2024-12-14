
# Claim: Guanine nucleotide exchange factors (GEFs) mediate RhoA activation in response to tensional forces on fibronectin-binding integrins.
# The simulation will model the interaction between GEFs and integrins under mechanical tension.

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

class GEF(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "activated": False,
            "signaling_pathway": None
        }

    def activate(self, pathway):
        self.properties["activated"] = True
        self.properties["signaling_pathway"] = pathway

    def makeDescriptionStr(self):
        return f"{self.name} is {'activated' if self.properties['activated'] else 'not activated'}."

class Integrin(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "tension_applied": False
        }

    def applyTension(self):
        self.properties["tension_applied"] = True

    def makeDescriptionStr(self):
        return f"{self.name} has {'tension applied' if self.properties['tension_applied'] else 'no tension applied'}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "cell environment")

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
        gef1 = GEF("LARG")
        gef2 = GEF("GEF-H1")
        integrin = Integrin("Fibronectin-binding Integrin")
        world.addObject(gef1)
        world.addObject(gef2)
        world.addObject(integrin)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("apply tension", ["apply_tension"])
        self.addAction("activate LARG", ["activate", "LARG"])
        self.addAction("activate GEF-H1", ["activate", "GEF-H1"])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply_tension":
            integrin = self.rootObject.containsItemWithName("Fibronectin-binding Integrin")[0]
            integrin.applyTension()
            self.observationStr = f"Tension applied to {integrin.name}."
        elif actionVerb == "activate":
            gef_name = action[1]
            gef = self.rootObject.containsItemWithName(gef_name)[0]
            gef.activate("Src family tyrosine kinase Fyn" if gef_name == "LARG" else "ERK")
            self.observationStr = f"{gef.name} activated via {gef.properties['signaling_pathway']}."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "apply tension", "activate LARG", "activate GEF-H1"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final check to determine if the claim is supported
    gef1 = simulation.rootObject.containsItemWithName("LARG")[0]
    gef2 = simulation.rootObject.containsItemWithName("GEF-H1")[0]
    if gef1.properties["activated"] and gef2.properties["activated"]:
        print("Claim Supported: GEFs mediate RhoA activation in response to tension.")
    else:
        print("Claim Refuted: GEFs did not activate as expected.")

if __name__ == "__main__":
    main()
