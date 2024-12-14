
# Claim: Lack of FGF21 in mice slows the rate of atherosclerotic plaque formation.

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

class FGF21(GameObject):
    def __init__(self, name, is_present=True):
        super().__init__(name)
        self.properties = {
            "is_present": is_present,
            "plaque_formation_rate": 0  # 0 means normal rate
        }

    def tick(self):
        if not self.properties["is_present"]:
            self.properties["plaque_formation_rate"] += 1  # Lack of FGF21 increases plaque formation rate

class AtherosclerosisSimulation(Container):
    def __init__(self):
        super().__init__("Atherosclerosis Simulation")
        self.fgf21 = FGF21("FGF21", is_present=False)  # Simulating lack of FGF21
        self.addObject(self.fgf21)

    def makeDescriptionStr(self):
        return f"In the simulation, FGF21 is {'present' if self.fgf21.properties['is_present'] else 'absent'}, leading to a plaque formation rate of {self.fgf21.properties['plaque_formation_rate']}."

class Simulation:
    def __init__(self):
        self.rootObject = AtherosclerosisSimulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_simulation()

    def run_simulation(self):
        for _ in range(5):  # Simulate over 5 ticks
            self.rootObject.tick()
            self.observationStr += f"\nAfter tick: {self.rootObject.fgf21.properties['plaque_formation_rate']}"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    if simulation.rootObject.fgf21.properties['plaque_formation_rate'] > 0:
        print("Claim is Supported: Lack of FGF21 in mice slows the rate of atherosclerotic plaque formation.")
    else:
        print("Claim is Refuted: Lack of FGF21 does not slow the rate of atherosclerotic plaque formation.")

if __name__ == "__main__":
    main()
