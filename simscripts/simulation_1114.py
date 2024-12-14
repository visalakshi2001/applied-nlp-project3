
# Claim: Surfactin producing cells and exopolymer producing cells cooperate to generate "Van Gogh" bundles that have sliding abilities on specialized media.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class Bacteria(GameObject):
    def __init__(self, name, type, friction=0):
        super().__init__(name)
        self.type = type  # Type can be 'surfactin' or 'exopolymer'
        self.friction = friction  # Friction reduction ability

    def tick(self):
        # Simulate the interaction between surfactin and exopolymer producing cells
        if self.type == 'surfactin':
            self.friction = 1  # Surfactin producing cells reduce friction
        elif self.type == 'exopolymer':
            self.friction = 0.5  # Exopolymer producing cells have some friction

class VanGoghBundle(Container):
    def __init__(self):
        super().__init__("Van Gogh Bundle")
        self.properties["isSliding"] = True  # Bundles can slide

    def checkSlidingAbility(self):
        # Check if the bundle can slide based on the friction properties of its components
        total_friction = sum([bacteria.friction for bacteria in self.contains])
        return total_friction < 2  # If total friction is less than 2, it can slide

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
        surfactin_cell = Bacteria("Surfactin Cell", "surfactin")
        exopolymer_cell = Bacteria("Exopolymer Cell", "exopolymer")
        bundle = VanGoghBundle()
        
        # Adding cells to the bundle
        bundle.addObject(surfactin_cell)
        bundle.addObject(exopolymer_cell)
        
        world.addObject(bundle)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("check sliding ability of Van Gogh Bundle", ["check"])

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

        if actionVerb == "check":
            bundle = self.rootObject.contains[0]  # Get the Van Gogh Bundle
            can_slide = bundle.checkSlidingAbility()
            self.observationStr = f"The Van Gogh Bundle can slide: {can_slide}."

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
    actions = ["check sliding ability of Van Gogh Bundle"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
