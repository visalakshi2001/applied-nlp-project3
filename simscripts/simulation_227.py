
# Claim: Cancers that initially benefit from epidermal growth factor receptor targeted therapies later become refractory through several mechanisms.
# The simulation will model cancer cells that initially respond to EGFR-targeted therapies and later develop resistance.

from simulation_utils import GameObject, Container

class CancerCell(GameObject):
    def __init__(self, name, initial_response=True):
        super().__init__(name)
        self.properties = {
            "initial_response": initial_response,
            "resistance_developed": False
        }

    def develop_resistance(self):
        if self.properties["initial_response"]:
            self.properties["resistance_developed"] = True
            self.properties["initial_response"] = False

    def makeDescriptionStr(self):
        response_status = "initially responsive" if self.properties["initial_response"] else "developed resistance"
        return f"A {self.name} that has {response_status} to EGFR-targeted therapies."

class World(Container):
    def __init__(self):
        Container.__init__(self, "cancer_environment")

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
        cancer1 = CancerCell("Lung Cancer Cell")
        cancer2 = CancerCell("Colorectal Cancer Cell")
        world.addObject(cancer1)
        world.addObject(cancer2)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("look", ["look"])
        self.addAction("develop resistance in Lung Cancer Cell", ["develop", self.rootObject.contains[0]])
        self.addAction("develop resistance in Colorectal Cancer Cell", ["develop", self.rootObject.contains[1]])

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "develop":
            action[1].develop_resistance()
            self.observationStr = f"{action[1].name} has developed resistance to EGFR-targeted therapies."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "develop resistance in Lung Cancer Cell", "look", "develop resistance in Colorectal Cancer Cell", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
