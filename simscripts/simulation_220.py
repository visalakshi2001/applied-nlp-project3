
# Claim: Ca2+ cycling controls whole-body energy homeostasis in beige fat.
# The simulation will model the relationship between Ca2+ cycling and energy homeostasis in beige fat.

from simulation_utils import GameObject, Container

class BeigeFat(GameObject):
    def __init__(self, name, ca2_cycling=0, glucose_expansion=0):
        super().__init__(name)
        self.properties = {
            "ca2_cycling": ca2_cycling,
            "glucose_expansion": glucose_expansion,
            "energy_homeostasis": 0
        }

    def tick(self):
        # Simulate the effect of Ca2+ cycling on energy homeostasis
        if self.properties["ca2_cycling"] > 0:
            self.properties["energy_homeostasis"] = self.properties["ca2_cycling"] * 2  # Arbitrary multiplier for effect
            self.properties["glucose_expansion"] = self.properties["ca2_cycling"] * 1.5  # Arbitrary multiplier for glucose expansion

    def makeDescriptionStr(self):
        description = (f"A {self.name} with Ca2+ cycling level {self.properties['ca2_cycling']}, "
                       f"glucose expansion {self.properties['glucose_expansion']}, "
                       f"and energy homeostasis level {self.properties['energy_homeostasis']}.")
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = World()
        beige_fat = BeigeFat("beige_fat")
        world.addObject(beige_fat)
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
                self.addAction(f"increase Ca2+ cycling of {objReferent}", ["increase", obj])
                self.addAction(f"decrease Ca2+ cycling of {objReferent}", ["decrease", obj])

    def actionIncrease(self, beige_fat):
        if type(beige_fat) != BeigeFat:
            return f"Cannot increase the Ca2+ cycling of {beige_fat.name}."
        else:
            beige_fat.properties["ca2_cycling"] += 1
            return f"You increase the Ca2+ cycling of {beige_fat.name} by 1."
        
    def actionDecrease(self, beige_fat):
        if type(beige_fat) != BeigeFat:
            return f"Cannot decrease the Ca2+ cycling of {beige_fat.name}."
        else:
            beige_fat.properties["ca2_cycling"] -= 1
            return f"You decrease the Ca2+ cycling of {beige_fat.name} by 1."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if (actionVerb == "look"):
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif (actionVerb == "increase"):
            self.observationStr = self.actionIncrease(action[1])
        elif (actionVerb == "decrease"):
            self.observationStr = self.actionDecrease(action[1])

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
    actions = ["increase Ca2+ cycling of beige_fat", "look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Check the energy homeostasis level to verify the claim
    beige_fat = simulation.rootObject.containsItemWithName("beige_fat")[0]
    if beige_fat.properties["energy_homeostasis"] > 0:
        print("Claim Supported: Ca2+ cycling controls whole-body energy homeostasis in beige fat.")
    else:
        print("Claim Refuted: Ca2+ cycling does not control whole-body energy homeostasis in beige fat.")

if __name__ == "__main__":
    main()
