
# Claim: RANK-RANKL pathway signalling is linked to development of Aire-expressing medullary thymic epithelial cells.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class ThymicEpithelialCell(GameObject):
    def __init__(self, name, isAireExpressing=False):
        super().__init__(name)
        self.properties = {
            "isAireExpressing": isAireExpressing
        }

    def tick(self):
        # Simulate the maturation process based on RANKL signaling
        if self.properties["isAireExpressing"]:
            self.properties["isAireExpressing"] = True  # Remain Aire-expressing
        else:
            self.properties["isAireExpressing"] = False  # Not Aire-expressing

    def makeDescriptionStr(self):
        return f"A {self.name} cell, which is {'Aire-expressing' if self.properties['isAireExpressing'] else 'not Aire-expressing'}."

class RANKLSignal(GameObject):
    def __init__(self):
        super().__init__("RANKL Signal")

class RANKLInducerCell(GameObject):
    def __init__(self):
        super().__init__("CD4+3− RANKL+ Inducer Cell")

    def tick(self, mTEC):
        # Simulate the signaling effect on mTECs
        if isinstance(mTEC, ThymicEpithelialCell) and not mTEC.properties["isAireExpressing"]:
            mTEC.properties["isAireExpressing"] = True  # Induce maturation to Aire-expressing

class World(Container):
    def __init__(self):
        super().__init__("Thymus Environment")
        self.addObject(RANKLSignal())
        self.addObject(RANKLInducerCell())
        # Create mTEC progenitors
        self.mTEC_progenitor = ThymicEpithelialCell("mTEC Progenitor", isAireExpressing=False)
        self.addObject(self.mTEC_progenitor)

    def makeDescriptionStr(self):
        outStr = super().makeDescriptionStr()
        outStr += f"\nIn the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = World()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("signal maturation", ["signal maturation"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "signal maturation":
            # Simulate RANKL signaling to induce maturation
            inducer_cell = self.rootObject.contains[1]  # CD4+3− RANKL+ Inducer Cell
            mTEC = self.rootObject.mTEC_progenitor
            inducer_cell.tick(mTEC)  # Signal maturation
            self.observationStr = f"{inducer_cell.name} signals maturation of {mTEC.name}."

        # Update the world state
        self.doWorldTick()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            if isinstance(obj, ThymicEpithelialCell):
                obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "signal maturation"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
