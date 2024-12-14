
# Claim: Increased diastolic blood pressure (DBP) is associated with abdominal aortic aneurysm.
# The simulation will analyze the relationship between diastolic blood pressure and abdominal aortic aneurysm.

from simulation_utils import GameObject, Container

class BloodPressure(GameObject):
    def __init__(self, name, DBP=0):
        super().__init__(name)
        self.properties = {
            "DBP": DBP,  # Diastolic Blood Pressure
            "associated_with_AAA": False  # Association with Abdominal Aortic Aneurysm
        }

    def tick(self):
        # Simulate the effect of DBP on the association with abdominal aortic aneurysm
        if self.properties["DBP"] > 80:  # Assuming a threshold for increased DBP
            self.properties["associated_with_AAA"] = True
        else:
            self.properties["associated_with_AAA"] = False

    def makeDescriptionStr(self):
        description = f"{self.name} has a diastolic blood pressure of {self.properties['DBP']} mm Hg."
        if self.properties["associated_with_AAA"]:
            description += " This is associated with abdominal aortic aneurysm."
        else:
            description += " This is not associated with abdominal aortic aneurysm."
        return description

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
        # Create blood pressure objects with different DBP values
        bp1 = BloodPressure("Patient 1", DBP=85)  # Increased DBP
        bp2 = BloodPressure("Patient 2", DBP=75)  # Normal DBP
        world.addObject(bp1)
        world.addObject(bp2)        
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

        # Call tick to update associations
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

if __name__ == "__main__":
    main()
