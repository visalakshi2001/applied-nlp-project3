
# Claim: Most termination events in Okazaki fragments are dictated by initiation patterns.
# The simulation will analyze the relationship between initiation patterns and termination events in Okazaki fragments.

from simulation_utils import GameObject, Container

class OkazakiFragment(GameObject):
    def __init__(self, name, initiation_pattern=0):
        super().__init__(name)
        self.initiation_pattern = initiation_pattern
        self.termination_event = 0

    def tick(self):
        # The termination event is influenced by the initiation pattern
        self.termination_event = self.initiation_pattern * 0.8  # Arbitrary relationship for simulation

    def makeDescriptionStr(self):
        return f"{self.name} with initiation pattern {self.initiation_pattern} has termination event level {self.termination_event}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        fragment1 = OkazakiFragment("Okazaki Fragment 1", initiation_pattern=5)
        fragment2 = OkazakiFragment("Okazaki Fragment 2", initiation_pattern=3)
        world.addObject(fragment1)
        world.addObject(fragment2)        
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
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

if __name__ == "__main__":
    main()
