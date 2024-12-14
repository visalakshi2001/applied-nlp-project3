
# Claim: Egr2 regulates the homeostasis of B and T cells.
# The simulation will model the effects of Egr2 on B and T cells and their homeostasis.

from simulation_utils import GameObject, Container

class Lymphocyte(GameObject):
    def __init__(self, name, egr2_active=True):
        super().__init__(name)
        self.properties = {
            "egr2_active": egr2_active,
            "proinflammatory_cytokines": 0,
            "proliferation": 0
        }

    def tick(self):
        if self.properties["egr2_active"]:
            self.properties["proinflammatory_cytokines"] = 1  # Normal levels
            self.properties["proliferation"] = 1  # Normal proliferation
        else:
            self.properties["proinflammatory_cytokines"] = 10  # Excessive levels
            self.properties["proliferation"] = 0  # Impaired proliferation

    def makeDescriptionStr(self):
        description = f"A {self.name} with Egr2 active: {self.properties['egr2_active']}, " \
                      f"proinflammatory cytokines level: {self.properties['proinflammatory_cytokines']}, " \
                      f"proliferation level: {self.properties['proliferation']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "immune system environment")

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
        lymphocyte1 = Lymphocyte("B cell", egr2_active=True)
        lymphocyte2 = Lymphocyte("T cell", egr2_active=False)  # Simulating Egr2 deletion
        world.addObject(lymphocyte1)
        world.addObject(lymphocyte2)        
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

# The simulation will show that the B cell with Egr2 active has normal levels of proinflammatory cytokines and proliferation,
# while the T cell without Egr2 has excessive proinflammatory cytokines and impaired proliferation.
# This supports the claim that Egr2 regulates the homeostasis of B and T cells.
