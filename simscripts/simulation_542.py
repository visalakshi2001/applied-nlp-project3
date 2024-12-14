
# Claim: IFI16 impedes STING phosphorylation and translocation, resulting in reduced activation of STING.
# The simulation will test the interaction between IFI16 and STING to verify the claim.

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
        return self.properties.get(propertyName, None)

    def addObject(self, obj):
        obj.removeSelfFromContainer()
        self.contains.append(obj)
        obj.parent = self

    def removeObject(self, obj):
        self.contains.remove(obj)
        obj.parent = None

    def removeSelfFromContainer(self):
        if self.parent is not None:
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
        if not self.getProperty("isOpenable"):
            return ("The " + self.name + " can't be closed.", False)
        if not self.getProperty("isOpen"):
            return ("The " + self.name + " is already closed.", False)
        self.properties["isOpen"] = False
        return ("The " + self.name + " is now closed.", True)

class IFI16(GameObject):
    def __init__(self):
        super().__init__("IFI16")
        self.properties = {
            "STING_phosphorylation": True,
            "STING_translocation": True,
            "activation": True
        }

    def impede_STING(self):
        self.properties["STING_phosphorylation"] = False
        self.properties["STING_translocation"] = False
        self.properties["activation"] = False

class STING(GameObject):
    def __init__(self):
        super().__init__("STING")
        self.properties = {
            "phosphorylation": True,
            "translocation": True,
            "activation": True
        }

class World(Container):
    def __init__(self):
        super().__init__("environment")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def _initialize_simulation(self):
        world = World()
        ifi16 = IFI16()
        sting = STING()
        world.addObject(ifi16)
        world.addObject(sting)
        return world

    def run_simulation(self):
        ifi16 = self.rootObject.containsItemWithName("IFI16")[0]
        sting = self.rootObject.containsItemWithName("STING")[0]

        # Before IFI16 impedes STING
        initial_state = {
            "STING_phosphorylation": sting.getProperty("phosphorylation"),
            "STING_translocation": sting.getProperty("translocation"),
            "activation": sting.getProperty("activation")
        }

        # IFI16 impedes STING
        ifi16.impede_STING()

        # After IFI16 impedes STING
        final_state = {
            "STING_phosphorylation": sting.getProperty("phosphorylation"),
            "STING_translocation": sting.getProperty("translocation"),
            "activation": sting.getProperty("activation")
        }

        # Check if the claim is supported or refuted
        if (initial_state["STING_phosphorylation"] and initial_state["STING_translocation"] and initial_state["activation"]) and \
           (not final_state["STING_phosphorylation"] and not final_state["STING_translocation"] and not final_state["activation"]):
            self.result = "Supported"
        else:
            self.result = "Refuted"

def main():
    simulation = Simulation()
    print(f"Claim Verification Result: {simulation.result}")

if __name__ == "__main__":
    main()
