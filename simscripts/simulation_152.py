
# Claim: B cells go through plasmablast differentiation and antibody production by continuous expression of EBI2.

from simulation_utils import GameObject, Container

class BCell(GameObject):
    def __init__(self, name, ebi2_expression=0, plasmablast_differentiation=False):
        super().__init__(name)
        self.properties = {
            "ebi2_expression": ebi2_expression,
            "plasmablast_differentiation": plasmablast_differentiation
        }

    def tick(self):
        # If EBI2 is continuously expressed, B cells differentiate into plasmablasts
        if self.properties["ebi2_expression"] > 0:
            self.properties["plasmablast_differentiation"] = True

    def makeDescriptionStr(self):
        description = f"A B cell named {self.name}, EBI2 expression level is {self.properties['ebi2_expression']}, "
        description += f"and plasmablast differentiation status is {'Yes' if self.properties['plasmablast_differentiation'] else 'No'}."
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        b_cell = BCell("BCell_1", ebi2_expression=1)  # EBI2 is expressed
        world.addObject(b_cell)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"increase EBI2 expression of {objReferent}", ["increase", obj])

    def actionIncrease(self, b_cell):
        if type(b_cell) != BCell:
            return f"Cannot increase the EBI2 expression of {b_cell.name}."
        else:
            b_cell.properties["ebi2_expression"] += 1
            return f"You increase the EBI2 expression of {b_cell.name} by 1."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb.startswith("increase"):
            self.observationStr = self.actionIncrease(action[1])

        self.doWorldTick()
        self.generatePossibleActions()
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

    # Check if the claim is supported or refuted
    b_cell = simulation.rootObject.contains[0]  # Get the B cell
    if b_cell.properties["plasmablast_differentiation"]:
        print("Claim Supported: B cells go through plasmablast differentiation by continuous expression of EBI2.")
    else:
        print("Claim Refuted: B cells do not go through plasmablast differentiation.")

if __name__ == "__main__":
    main()
