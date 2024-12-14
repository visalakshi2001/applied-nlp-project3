
# Claim: Ca2+ cycling is a UCP1-dependent thermogenic mechanism.
# The simulation will test the relationship between Ca2+ cycling and UCP1 in thermogenesis.

from simulation_utils import GameObject, Container

class ThermogenicMechanism(GameObject):
    def __init__(self, name, ucp1_dependent=False, ca2_cycling_active=False):
        super().__init__(name)
        self.properties = {
            "ucp1_dependent": ucp1_dependent,
            "ca2_cycling_active": ca2_cycling_active
        }

    def tick(self):
        # Simulate the thermogenic mechanism
        if self.properties["ucp1_dependent"]:
            self.properties["ca2_cycling_active"] = True
        else:
            self.properties["ca2_cycling_active"] = False

    def makeDescriptionStr(self):
        description = f"{self.name} - UCP1 dependent: {self.properties['ucp1_dependent']}, Ca2+ cycling active: {self.properties['ca2_cycling_active']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "thermogenic environment")

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
        ucp1_mechanism = ThermogenicMechanism("UCP1 Mechanism", ucp1_dependent=True)
        ca2_mechanism = ThermogenicMechanism("Ca2+ Cycling Mechanism", ucp1_dependent=False)
        world.addObject(ucp1_mechanism)
        world.addObject(ca2_mechanism)        
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

    # Check the properties to determine if the claim is supported or refuted
    ucp1_mechanism = simulation.rootObject.contains[0]
    ca2_mechanism = simulation.rootObject.contains[1]

    if ucp1_mechanism.properties["ca2_cycling_active"] and not ca2_mechanism.properties["ca2_cycling_active"]:
        print("Claim Supported: Ca2+ cycling is a UCP1-dependent thermogenic mechanism.")
    else:
        print("Claim Refuted: Ca2+ cycling is not a UCP1-dependent thermogenic mechanism.")

if __name__ == "__main__":
    main()
