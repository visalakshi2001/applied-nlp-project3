
# Claim: The RANK-RANK-Ligand (RANKL) pathway is involved in the development of Aire-expressing medullary thymic epithelial cells (mTECs).

from simulation_utils import GameObject, Container

class ThymicEpithelialCell(GameObject):
    def __init__(self, name, isAireExpressing=False):
        super().__init__(name)
        self.properties = {
            "isAireExpressing": isAireExpressing
        }

    def tick(self):
        # Simulate maturation process
        if not self.properties["isAireExpressing"]:
            self.properties["isAireExpressing"] = True  # Simulate maturation into Aire-expressing mTECs

    def makeDescriptionStr(self):
        return f"{self.name} (Aire-expressing: {self.properties['isAireExpressing']})"

class RANKLSignal(GameObject):
    def __init__(self):
        super().__init__("RANKL Signal")

class RANKLInducerCell(GameObject):
    def __init__(self):
        super().__init__("CD4+3− RANKL+ Inducer Cell")

    def tick(self, mTEC):
        # Simulate the signaling to promote maturation of mTECs
        if isinstance(mTEC, ThymicEpithelialCell) and not mTEC.properties["isAireExpressing"]:
            mTEC.properties["isAireExpressing"] = True  # Induce maturation

class World(Container):
    def __init__(self):
        super().__init__("Thymus Environment")
        self.addObject(RANKLInducerCell())
        self.addObject(RANKLSignal())
        self.addObject(ThymicEpithelialCell("mTEC Progenitor", isAireExpressing=False))

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
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "tick":
            # Simulate the tick of the environment
            for obj in self.rootObject.contains:
                if isinstance(obj, RANKLInducerCell):
                    for mTEC in self.rootObject.contains:
                        if isinstance(mTEC, ThymicEpithelialCell):
                            obj.tick(mTEC)
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the signaling process
    print("Simulating RANKL signaling...")
    print(simulation.step("tick"))

    # Check if the mTEC has matured
    mTEC = simulation.rootObject.contains[2]  # Access the mTEC Progenitor
    if mTEC.properties["isAireExpressing"]:
        result = "Supported"
    else:
        result = "Refuted"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
