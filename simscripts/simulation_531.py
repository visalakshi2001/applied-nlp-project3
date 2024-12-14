
# Claim: Human embryonic stem cells have the capacity to give rise to differentiated progeny representative of all three embryonic germ layers.

from simulation_utils import GameObject, Container

class StemCell(GameObject):
    def __init__(self, name, undifferentiated=True):
        super().__init__(name)
        self.properties = {
            "undifferentiated": undifferentiated,
            "germ_layers": ["ectoderm", "mesoderm", "endoderm"],
            "differentiated_cells": []
        }

    def differentiate(self):
        if self.properties["undifferentiated"]:
            self.properties["undifferentiated"] = False
            self.properties["differentiated_cells"] = self.properties["germ_layers"]
            return f"{self.name} has differentiated into cells of all three germ layers."
        else:
            return f"{self.name} is already differentiated."

    def makeDescriptionStr(self):
        state = "undifferentiated" if self.properties["undifferentiated"] else "differentiated"
        return f"A {self.name} stem cell, currently {state}, with potential to differentiate into: {', '.join(self.properties['germ_layers'])}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "embryonic_stem_cell_environment")

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
        stem_cell = StemCell("Human Embryonic Stem Cell")
        world.addObject(stem_cell)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        for obj in allObjects:
            if isinstance(obj, StemCell):
                self.addAction(f"differentiate {obj.name}", ["differentiate", obj])

    def actionDifferentiate(self, stem_cell):
        if isinstance(stem_cell, StemCell):
            return stem_cell.differentiate()
        return "Invalid action."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb.startswith("differentiate"):
            self.observationStr = self.actionDifferentiate(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "differentiate Human Embryonic Stem Cell"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
