
# Claim: Ly49Q directs the organization of neutrophil polarization by regulating membrane raft functions.
# This simulation will test the claim by simulating the effects of Ly49Q on neutrophil polarization and membrane raft functions.

from simulation_utils import GameObject, Container

class Neutrophil(GameObject):
    def __init__(self, name, polarization=0, membrane_raft_function=0):
        super().__init__(name)
        self.properties = {
            "polarization": polarization,
            "membrane_raft_function": membrane_raft_function
        }

    def tick(self):
        # Simulate the effect of Ly49Q on polarization and membrane raft function
        if self.properties["membrane_raft_function"] > 0:
            self.properties["polarization"] += self.properties["membrane_raft_function"] * 2  # Arbitrary multiplier for effect
        else:
            self.properties["polarization"] -= 1  # Decrease polarization if membrane raft function is inhibited

    def makeDescriptionStr(self):
        return f"A {self.name} with polarization level {self.properties['polarization']} and membrane raft function level {self.properties['membrane_raft_function']}."

class Ly49Q(GameObject):
    def __init__(self, name, active=True):
        super().__init__(name)
        self.active = active

    def regulate(self, neutrophil):
        if self.active:
            neutrophil.properties["membrane_raft_function"] = 1  # Activate membrane raft function
        else:
            neutrophil.properties["membrane_raft_function"] = -1  # Inhibit membrane raft function

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
        ly49Q = Ly49Q("Ly49Q")
        world.addObject(neutrophil)
        world.addObject(ly49Q)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "activate Ly49Q": ["activate", True],
            "inactivate Ly49Q": ["activate", False],
            "tick": ["tick"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "activate":
            ly49Q = self.rootObject.contains[1]  # Ly49Q is the second object
            ly49Q.active = action[1]
            self.observationStr = f"{ly49Q.name} is now {'active' if ly49Q.active else 'inactive'}."
        elif actionVerb == "tick":
            neutrophil = self.rootObject.contains[0]  # Neutrophil is the first object
            ly49Q = self.rootObject.contains[1]
            ly49Q.regulate(neutrophil)
            neutrophil.tick()
            self.observationStr = "Tick processed."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    actions = ["activate Ly49Q", "tick", "inactivate Ly49Q", "tick"]
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print(simulation.rootObject.makeDescriptionStr())

if __name__ == "__main__":
    main()
