
# Claim: Patients with common epithelial cancers are less likely to have an emergency event as their first hospital admission if they live in resource-deprived areas.
# The simulation will model patients with different socioeconomic statuses and their likelihood of emergency admissions.

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

class Patient(GameObject):
    def __init__(self, name, is_deprived_area, cancer_type):
        super().__init__(name)
        self.properties = {
            "is_deprived_area": is_deprived_area,
            "cancer_type": cancer_type,
            "emergency_admission": self.determine_emergency_admission()
        }

    def determine_emergency_admission(self):
        # Simulate the likelihood of emergency admission based on deprivation and cancer type
        if self.properties["is_deprived_area"]:
            return True  # More likely to have emergency admission
        else:
            return False  # Less likely to have emergency admission

class World(Container):
    def __init__(self):
        super().__init__("hospital environment")

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
        # Create patients with different socioeconomic statuses and cancer types
        patient1 = Patient("Patient A", True, "breast cancer")  # Deprived area
        patient2 = Patient("Patient B", False, "lung cancer")  # Not deprived area
        patient3 = Patient("Patient C", True, "colorectal cancer")  # Deprived area
        patient4 = Patient("Patient D", False, "breast cancer")  # Not deprived area
        
        world.addObject(patient1)
        world.addObject(patient2)
        world.addObject(patient3)
        world.addObject(patient4)
        
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
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

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    # Check the emergency admission status of each patient
    for patient in simulation.rootObject.contains:
        print(f"{patient.name} (Deprived: {patient.getProperty('is_deprived_area')}, Cancer Type: {patient.getProperty('cancer_type')}): Emergency Admission = {patient.properties['emergency_admission']}")

if __name__ == "__main__":
    main()
