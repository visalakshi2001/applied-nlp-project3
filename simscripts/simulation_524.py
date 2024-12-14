
# Claim: Higher plasma levels of I-carnitine, when associated with trimethylamine N-oxide, are positively correlated with cardiovascular events in humans.
# The simulation will model the relationship between L-carnitine, TMAO, and cardiovascular events.

from simulation_utils import GameObject, Container

class Carnitine(GameObject):
    def __init__(self, name, plasma_level=0):
        super().__init__(name)
        self.plasma_level = plasma_level  # Plasma level of L-carnitine

class TMAO(GameObject):
    def __init__(self, name, concentration=0):
        super().__init__(name)
        self.concentration = concentration  # Concentration of TMAO

class CardiovascularEvent(GameObject):
    def __init__(self, name, risk_factor=0):
        super().__init__(name)
        self.risk_factor = risk_factor  # Risk factor for cardiovascular events

class Human(GameObject):
    def __init__(self, name, carnitine, tmao):
        super().__init__(name)
        self.carnitine = carnitine
        self.tmao = tmao
        self.cardiovascular_event = CardiovascularEvent("Cardiovascular Event")

    def assess_risk(self):
        # Risk is higher if both plasma levels of L-carnitine and TMAO concentration are high
        if self.carnitine.plasma_level > 5 and self.tmao.concentration > 5:
            self.cardiovascular_event.risk_factor = 1  # High risk
        else:
            self.cardiovascular_event.risk_factor = 0  # Low risk

    def makeDescriptionStr(self):
        return f"{self.name} has plasma L-carnitine level of {self.carnitine.plasma_level} and TMAO concentration of {self.tmao.concentration}. Risk factor for cardiovascular events: {self.cardiovascular_event.risk_factor}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

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
        carnitine = Carnitine("L-carnitine", plasma_level=6)  # High plasma level
        tmao = TMAO("TMAO", concentration=7)  # High TMAO concentration
        human = Human("Human Subject", carnitine, tmao)
        world.addObject(human)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("assess risk", ["assess"])

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

        if actionVerb == "assess":
            human = self.rootObject.contains[0]  # Get the human object
            human.assess_risk()
            self.observationStr = human.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    action = "assess risk"
    print(f"Action: {action}")
    obs = simulation.step(action)
    print(obs)

if __name__ == "__main__":
    main()
