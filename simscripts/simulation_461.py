
# Claim: Genetic deletion of JAM-A increases gut permeability.
# This simulation will test the claim by simulating the effects of JAM-A deletion on gut permeability.

from simulation_utils import GameObject, Container

class GutBarrier(GameObject):
    def __init__(self, name, permeability=0):
        super().__init__(name)
        self.permeability = permeability  # Represents gut permeability

    def tick(self):
        # If JAM-A is deleted, increase permeability
        if self.name == "JAM-A Deletion":
            self.permeability += 1  # Increase permeability due to JAM-A deletion

    def makeDescriptionStr(self):
        return f"The gut barrier '{self.name}' has a permeability level of {self.permeability}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        gut_barrier = GutBarrier("JAM-A Deletion")
        world.addObject(gut_barrier)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

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

    # Check permeability level to determine if the claim is supported or refuted
    gut_barrier = simulation.rootObject.contains[0]  # Access the gut barrier object
    if gut_barrier.permeability > 0:
        print("Claim Supported: Genetic deletion of JAM-A increases gut permeability.")
    else:
        print("Claim Refuted: Genetic deletion of JAM-A does not increase gut permeability.")

if __name__ == "__main__":
    main()
