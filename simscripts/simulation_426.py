
# Claim: Forkhead 0 (fox0) transcription factors are involved in apoptosis.
# The simulation will demonstrate the involvement of Forkhead O (FoxO) transcription factors in apoptosis.

from simulation_utils import GameObject, Container

class ForkheadO(GameObject):
    def __init__(self, name, apoptosis_effect=0):
        super().__init__(name)
        self.apoptosis_effect = apoptosis_effect

    def induce_apoptosis(self):
        # Simulate the effect of Forkhead O on apoptosis
        self.apoptosis_effect += 1

    def makeDescriptionStr(self):
        return f"{self.name} has an apoptosis effect level of {self.apoptosis_effect}."

class Cell(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.forkheadO = ForkheadO("Forkhead O")

    def undergo_apoptosis(self):
        self.forkheadO.induce_apoptosis()

    def makeDescriptionStr(self):
        return f"{self.name} contains {self.forkheadO.makeDescriptionStr()}"

class World(Container):
    def __init__(self):
        super().__init__("cell environment")

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
        cell = Cell("Cell 1")
        world.addObject(cell)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("induce apoptosis", ["induce apoptosis"])

    def actionInduceApoptosis(self, cell):
        cell.undergo_apoptosis()
        return f"Apoptosis induced in {cell.name}."

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "induce apoptosis":
            self.observationStr = self.actionInduceApoptosis(self.rootObject.contains[0])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["induce apoptosis"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()
        print(simulation.rootObject.makeDescriptionStr())

if __name__ == "__main__":
    main()
