
# Claim: Radioiodine treatment of non-toxic multinodular goitre increases thyroid volume.
# The simulation will test the claim by modeling the effect of radioiodine treatment on thyroid volume.

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

class Patient(GameObject):
    def __init__(self, name, thyroid_volume):
        super().__init__(name)
        self.properties = {
            "thyroid_volume": thyroid_volume,
            "treatment_effect": 0
        }

    def apply_treatment(self, dose):
        # Simulate the effect of treatment on thyroid volume
        self.properties["treatment_effect"] = dose
        self.properties["thyroid_volume"] -= (self.properties["thyroid_volume"] * 0.6)  # 60% reduction

    def makeDescriptionStr(self):
        return f"{self.name} has a thyroid volume of {self.properties['thyroid_volume']} ml after treatment."

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
        patient = Patient("Patient 1", 73)  # Initial thyroid volume
        world.addObject(patient)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("apply treatment", ["apply treatment"])

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

        if actionVerb == "apply treatment":
            patient = self.rootObject.contains[0]  # Get the patient
            patient.apply_treatment(3.7)  # Apply treatment with a dose
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    result = simulation.step("apply treatment")
    print(result)

    # Check if the thyroid volume has increased or decreased
    final_volume = simulation.rootObject.contains[0].properties["thyroid_volume"]
    if final_volume < 73:  # Initial volume
        print("Claim Refuted: Radioiodine treatment decreases thyroid volume.")
    else:
        print("Claim Supported: Radioiodine treatment increases thyroid volume.")

if __name__ == "__main__":
    main()
