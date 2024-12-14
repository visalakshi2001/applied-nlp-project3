
# Claim: Helminths interfere with immune system control of coinfections by microbial pathogens.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class Helminth(GameObject):
    def __init__(self, name, resistance_impairment=0):
        super().__init__(name)
        self.resistance_impairment = resistance_impairment

    def tick(self):
        # Simulate the effect of helminth on resistance
        self.resistance_impairment += 1  # Increase impairment over time

class MicrobialPathogen(GameObject):
    def __init__(self, name, bacterial_load=0):
        super().__init__(name)
        self.bacterial_load = bacterial_load

    def tick(self):
        # Simulate the increase in bacterial load due to helminth interference
        self.bacterial_load += 2  # Increase load over time

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        helminth = Helminth("Nippostrongylus brasiliensis")
        pathogen = MicrobialPathogen("Mycobacterium tuberculosis")
        world.addObject(helminth)
        world.addObject(pathogen)
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

    # Check the state of the helminth and microbial pathogen to determine claim support
    helminth = simulation.rootObject.containsItemWithName("Nippostrongylus brasiliensis")[0]
    pathogen = simulation.rootObject.containsItemWithName("Mycobacterium tuberculosis")[0]

    if helminth.resistance_impairment > 0 and pathogen.bacterial_load > 0:
        print("Claim Supported: Helminths interfere with immune system control of coinfections by microbial pathogens.")
    else:
        print("Claim Refuted: Helminths do not interfere with immune system control of coinfections by microbial pathogens.")

if __name__ == "__main__":
    main()
