
# Claim: Transcription factor EB induces transcription of pro-inflammatory cytokines in macrophages infected with Staphylococcus aureus.
# The simulation will model the activation of TFEB in macrophages and its effect on pro-inflammatory cytokines upon S. aureus infection.

from simulation_utils import GameObject, Container

class Macrophage(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.properties = {
            "TFEB_active": False,
            "pro_inflammatory_cytokines": 0
        }

    def activate_TFEB(self):
        self.properties["TFEB_active"] = True
        self.properties["pro_inflammatory_cytokines"] += 5  # Arbitrary increase to represent cytokine production

    def tick(self):
        if self.properties["TFEB_active"]:
            self.properties["pro_inflammatory_cytokines"] += 1  # Continuous production of cytokines

    def makeDescriptionStr(self):
        description = f"A {self.name} with TFEB active: {self.properties['TFEB_active']}, pro-inflammatory cytokines level: {self.properties['pro_inflammatory_cytokines']}."
        return description

class Bacteria(GameObject):
    def __init__(self, name):
        super().__init__(name)

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        macrophage = Macrophage("macrophage_1")
        bacteria = Bacteria("Staphylococcus aureus")
        world.addObject(macrophage)
        world.addObject(bacteria)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        allObjects = self.makeNameToObjectDict()
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("activate TFEB", ["activate", allObjects["macrophage_1"][0]])

    def actionActivateTFEB(self, macrophage):
        if isinstance(macrophage, Macrophage):
            macrophage.activate_TFEB()
            return f"TFEB is activated in {macrophage.name}."
        return "Error: Not a macrophage."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "activate":
            self.observationStr = self.actionActivateTFEB(action[1])

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
    actions = ["activate TFEB", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Final observation to check the cytokine level
    final_obs = simulation.step("look")
    print(final_obs)

if __name__ == "__main__":
    main()
