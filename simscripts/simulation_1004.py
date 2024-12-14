
# Claim: RANK-RANKL pathway signalling has no known association with development of Aire-expressing medullary thymic epithelial cells.
# The simulation will test the association between RANK-RANKL signaling and the development of Aire-expressing mTECs.

from simulation_utils import GameObject, Container

class ThymicEpithelialCell(GameObject):
    def __init__(self, name, isAireExpressing=False):
        super().__init__(name)
        self.properties = {
            "isAireExpressing": isAireExpressing
        }

    def tick(self):
        # Simulate the maturation process based on RANKL signaling
        if self.getProperty("isAireExpressing"):
            self.properties["isAireExpressing"] = True

class RANKLSignal(GameObject):
    def __init__(self):
        super().__init__("RANKL Signal")

class CD4InducerCell(GameObject):
    def __init__(self):
        super().__init__("CD4+3− Inducer Cell")

    def signal(self, mTEC):
        # If this cell signals, it promotes maturation of mTECs
        if isinstance(mTEC, ThymicEpithelialCell):
            mTEC.properties["isAireExpressing"] = True

class World(Container):
    def __init__(self):
        super().__init__("Thymus Environment")

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
        rankl_signal = RANKLSignal()
        cd4_cell = CD4InducerCell()
        mTEC = ThymicEpithelialCell("mTEC", isAireExpressing=False)

        world.addObject(rankl_signal)
        world.addObject(cd4_cell)
        world.addObject(mTEC)

        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "signal mTEC": ["signal", "mTEC"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "signal":
            # Simulate signaling from CD4+3− Inducer Cell to mTEC
            cd4_cell = self.rootObject.contains[1]  # CD4+3− Inducer Cell
            mTEC = self.rootObject.contains[2]  # mTEC
            cd4_cell.signal(mTEC)

        # Update the observation string
        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate signaling
    print("Action: signal mTEC")
    obs = simulation.step("signal mTEC")
    print(obs)

    # Check if mTEC is Aire-expressing after signaling
    mTEC = simulation.rootObject.contains[2]  # mTEC
    if mTEC.getProperty("isAireExpressing"):
        result = "Refuted: RANK-RANKL pathway signalling is associated with the development of Aire-expressing mTECs."
    else:
        result = "Supported: RANK-RANKL pathway signalling has no known association with development of Aire-expressing mTECs."

    print(result)

if __name__ == "__main__":
    main()
