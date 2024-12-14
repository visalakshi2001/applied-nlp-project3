
# Claim: Citrullinated proteins externalized in neutrophil extracellular traps act indirectly to disrupt the inflammatory cycle.

# Importing necessary classes from the base template
from simulation_utils import GameObject, Container

class CitrullinatedProtein(GameObject):
    def __init__(self, name, is_externalized=False):
        super().__init__(name)
        self.properties = {
            "is_externalized": is_externalized,
            "disrupt_inflammatory_cycle": False
        }

    def tick(self):
        # If the protein is externalized, it disrupts the inflammatory cycle
        if self.properties["is_externalized"]:
            self.properties["disrupt_inflammatory_cycle"] = True

    def makeDescriptionStr(self):
        description = f"A {self.name}, which is {'externalized' if self.properties['is_externalized'] else 'not externalized'} and {'disrupts' if self.properties['disrupt_inflammatory_cycle'] else 'does not disrupt'} the inflammatory cycle."
        return description

class Neutrophil(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.contains = []

    def addCitrullinatedProtein(self, protein):
        self.addObject(protein)

class NeutrophilExtracellularTrap(Container):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        neutrophil = Neutrophil("neutrophil_1")
        net = NeutrophilExtracellularTrap("NET_1")
        
        # Create citrullinated proteins
        citrullinated_protein_1 = CitrullinatedProtein("citrullinated_protein_1", is_externalized=True)
        citrullinated_protein_2 = CitrullinatedProtein("citrullinated_protein_2", is_externalized=False)

        # Add proteins to neutrophil and NET
        neutrophil.addCitrullinatedProtein(citrullinated_protein_1)
        net.addObject(citrullinated_protein_2)

        # Add neutrophil and NET to the world
        world.addObject(neutrophil)
        world.addObject(net)

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
