
# Claim: Activation of PPM1D enhances p53 function.
# The simulation will model the relationship between PPM1D activation and p53 function based on the provided reference text.

from simulation_utils import GameObject, Container

class PPM1D(GameObject):
    def __init__(self, name, activation_level=0):
        super().__init__(name)
        self.activation_level = activation_level  # Level of activation of PPM1D
        self.suppression_of_p53 = 0  # Level of suppression of p53

    def tick(self):
        # The higher the activation level, the more suppression of p53 occurs
        self.suppression_of_p53 = self.activation_level * 2  # Arbitrary multiplier for simulation

    def makeDescriptionStr(self):
        return f"{self.name} with activation level {self.activation_level} suppresses p53 by {self.suppression_of_p53}."

class P53(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.functionality = 100  # Base functionality of p53

    def tick(self, ppm1d):
        # The functionality of p53 decreases with increased suppression
        self.functionality -= ppm1d.suppression_of_p53
        if self.functionality < 0:
            self.functionality = 0  # p53 cannot have negative functionality

    def makeDescriptionStr(self):
        return f"{self.name} has functionality level {self.functionality}."

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
        ppm1d = PPM1D("PPM1D", activation_level=5)  # Simulating activation of PPM1D
        p53 = P53("p53")
        world.addObject(ppm1d)
        world.addObject(p53)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("tick", ["tick"])

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "tick":
            # Perform a tick to update the state of the simulation
            ppm1d = self.rootObject.contains[0]  # PPM1D
            p53 = self.rootObject.contains[1]  # p53
            ppm1d.tick()
            p53.tick(ppm1d)

        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["tick"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Determine if the claim is supported or refuted based on p53 functionality
    p53_functionality = simulation.rootObject.contains[1].functionality
    if p53_functionality < 100:  # If functionality is reduced, claim is supported
        print("Claim Supported: Activation of PPM1D enhances p53 function by suppressing it.")
    else:
        print("Claim Refuted: Activation of PPM1D does not enhance p53 function.")

if __name__ == "__main__":
    main()
