
# Claim: Active Ly49Q induces neutrophil polarization.
# The simulation will test the claim by simulating the behavior of neutrophils in response to the presence of Ly49Q.

from simulation_utils import GameObject, Container

class Neutrophil(GameObject):
    def __init__(self, name, is_polarized=False):
        super().__init__(name)
        self.is_polarized = is_polarized

    def induce_polarization(self):
        self.is_polarized = True

    def makeDescriptionStr(self):
        return f"A {self.name} that is {'polarized' if self.is_polarized else 'not polarized'}."

class Ly49Q(GameObject):
    def __init__(self, name):
        super().__init__(name)

    def activate(self, neutrophil):
        neutrophil.induce_polarization()

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
        neutrophil = Neutrophil("neutrophil_1")
        ly49q = Ly49Q("Ly49Q")
        world.addObject(neutrophil)
        world.addObject(ly49q)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("activate Ly49Q on neutrophil", ["activate", "neutrophil_1"])

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

        if actionVerb == "activate":
            ly49q = self.rootObject.containsItemWithName("Ly49Q")[0]
            neutrophil = self.rootObject.containsItemWithName(action[1])[0]
            ly49q.activate(neutrophil)
            self.observationStr = f"{ly49q.name} activated on {neutrophil.name}."
        
        self.observationStr += "\n" + self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["activate Ly49Q on neutrophil"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
