
# Claim: YAP/TAZ is required in intestinal regeneration in mouse models of ulcerative colitis.
# This simulation will model the role of YAP/TAZ in intestinal regeneration during ulcerative colitis in a mouse model.

from simulation_utils import GameObject, Container

class YAPTAZ(GameObject):
    def __init__(self, name, activation_level=0):
        super().__init__(name)
        self.activation_level = activation_level
        self.properties = {
            "activation_level": activation_level
        }

    def tick(self):
        # Simulate the activation of YAP/TAZ during regeneration
        self.activation_level += 1  # Increase activation level over time

    def makeDescriptionStr(self):
        return f"{self.name} with activation level: {self.activation_level}"

class IntestinalCell(GameObject):
    def __init__(self, name, state="normal"):
        super().__init__(name)
        self.state = state

    def tick(self, yap_taz):
        # Simulate cell state change based on YAP/TAZ activation
        if yap_taz.activation_level > 0:
            self.state = "regenerating"  # Change state to regenerating if YAP/TAZ is activated
        else:
            self.state = "normal"

    def makeDescriptionStr(self):
        return f"{self.name} is currently in {self.state} state."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("intestinal environment")
        yap_taz = YAPTAZ("YAP/TAZ")
        intestinal_cell = IntestinalCell("Intestinal Cell")
        world.addObject(yap_taz)
        world.addObject(intestinal_cell)
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
        self.addAction("tick", ["tick"])

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

        if actionVerb == "tick":
            # Perform a tick in the simulation
            yap_taz = self.rootObject.contains[0]  # Get YAP/TAZ object
            intestinal_cell = self.rootObject.contains[1]  # Get Intestinal Cell object
            yap_taz.tick()  # Update YAP/TAZ
            intestinal_cell.tick(yap_taz)  # Update Intestinal Cell based on YAP/TAZ activation
            self.observationStr = f"After tick: {yap_taz.makeDescriptionStr()}, {intestinal_cell.makeDescriptionStr()}"

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["tick"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
