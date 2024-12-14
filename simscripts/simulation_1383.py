
# Claim: aPKCz causes tumour suppression by affecting glutamine metabolism.
# The simulation will model the relationship between PKCζ levels and tumorigenesis, focusing on glutamine metabolism.

from simulation_utils import GameObject, Container

class TumorCell(GameObject):
    def __init__(self, name, pkc_level=1, glutamine_utilization=0):
        super().__init__(name)
        self.properties = {
            "pkc_level": pkc_level,  # 1 means normal, 0 means deficient
            "glutamine_utilization": glutamine_utilization  # Amount of glutamine utilized
        }

    def tick(self):
        # If PKCζ is deficient, increase glutamine utilization
        if self.properties["pkc_level"] == 0:
            self.properties["glutamine_utilization"] += 2  # Arbitrary increase for simulation

class PKCz(GameObject):
    def __init__(self, name, level=1):
        super().__init__(name)
        self.properties = {
            "level": level  # 1 means present, 0 means absent
        }

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        pkc = PKCz("PKCζ", level=0)  # Simulating PKCζ deficiency
        tumor_cell = TumorCell("TumorCell_1", pkc_level=pkc.properties["level"])
        world.addObject(pkc)
        world.addObject(tumor_cell)
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
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the glutamine utilization to determine if the claim is supported or refuted
    tumor_cell = simulation.rootObject.containsItemWithName("TumorCell_1")[0]
    if tumor_cell.properties["glutamine_utilization"] > 0:
        print("Claim Supported: aPKCz deficiency leads to increased glutamine metabolism, supporting tumorigenesis.")
    else:
        print("Claim Refuted: aPKCz does not affect glutamine metabolism.")

if __name__ == "__main__":
    main()
