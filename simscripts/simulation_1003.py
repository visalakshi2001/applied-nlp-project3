
# Claim: RAD52 is involved in break-induced DNA replication (BIR).
# The simulation will model the involvement of RAD52 in break-induced replication under DNA replication stress.

from simulation_utils import GameObject, Container

class DNAReplication(GameObject):
    def __init__(self, name, replication_stress=0, RAD52_activity=0):
        super().__init__(name)
        self.properties = {
            "replication_stress": replication_stress,
            "RAD52_activity": RAD52_activity
        }

    def tick(self):
        # Simulate the effect of replication stress on RAD52 activity
        if self.properties["replication_stress"] > 0:
            self.properties["RAD52_activity"] = 1  # RAD52 is activated under stress
        else:
            self.properties["RAD52_activity"] = 0  # RAD52 is inactive without stress

    def makeDescriptionStr(self):
        description = (f"{self.name} with replication stress level {self.properties['replication_stress']} "
                       f"has RAD52 activity level {self.properties['RAD52_activity']}.")
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        replication = DNAReplication("DNA Replication")
        world.addObject(replication)
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
                self.addAction(f"apply replication stress to {objReferent}", ["apply_stress", obj])
                self.addAction(f"remove replication stress from {objReferent}", ["remove_stress", obj])

    def actionApplyStress(self, replication):
        if type(replication) != DNAReplication:
            return f"Cannot apply stress to {replication.name}."
        else:
            replication.properties["replication_stress"] += 1
            return f"You apply replication stress to {replication.name}."

    def actionRemoveStress(self, replication):
        if type(replication) != DNAReplication:
            return f"Cannot remove stress from {replication.name}."
        else:
            replication.properties["replication_stress"] = max(0, replication.properties["replication_stress"] - 1)
            return f"You remove replication stress from {replication.name}."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply_stress":
            self.observationStr = self.actionApplyStress(action[1])
        elif actionVerb == "remove_stress":
            self.observationStr = self.actionRemoveStress(action[1])

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
    actions = ["apply replication stress to DNA Replication", "look", "remove replication stress from DNA Replication", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
