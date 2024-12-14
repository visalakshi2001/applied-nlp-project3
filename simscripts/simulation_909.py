
# Claim: PKG-la does not have a large impact on expression of pain hypersensitivity in PGK-la knockout mice.
# The simulation will model the impact of PKG-I on pain hypersensitivity in knockout mice.

from simulation_utils import GameObject, Container

class Nociceptor(GameObject):
    def __init__(self, name, pkgi_expression=0):
        super().__init__(name)
        self.pkgi_expression = pkgi_expression  # Represents the level of PKG-I expression

    def tick(self):
        # Simulate the effect of PKG-I expression on pain hypersensitivity
        if self.pkgi_expression > 0:
            self.properties["pain_hypersensitivity"] = self.pkgi_expression * 2  # Arbitrary relationship
        else:
            self.properties["pain_hypersensitivity"] = 0  # No PKG-I means no hypersensitivity

    def makeDescriptionStr(self):
        return f"A nociceptor named {self.name} with PKG-I expression level {self.pkgi_expression}."

class KnockoutMouse(GameObject):
    def __init__(self, name, pkgi_expression=0):
        super().__init__(name)
        self.nociceptor = Nociceptor(name="nociceptor_" + name, pkgi_expression=pkgi_expression)

    def tick(self):
        self.nociceptor.tick()

    def makeDescriptionStr(self):
        return f"A knockout mouse named {self.name} with nociceptor PKG-I expression level {self.nociceptor.pkgi_expression}."

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
        knockout_mouse = KnockoutMouse(name="PGK-la", pkgi_expression=0)  # PKG-I expression is 0 in knockout
        world.addObject(knockout_mouse)
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

    # Check the pain hypersensitivity level
    knockout_mouse = simulation.rootObject.contains[0]
    pain_hypersensitivity = knockout_mouse.nociceptor.properties.get("pain_hypersensitivity", 0)
    if pain_hypersensitivity == 0:
        print("Claim Supported: PKG-la does not have a large impact on expression of pain hypersensitivity in PGK-la knockout mice.")
    else:
        print("Claim Refuted: PKG-la has an impact on expression of pain hypersensitivity in PGK-la knockout mice.")

if __name__ == "__main__":
    main()
