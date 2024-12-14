
# Claim: Knockout proximal tubule-specific deletion of the BMP receptor Alk3 causes fibrosis.
# The simulation will model the effects of Alk3 deletion on fibrosis in the kidney.

from simulation_utils import GameObject, Container

class KidneyCell(GameObject):
    def __init__(self, name, alk3_present=True):
        super().__init__(name)
        self.properties = {
            "alk3_present": alk3_present,
            "tgf_beta_signaling": 0,
            "fibrosis": 0
        }

    def tick(self):
        if not self.properties["alk3_present"]:
            self.properties["tgf_beta_signaling"] += 1  # Enhanced TGF-β signaling
            self.properties["fibrosis"] += 1  # Increase in fibrosis

    def makeDescriptionStr(self):
        description = f"A {self.name} cell with Alk3 {'present' if self.properties['alk3_present'] else 'deleted'}. "
        description += f"TGF-β signaling level: {self.properties['tgf_beta_signaling']}, Fibrosis level: {self.properties['fibrosis']}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("kidney")
        healthy_cell = KidneyCell("healthy_kidney_cell", alk3_present=True)
        damaged_cell = KidneyCell("damaged_kidney_cell", alk3_present=False)  # Alk3 deleted
        world.addObject(healthy_cell)
        world.addObject(damaged_cell)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

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
    for _ in range(5):  # Simulate several ticks to observe changes
        obs = simulation.step("look")
        print(obs)
        print()

if __name__ == "__main__":
    main()
