
# Claim: Diabetic patients with acute coronary syndrome experience decreased short-term and long-term risk for bleeding events.
# The simulation will analyze the relationship between diabetes and the risk of bleeding events in patients with acute coronary syndrome.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, diabetes=False, bleeding_risk=0):
        super().__init__(name)
        self.properties = {
            "diabetes": diabetes,
            "bleeding_risk": bleeding_risk
        }

    def tick(self):
        # Simulate the effect of diabetes on bleeding risk
        if self.properties["diabetes"]:
            self.properties["bleeding_risk"] = max(0, self.properties["bleeding_risk"] - 1)  # Decrease risk
        else:
            self.properties["bleeding_risk"] += 1  # Increase risk

    def makeDescriptionStr(self):
        description = f"{self.name} (Diabetes: {self.properties['diabetes']}, Bleeding Risk: {self.properties['bleeding_risk']})"
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "hospital environment")

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
        diabetic_patient = Patient("Diabetic Patient", diabetes=True, bleeding_risk=5)
        nondiabetic_patient = Patient("Nondiabetic Patient", diabetes=False, bleeding_risk=5)
        world.addObject(diabetic_patient)
        world.addObject(nondiabetic_patient)        
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

if __name__ == "__main__":
    main()
