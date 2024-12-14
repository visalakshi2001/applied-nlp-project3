
# Claim: T cell receptor /CD3 microdomains are required to induce the immunologic synapse.
# The simulation will model T cell receptor (TCR-CD3) triggering and its role in the immunologic synapse.

from simulation_utils import GameObject, Container

class TCellReceptor(GameObject):
    def __init__(self, name, is_triggered=False):
        super().__init__(name)
        self.properties = {
            "is_triggered": is_triggered
        }

    def trigger(self):
        self.properties["is_triggered"] = True

    def reset(self):
        self.properties["is_triggered"] = False

    def makeDescriptionStr(self):
        return f"{self.name} is {'triggered' if self.properties['is_triggered'] else 'not triggered'}."

class ImmunologicSynapse(Container):
    def __init__(self, name):
        super().__init__(name)

    def check_synapse(self, tcr):
        if tcr.getProperty("is_triggered"):
            return "The immunologic synapse is formed."
        else:
            return "The immunologic synapse is not formed."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("T Cell Environment")
        tcr = TCellReceptor("T Cell Receptor")
        synapse = ImmunologicSynapse("Immunologic Synapse")
        world.addObject(tcr)
        world.addObject(synapse)
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
        self.addAction("trigger T Cell Receptor", ["trigger", allObjects["T Cell Receptor"][0]])
        self.addAction("check immunologic synapse", ["check", allObjects["Immunologic Synapse"][0]])

    def actionTrigger(self, tcr):
        tcr.trigger()
        return f"You triggered the {tcr.name}."

    def actionCheckSynapse(self, synapse):
        return synapse.check_synapse(self.makeNameToObjectDict()["T Cell Receptor"][0])

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "trigger":
            self.observationStr = self.actionTrigger(action[1])
        elif actionVerb == "check":
            self.observationStr = self.actionCheckSynapse(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "trigger T Cell Receptor", "check immunologic synapse"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
