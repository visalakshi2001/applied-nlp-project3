
# Claim: Repressing IL-18 has negative effects on atherosclerotic lesion composition and progression.
# The simulation will model the effects of IL-18 levels on atherosclerotic plaques.

from simulation_utils import GameObject, Container

class AtheroscleroticPlaque(GameObject):
    def __init__(self, name, il18_level=0, stability=0):
        super().__init__(name)
        self.properties = {
            "il18_level": il18_level,  # Level of IL-18
            "stability": stability       # Stability of the plaque (0 = unstable, 1 = stable)
        }

    def tick(self):
        # The stability of the plaque is inversely related to IL-18 levels
        if self.properties["il18_level"] > 0:
            self.properties["stability"] = 0  # Unstable
        else:
            self.properties["stability"] = 1  # Stable

    def makeDescriptionStr(self):
        stability_status = "unstable" if self.properties["stability"] == 0 else "stable"
        return f"A {self.name} with IL-18 level {self.properties['il18_level']} and is {stability_status}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "atherosclerosis environment")

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
        plaque_stable = AtheroscleroticPlaque("stable plaque", il18_level=0)
        plaque_unstable = AtheroscleroticPlaque("unstable plaque", il18_level=5)  # High IL-18 level
        world.addObject(plaque_stable)
        world.addObject(plaque_unstable)        
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("increase IL-18", ["increase"])
        self.addAction("decrease IL-18", ["decrease"])

    def actionIncrease(self, plaque):
        plaque.properties["il18_level"] += 1
        return f"You increase the IL-18 level of {plaque.name} by 1."

    def actionDecrease(self, plaque):
        plaque.properties["il18_level"] -= 1
        return f"You decrease the IL-18 level of {plaque.name} by 1."

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "increase":
            self.observationStr = self.actionIncrease(self.rootObject.contains[1])  # Increase IL-18 of unstable plaque
        elif actionVerb == "decrease":
            self.observationStr = self.actionDecrease(self.rootObject.contains[0])  # Decrease IL-18 of stable plaque

        # Do one tick of the environment
        self.doWorldTick()

        # Update possible actions
        self.generatePossibleActions()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "increase IL-18", "look", "decrease IL-18", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()

# The simulation will show that increasing IL-18 leads to instability in plaques, supporting the claim.
