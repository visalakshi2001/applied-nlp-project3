
# Claim: Antimicrobial agents are less effective due to the pressure of antimicrobial usage.
# This simulation will model the effect of antimicrobial usage on bacteria and their resistance.

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
        bacteria1 = Bacteria("bacteria_1", resistance=0, usage_pressure=0)
        bacteria2 = Bacteria("bacteria_2", resistance=0, usage_pressure=0)
        world.addObject(bacteria1)
        world.addObject(bacteria2)        
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])

        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"apply pressure to {objReferent}", ["apply_pressure", obj])

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def actionApplyPressure(self, bacteria):
        if type(bacteria) != Bacteria:
            return f"Cannot apply pressure to {bacteria.name}."
        else:
            bacteria.properties["usage_pressure"] += 1  # Increase pressure
            return f"You apply pressure to {bacteria.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply_pressure":
            self.observationStr = self.actionApplyPressure(action[1])

        self.doWorldTick()
        self.generatePossibleActions()
        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["apply pressure to bacteria_1", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()

# The output of the simulation will show the increase in resistance of bacteria due to the pressure of antimicrobial usage.
# If the resistance increases, it supports the claim that antimicrobial agents are less effective due to the pressure of antimicrobial usage.
