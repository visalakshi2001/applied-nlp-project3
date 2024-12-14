
# Claim: Klf2 is important for proper myeloid cell function.
# This simulation will test the claim by simulating the role of Klf2 in myeloid cell activation.

from simulation_utils import GameObject, Container

class MyeloidCell(GameObject):
    def __init__(self, name, Klf2_expression=0):
        super().__init__(name)
        self.Klf2_expression = Klf2_expression
        self.properties = {
            "Klf2_expression": Klf2_expression,
            "activation_state": "inactive"
        }

    def activate(self):
        if self.Klf2_expression > 0:
            self.properties["activation_state"] = "active"
        else:
            self.properties["activation_state"] = "inactive"

    def tick(self):
        # Simulate the effect of Klf2 on myeloid cell activation
        self.activate()

    def makeDescriptionStr(self):
        description = f"A {self.name} with Klf2 expression level {self.Klf2_expression}, currently {self.properties['activation_state']}."
        return description

class Klf2(GameObject):
    def __init__(self, name, expression_level=1):
        super().__init__(name)
        self.expression_level = expression_level

    def tick(self):
        # Klf2 acts as a repressor of myeloid cell activation
        if self.expression_level > 0:
            return "Klf2 is active, repressing myeloid cell activation."
        else:
            return "Klf2 is inactive, allowing myeloid cell activation."

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
        myeloid_cell = MyeloidCell("myeloid_cell_1", Klf2_expression=1)  # Klf2 is expressed
        klf2 = Klf2("Klf2", expression_level=1)  # Klf2 is active
        world.addObject(myeloid_cell)
        world.addObject(klf2)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("decrease Klf2 expression", ["decrease", "Klf2"])
        self.addAction("increase Klf2 expression", ["increase", "Klf2"])

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
        elif actionVerb == "decrease":
            if action[1] == "Klf2":
                self.rootObject.contains[1].expression_level -= 1  # Decrease Klf2 expression
                self.observationStr = "Decreased Klf2 expression."
        elif actionVerb == "increase":
            if action[1] == "Klf2":
                self.rootObject.contains[1].expression_level += 1  # Increase Klf2 expression
                self.observationStr = "Increased Klf2 expression."

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
    actions = ["look", "decrease Klf2 expression", "look", "increase Klf2 expression", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
