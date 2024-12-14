
# Claim: IL-6 signaling plays a major role in atherosclerotic cardiovascular disease.
# The simulation will assess the relationship between IL-6 signaling and coronary heart disease.

from simulation_utils import GameObject, Container

class IL6R(GameObject):
    def __init__(self, name, signaling_effect=0):
        super().__init__(name)
        self.signaling_effect = signaling_effect  # Represents the effect of IL-6 signaling

    def tick(self):
        # Simulate the effect of IL-6 signaling on coronary heart disease risk
        self.signaling_effect += 14.6  # Increase in IL-6 concentration

class CoronaryHeartDisease(GameObject):
    def __init__(self, name, risk_factor=100):
        super().__init__(name)
        self.risk_factor = risk_factor  # Represents the risk factor for coronary heart disease

    def tick(self, il6r):
        # Simulate the effect of IL-6 signaling on coronary heart disease risk
        if il6r.signaling_effect > 0:
            self.risk_factor -= 3.4  # Decrease in risk factor due to IL-6 signaling

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
        il6r = IL6R("IL6R", signaling_effect=0)
        chd = CoronaryHeartDisease("Coronary Heart Disease", risk_factor=100)
        world.addObject(il6r)
        world.addObject(chd)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("simulate IL-6 signaling", ["simulate"])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "simulate":
            il6r = self.rootObject.contains[0]  # Get IL6R object
            chd = self.rootObject.contains[1]    # Get Coronary Heart Disease object
            il6r.tick()  # Simulate IL-6 signaling
            chd.tick(il6r)  # Update coronary heart disease risk based on IL-6 signaling
            self.observationStr = f"IL-6 signaling increased by {il6r.signaling_effect} and coronary heart disease risk is now {chd.risk_factor}."
        
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    action = "simulate IL-6 signaling"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

if __name__ == "__main__":
    main()
