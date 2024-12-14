
# Claim: Higher plasma levels of I-carnitine, when associated with trimethylamine N-oxide, are negatively correlated with cardiovascular events in humans.
# This simulation will model the relationship between L-carnitine, TMAO levels, and cardiovascular events.

from simulation_utils import GameObject, Container

class Carnitine(GameObject):
    def __init__(self, name, plasma_level=0):
        super().__init__(name)
        self.plasma_level = plasma_level  # Plasma level of L-carnitine

class TMAO(GameObject):
    def __init__(self, name, level=0):
        super().__init__(name)
        self.level = level  # Level of TMAO

class CardiovascularEvent(GameObject):
    def __init__(self, name, risk_factor=0):
        super().__init__(name)
        self.risk_factor = risk_factor  # Risk factor for cardiovascular events

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        carnitine = Carnitine("L-carnitine", plasma_level=10)  # Example plasma level
        tmao = TMAO("TMAO", level=15)  # Example TMAO level
        cve = CardiovascularEvent("Cardiovascular Event", risk_factor=0)  # Initial risk factor
        world.addObject(carnitine)
        world.addObject(tmao)
        world.addObject(cve)
        return world

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += f"\t{obj.name} with plasma level {getattr(obj, 'plasma_level', 'N/A')} and TMAO level {getattr(obj, 'level', 'N/A')}.\n"
        return outStr

    def evaluate_risk(self):
        carnitine = self.rootObject.contains[0]  # L-carnitine
        tmao = self.rootObject.contains[1]  # TMAO
        cve = self.rootObject.contains[2]  # Cardiovascular Event

        # Evaluate the risk based on the claim
        if carnitine.plasma_level > 5 and tmao.level > 10:
            cve.risk_factor = 1  # Increased risk
            return "Claim Refuted: Higher plasma levels of L-carnitine and TMAO are associated with increased cardiovascular risk."
        else:
            cve.risk_factor = 0  # Normal risk
            return "Claim Supported: Higher plasma levels of L-carnitine and TMAO are not associated with increased cardiovascular risk."

def main():
    simulation = Simulation()
    print(simulation.makeDescriptionStr())
    result = simulation.evaluate_risk()
    print(result)

if __name__ == "__main__":
    main()
