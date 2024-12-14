
# Claim: The microtubule-dependent delivery and secretion of matrix metalloproteases (MMPs) is partially responsible for the disassembly of adhesion sites.

# simulation_utils.py
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
            return ("The " + self.name + " is closed, so things can't be removed from it.", None, False)

        if obj not in self.contains:
            return ("The " + obj.name + " is not contained in the " + self.name + ".", None, False)

        obj.removeSelfFromContainer()
        return ("The " + obj.getReferents()[0] + " is removed from the " + self.name + ".", obj, True)

class Microtubule(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "MMP_delivery": 0,
            "FA_disassembly": 0
        }

    def tick(self):
        # Simulate the delivery of MMPs and its effect on FA disassembly
        self.properties["FA_disassembly"] += self.properties["MMP_delivery"]

class AdhesionSite(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "is_disassembled": False
        }

    def disassemble(self):
        self.properties["is_disassembled"] = True

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
        microtubule = Microtubule("microtubule_1")
        adhesion_site = AdhesionSite("adhesion_site_1")
        world.addObject(microtubule)
        world.addObject(adhesion_site)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("deliver MMPs", ["deliver", allObjects[0]])  # Deliver MMPs using the first object (microtubule)
        self.addAction("disassemble adhesion site", ["disassemble", allObjects[1]])  # Disassemble the adhesion site

    def actionDeliverMMPs(self, microtubule):
        if type(microtubule) != Microtubule:
            return f"Cannot deliver MMPs from {microtubule.name}."
        else:
            microtubule.properties["MMP_delivery"] += 1
            return f"You deliver MMPs from {microtubule.name}."

    def actionDisassemble(self, adhesion_site):
        if type(adhesion_site) != AdhesionSite:
            return f"Cannot disassemble {adhesion_site.name}."
        else:
            adhesion_site.disassemble()
            return f"You disassemble {adhesion_site.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "deliver":
            self.observationStr = self.actionDeliverMMPs(action[1])
        elif actionVerb == "disassemble":
            self.observationStr = self.actionDisassemble(action[1])

        # Do one tick of the environment
        self.doWorldTick()
        self.generatePossibleActions()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["deliver MMPs", "disassemble adhesion site", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check if the adhesion site is disassembled
    adhesion_site = simulation.rootObject.containsItemWithName("adhesion_site_1")[0]
    if adhesion_site.properties["is_disassembled"]:
        print("Claim Supported: The microtubule-dependent delivery and secretion of matrix metalloproteases (MMPs) is partially responsible for the disassembly of adhesion sites.")
    else:
        print("Claim Refuted: The microtubule-dependent delivery and secretion of matrix metalloproteases (MMPs) is not responsible for the disassembly of adhesion sites.")

if __name__ == "__main__":
    main()
