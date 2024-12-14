
# Claim: Normal granulomas form in the presence of TNF in Zebrafish.
# The simulation will test the effect of TNF presence on granuloma formation in zebrafish.

from simulation_utils import GameObject, Container

class Granuloma(GameObject):
    def __init__(self, name, tnf_present=True):
        super().__init__(name)
        self.tnf_present = tnf_present
        self.granuloma_integrity = True  # True means the granuloma is intact

    def tick(self):
        if not self.tnf_present:
            self.granuloma_integrity = False  # Granuloma breaks down without TNF

    def makeDescriptionStr(self):
        integrity_status = "intact" if self.granuloma_integrity else "broken down"
        return f"A granuloma named {self.name} is currently {integrity_status}."

class Bacteria(GameObject):
    def __init__(self, name):
        super().__init__(name)

class Zebrafish(Container):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        zebrafish = Zebrafish("zebrafish_1")
        bacteria = Bacteria("mycobacterium")
        granuloma_with_tnf = Granuloma("granuloma_with_tnf", tnf_present=True)
        granuloma_without_tnf = Granuloma("granuloma_without_tnf", tnf_present=False)

        zebrafish.addObject(bacteria)
        zebrafish.addObject(granuloma_with_tnf)
        zebrafish.addObject(granuloma_without_tnf)

        return zebrafish

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

    # Check the integrity of granulomas to determine claim support
    granulomas = simulation.rootObject.containsItemWithName("granuloma_with_tnf") + simulation.rootObject.containsItemWithName("granuloma_without_tnf")
    tnf_present_integrity = granulomas[0].granuloma_integrity
    tnf_absent_integrity = granulomas[1].granuloma_integrity

    if tnf_present_integrity and not tnf_absent_integrity:
        print("Claim Supported: Normal granulomas form in the presence of TNF in Zebrafish.")
    else:
        print("Claim Refuted: Normal granulomas do not form in the presence of TNF in Zebrafish.")

if __name__ == "__main__":
    main()
