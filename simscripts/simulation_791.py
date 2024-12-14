
# Claim: Migraine with aura is associated with ischemic stroke.
# The simulation will evaluate the association between migraine with aura and ischemic stroke risk.

from simulation_utils import GameObject, Container

class Migraine(GameObject):
    def __init__(self, aura_status, risk_factor):
        super().__init__("Migraine")
        self.aura_status = aura_status  # True if aura is present, False otherwise
        self.risk_factor = risk_factor    # Risk factor for ischemic stroke

    def tick(self):
        # Update risk factor based on aura status
        if self.aura_status:
            self.risk_factor = 2.16  # Increased risk with aura
        else:
            self.risk_factor = 1.23  # Lower risk without aura

    def makeDescriptionStr(self):
        aura = "with aura" if self.aura_status else "without aura"
        return f"A migraine {aura} has a risk factor of {self.risk_factor} for ischemic stroke."

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
        migraine_with_aura = Migraine(aura_status=True, risk_factor=0)
        migraine_without_aura = Migraine(aura_status=False, risk_factor=0)
        world.addObject(migraine_with_aura)
        world.addObject(migraine_without_aura)
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

    # Check the risk factors to determine if the claim is supported or refuted
    migraine_with_aura = simulation.rootObject.contains[0]  # First object is migraine with aura
    migraine_without_aura = simulation.rootObject.contains[1]  # Second object is migraine without aura

    if migraine_with_aura.risk_factor > migraine_without_aura.risk_factor:
        print("Claim Supported: Migraine with aura is associated with ischemic stroke.")
    else:
        print("Claim Refuted: Migraine with aura is not associated with ischemic stroke.")

if __name__ == "__main__":
    main()
