
# Claim: Gpr124 increases BBB breakdown in mouse models of ischemic stroke.
# The simulation will model the effects of Gpr124 knockout on BBB integrity in mouse models of ischemic stroke.

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

class MouseModel(GameObject):
    def __init__(self, name, gpr124_status="normal", bbb_integrity=True):
        super().__init__(name)
        self.properties = {
            "gpr124_status": gpr124_status,  # normal or knockout
            "bbb_integrity": bbb_integrity  # True if BBB is intact, False if disrupted
        }

    def tick(self):
        if self.properties["gpr124_status"] == "knockout":
            self.properties["bbb_integrity"] = False  # Gpr124 knockout leads to BBB disruption

    def makeDescriptionStr(self):
        integrity_status = "intact" if self.properties["bbb_integrity"] else "disrupted"
        return f"A mouse model with Gpr124 status '{self.properties['gpr124_status']}' and BBB integrity is {integrity_status}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        normal_mouse = MouseModel("normal_mouse", gpr124_status="normal")
        knockout_mouse = MouseModel("knockout_mouse", gpr124_status="knockout")
        world.addObject(normal_mouse)
        world.addObject(knockout_mouse)
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

    # Check the BBB integrity of the knockout mouse
    knockout_mouse = simulation.rootObject.containsItemWithName("knockout_mouse")[0]
    if not knockout_mouse.properties["bbb_integrity"]:
        print("Claim Supported: Gpr124 increases BBB breakdown in mouse models of ischemic stroke.")
    else:
        print("Claim Refuted: Gpr124 does not increase BBB breakdown in mouse models of ischemic stroke.")

if __name__ == "__main__":
    main()
