
# Claim: Deregulation of HAND2 is a crucial step in endometrial carcinogenesis in mice.
# The simulation will model the relationship between HAND2 deregulation and endometrial cancer development in mice.

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

class EndometrialCell(GameObject):
    def __init__(self, name, HAND2_methylation=0):
        super().__init__(name)
        self.properties = {
            "HAND2_methylation": HAND2_methylation,
            "is_cancerous": False
        }

    def tick(self):
        # If HAND2 methylation is above a certain threshold, the cell becomes cancerous
        if self.properties["HAND2_methylation"] > 50:  # Arbitrary threshold for simulation
            self.properties["is_cancerous"] = True

    def makeDescriptionStr(self):
        description = f"{self.name} with HAND2 methylation level at {self.properties['HAND2_methylation']}."
        if self.properties["is_cancerous"]:
            description += " This cell is cancerous."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "endometrial environment")

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
        normal_cell = EndometrialCell("Normal Endometrial Cell", HAND2_methylation=20)
        cancerous_cell = EndometrialCell("Cancerous Endometrial Cell", HAND2_methylation=60)
        world.addObject(normal_cell)
        world.addObject(cancerous_cell)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("increase HAND2 methylation of Cancerous Endometrial Cell", ["increase", "Cancerous Endometrial Cell"])
        self.addAction("decrease HAND2 methylation of Normal Endometrial Cell", ["decrease", "Normal Endometrial Cell"])

    def actionIncrease(self, cell):
        if type(cell) != EndometrialCell:
            return f"Cannot increase HAND2 methylation of {cell.name}."
        else:
            cell.properties["HAND2_methylation"] += 10
            return f"You increase the HAND2 methylation of {cell.name} by 10."

    def actionDecrease(self, cell):
        if type(cell) != EndometrialCell:
            return f"Cannot decrease HAND2 methylation of {cell.name}."
        else:
            cell.properties["HAND2_methylation"] -= 10
            return f"You decrease the HAND2 methylation of {cell.name} by 10."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb.startswith("increase"):
            cell_name = action[1]
            cell = self.rootObject.containsItemWithName(cell_name)[0]
            self.observationStr = self.actionIncrease(cell)
        elif actionVerb.startswith("decrease"):
            cell_name = action[1]
            cell = self.rootObject.containsItemWithName(cell_name)[0]
            self.observationStr = self.actionDecrease(cell)

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
    actions = ["look", "increase HAND2 methylation of Cancerous Endometrial Cell", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()

# The simulation will show that increasing HAND2 methylation leads to cancerous cells, supporting the claim.
