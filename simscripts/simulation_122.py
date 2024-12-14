
# Claim: Antimicrobial agents are more effective due to the pressure of antimicrobial usage.
# The simulation will model the effect of antimicrobial usage on bacteria and their resistance.

from simulation_utils import GameObject, Container

class Bacteria(GameObject):
    def __init__(self, name, resistance=0, usage_pressure=0):
        super().__init__(name)
        self.properties = {
            "resistance": resistance,  # Resistance level of the bacteria
            "usage_pressure": usage_pressure  # Pressure from antimicrobial usage
        }

    def tick(self):
        # Resistance increases with usage pressure
        self.properties["resistance"] += self.properties["usage_pressure"] * 0.1  # Arbitrary factor for simulation

    def makeDescriptionStr(self):
        description = f"A {self.name}, with resistance level {self.properties['resistance']} and usage pressure {self.properties['usage_pressure']}."
        return description

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
        bacteria1 = Bacteria("bacteria_1", resistance=0, usage_pressure=5)  # Initial pressure from antimicrobial usage
        bacteria2 = Bacteria("bacteria_2", resistance=0, usage_pressure=3)  # Lower pressure
        world.addObject(bacteria1)
        world.addObject(bacteria2)        
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("tick", ["tick"])  # Action to simulate the passage of time

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "tick":
            self.doWorldTick()
            self.observationStr = "Time has passed, and bacteria have adjusted to antimicrobial pressure."

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["look", "tick", "look"]  # Look at the initial state, simulate a tick, then look again

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()

# The simulation will show that as the pressure of antimicrobial usage increases, the resistance of bacteria also increases.
# This supports the claim that antimicrobial agents are more effective due to the pressure of antimicrobial usage.
