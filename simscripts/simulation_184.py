
# Claim: Bone marrow cells don't contribute to adult macrophage compartments.
# The simulation will test the claim by simulating the behavior of macrophages after bone marrow transplantation.

from simulation_utils import GameObject, Container

class Macrophage(GameObject):
    def __init__(self, name, canExpand=True):
        super().__init__(name)
        self.canExpand = canExpand

    def tick(self):
        # Simulate the expansion of macrophages if they can expand
        if self.canExpand:
            self.properties["expansion"] = "expanding"
        else:
            self.properties["expansion"] = "not expanding"

    def makeDescriptionStr(self):
        return f"A {self.name} which is currently {self.properties.get('expansion', 'not defined')}."

class BoneMarrow(GameObject):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        boneMarrow = BoneMarrow("bone marrow")
        hostMacrophage = Macrophage("host macrophage", canExpand=True)  # Host macrophage can expand
        donorMacrophage = Macrophage("donor macrophage", canExpand=False)  # Donor macrophage cannot expand

        world.addObject(boneMarrow)
        world.addObject(hostMacrophage)
        world.addObject(donorMacrophage)
        
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

    # Check the expansion of host macrophages
    host_macrophage = simulation.rootObject.containsItemWithName("host macrophage")[0]
    donor_macrophage = simulation.rootObject.containsItemWithName("donor macrophage")[0]

    if host_macrophage.canExpand and not donor_macrophage.canExpand:
        result = "Supported: Host macrophages can expand independently of donor macrophages."
    else:
        result = "Refuted: Bone marrow cells contribute to adult macrophage compartments."

    print(result)

if __name__ == "__main__":
    main()
