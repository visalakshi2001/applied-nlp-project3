
# Claim: MFGE8 regulates fat absorption by binding to av-Beta3 and av-Beta5 integrins.
# The simulation will model the interaction of MFGE8 with integrins and its effect on fat absorption.

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

class Integrin(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties["fat_absorption"] = 0

    def bind_mfge8(self):
        self.properties["fat_absorption"] += 1

class Mfge8(GameObject):
    def __init__(self):
        super().__init__("Mfge8")

    def regulate_fat_absorption(self, integrin):
        integrin.bind_mfge8()

class FatCell(GameObject):
    def __init__(self):
        super().__init__("Fat Cell")
        self.properties["fat_storage"] = 0

    def absorb_fat(self, amount):
        self.properties["fat_storage"] += amount

class World(Container):
    def __init__(self):
        super().__init__("environment")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        mfge8 = Mfge8()
        integrin1 = Integrin("αvβ3 Integrin")
        integrin2 = Integrin("αvβ5 Integrin")
        fat_cell = FatCell()

        world.addObject(mfge8)
        world.addObject(integrin1)
        world.addObject(integrin2)
        world.addObject(fat_cell)

        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "regulate fat absorption with αvβ3": ["regulate", "αvβ3 Integrin"],
            "regulate fat absorption with αvβ5": ["regulate", "αvβ5 Integrin"],
        }

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]
        integrin_name = action[1]

        integrin = next((obj for obj in self.rootObject.contains if obj.name == integrin_name), None)
        mfge8 = next((obj for obj in self.rootObject.contains if obj.name == "Mfge8"), None)
        fat_cell = next((obj for obj in self.rootObject.contains if obj.name == "Fat Cell"), None)

        if actionVerb == "regulate":
            if integrin and mfge8:
                mfge8.regulate_fat_absorption(integrin)
                fat_cell.absorb_fat(integrin.getProperty("fat_absorption"))
                return f"{mfge8.name} regulated fat absorption through {integrin.name}. Fat Cell now stores {fat_cell.properties['fat_storage']} units of fat."
        
        return "ERROR: Unknown action."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["regulate fat absorption with αvβ3", "regulate fat absorption with αvβ5"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
