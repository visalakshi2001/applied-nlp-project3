
# Claim: COPI coatmer is involved in lipid homeostasis.
# The simulation will model the interaction between COPI components and lipid droplets to verify the claim.

from simulation_utils import GameObject, Container

class LipidDroplet(GameObject):
    def __init__(self, name, lipid_storage=0):
        super().__init__(name)
        self.lipid_storage = lipid_storage
        self.properties = {
            "lipid_storage": lipid_storage,
            "is_regulated": False
        }

    def regulate_lipids(self, copI_active):
        if copI_active:
            self.lipid_storage -= 1  # COPI promotes lipolysis
            self.properties["is_regulated"] = True
        else:
            self.lipid_storage += 1  # Without COPI, lipids accumulate
            self.properties["is_regulated"] = False

    def makeDescriptionStr(self):
        return f"A {self.name} with lipid storage level at {self.lipid_storage}."

class COPIComplex(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def makeDescriptionStr(self):
        return f"A {self.name} that is {'active' if self.active else 'inactive'}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "lipid homeostasis environment")

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
        lipid_droplet = LipidDroplet("lipid droplet")
        copI_complex = COPIComplex("COPI complex")
        world.addObject(lipid_droplet)
        world.addObject(copI_complex)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}

        self.addAction("look", ["look"])
        self.addAction("activate COPI", ["activate", allObjects["COPI complex"][0]])
        self.addAction("deactivate COPI", ["deactivate", allObjects["COPI complex"][0]])

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "activate":
            action[1].activate()
            self.rootObject.contains[0].regulate_lipids(action[1].active)
            self.observationStr = f"{action[1].name} is now active."
        elif actionVerb == "deactivate":
            action[1].deactivate()
            self.rootObject.contains[0].regulate_lipids(action[1].active)
            self.observationStr = f"{action[1].name} is now inactive."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "activate COPI", "look", "deactivate COPI", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
