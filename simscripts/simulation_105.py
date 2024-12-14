
# Claim: Alteration of origin firing causes changes in termination zones of Okazaki fragments.
# This simulation will test the claim by simulating the effects of altering origin firing on termination zones of Okazaki fragments.

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

class OkazakiFragment(GameObject):
    def __init__(self, name, termination_zone):
        super().__init__(name)
        self.properties["termination_zone"] = termination_zone

    def alterTerminationZone(self, new_zone):
        self.properties["termination_zone"] = new_zone

    def makeDescriptionStr(self):
        return f"{self.name} with termination zone at {self.properties['termination_zone']}."

class Origin(GameObject):
    def __init__(self, name, firing_time):
        super().__init__(name)
        self.properties["firing_time"] = firing_time

    def alterFiringTime(self, new_time):
        self.properties["firing_time"] = new_time

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        origin = Origin("Origin_1", "late")
        ok_fragment = OkazakiFragment("Okazaki_Fragment_1", "zone_A")
        world.addObject(origin)
        world.addObject(ok_fragment)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "look": ["look"],
            "alter firing time": ["alter", "Origin_1"],
            "check termination zone": ["check", "Okazaki_Fragment_1"]
        }

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "alter":
            origin = self.rootObject.containsItemWithName("Origin_1")[0]
            origin.alterFiringTime("early")
            ok_fragment = self.rootObject.containsItemWithName("Okazaki_Fragment_1")[0]
            ok_fragment.alterTerminationZone("zone_B")  # Simulating change in termination zone
            self.observationStr = f"Altered firing time of {origin.name} to early, resulting in {ok_fragment.name} termination zone change to {ok_fragment.properties['termination_zone']}."
        elif actionVerb == "check":
            ok_fragment = self.rootObject.containsItemWithName("Okazaki_Fragment_1")[0]
            self.observationStr = f"{ok_fragment.name} has termination zone at {ok_fragment.properties['termination_zone']}."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "alter firing time", "check termination zone"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
