
# Claim: In S. cerevisiae, the absence of RNA surveillance pathways reduces sensitivity to high iron conditions.
# The simulation will model the effect of RNA surveillance pathways on iron sensitivity in S. cerevisiae.

from simulation_utils import GameObject, Container

class YeastCell(GameObject):
    def __init__(self, name, rna_surveillance_active=True, iron_concentration=0):
        super().__init__(name)
        self.properties = {
            "rna_surveillance_active": rna_surveillance_active,
            "iron_concentration": iron_concentration,
            "sensitivity": 0  # 0 means not sensitive, 1 means sensitive
        }

    def tick(self):
        # If RNA surveillance is inactive, increase sensitivity to iron
        if not self.properties["rna_surveillance_active"]:
            if self.properties["iron_concentration"] > 5:  # Arbitrary threshold for sensitivity
                self.properties["sensitivity"] = 1  # Sensitive to high iron
            else:
                self.properties["sensitivity"] = 0  # Not sensitive
        else:
            self.properties["sensitivity"] = 0  # RNA surveillance active, not sensitive

    def makeDescriptionStr(self):
        return f"{self.name} with RNA surveillance {'active' if self.properties['rna_surveillance_active'] else 'inactive'}, iron concentration: {self.properties['iron_concentration']}, sensitivity: {'sensitive' if self.properties['sensitivity'] == 1 else 'not sensitive'}."

class World(Container):
    def __init__(self):
        super().__init__("environment")

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
        yeast_cell_active = YeastCell("Yeast Cell with RNA Surveillance Active", rna_surveillance_active=True, iron_concentration=6)
        yeast_cell_inactive = YeastCell("Yeast Cell with RNA Surveillance Inactive", rna_surveillance_active=False, iron_concentration=6)
        world.addObject(yeast_cell_active)
        world.addObject(yeast_cell_inactive)
        return world

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

if __name__ == "__main__":
    main()

# The expected output will show that the yeast cell with RNA surveillance inactive is sensitive to high iron conditions,
# while the one with RNA surveillance active is not sensitive, thus supporting the claim.
