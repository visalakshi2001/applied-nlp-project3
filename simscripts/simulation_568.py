
# Claim: In a naive state, blocking Wingless-Int-1 secretion from mouse embryonic stem cells inhibits self-renewal of the mouse embryonic stem cells.
# The simulation will model the effects of Wnt signaling on the self-renewal of mouse embryonic stem cells (ESCs).

from simulation_utils import GameObject, Container

class EmbryonicStemCell(GameObject):
    def __init__(self, name, wnt_signaling=1, self_renewal=1):
        super().__init__(name)
        self.properties = {
            "wnt_signaling": wnt_signaling,  # 1 means Wnt signaling is active, 0 means blocked
            "self_renewal": self_renewal       # 1 means self-renewal is occurring, 0 means it is inhibited
        }

    def tick(self):
        # If Wnt signaling is blocked, self-renewal is inhibited
        if self.properties["wnt_signaling"] == 0:
            self.properties["self_renewal"] = 0
        else:
            self.properties["self_renewal"] = 1

    def makeDescriptionStr(self):
        description = f"{self.name}: Wnt signaling is {'active' if self.properties['wnt_signaling'] else 'blocked'}, self-renewal is {'occurring' if self.properties['self_renewal'] else 'inhibited'}."
        return description

class WntSignalContainer(Container):
    def __init__(self):
        super().__init__("Wnt Signal Container")

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = WntSignalContainer()
        esc = EmbryonicStemCell("Mouse Embryonic Stem Cell")
        world.addObject(esc)
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
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"block Wnt signaling of {objReferent}", ["block", obj])
                self.addAction(f"activate Wnt signaling of {objReferent}", ["activate", obj])

    def actionBlock(self, esc):
        if type(esc) != EmbryonicStemCell:
            return f"Cannot block Wnt signaling of {esc.name}."
        else:
            esc.properties["wnt_signaling"] = 0
            return f"You block Wnt signaling of {esc.name}."

    def actionActivate(self, esc):
        if type(esc) != EmbryonicStemCell:
            return f"Cannot activate Wnt signaling of {esc.name}."
        else:
            esc.properties["wnt_signaling"] = 1
            return f"You activate Wnt signaling of {esc.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "block":
            self.observationStr = self.actionBlock(action[1])
        elif actionVerb == "activate":
            self.observationStr = self.actionActivate(action[1])

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
    actions = ["look", "block Wnt signaling of Mouse Embryonic Stem Cell", "look", "activate Wnt signaling of Mouse Embryonic Stem Cell", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
