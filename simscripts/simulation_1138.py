
# Claim: TRAP+ osteoclasts regulate mature osteoblast maintenance.
# The simulation will model the relationship between TRAP+ osteoclasts and osteoblasts, focusing on the role of PDGF-BB.

from simulation_utils import GameObject, Container

class Osteoclast(GameObject):
    def __init__(self, name, pdgf_bb=0):
        super().__init__(name)
        self.properties = {
            "pdgf_bb": pdgf_bb  # Platelet-derived growth factor-BB level
        }

    def tick(self):
        # Simulate the secretion of PDGF-BB by osteoclasts
        self.properties["pdgf_bb"] += 1  # Increase PDGF-BB level over time

class Osteoblast(GameObject):
    def __init__(self, name, maintenance_level=0):
        super().__init__(name)
        self.properties = {
            "maintenance_level": maintenance_level  # Maintenance level of osteoblasts
        }

    def tick(self, pdgf_bb):
        # Osteoblast maintenance is influenced by PDGF-BB levels
        self.properties["maintenance_level"] += pdgf_bb  # Increase maintenance level based on PDGF-BB

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("Bone Environment")
        osteoclast = Osteoclast("TRAP+ Osteoclast")
        osteoblast = Osteoblast("Mature Osteoblast")
        world.addObject(osteoclast)
        world.addObject(osteoblast)
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

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()

        # Perform a tick for all objects
        self.doWorldTick()

        return self.observationStr

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        osteoclast = next(obj for obj in allObjects if isinstance(obj, Osteoclast))
        osteoblast = next(obj for obj in allObjects if isinstance(obj, Osteoblast))

        # Update osteoclast PDGF-BB level
        osteoclast.tick()
        # Update osteoblast maintenance level based on PDGF-BB
        osteoblast.tick(osteoclast.properties["pdgf_bb"])

def main():
    simulation = Simulation()
    print(simulation.observationStr)

    # Run the simulation for a few steps to observe changes
    for _ in range(5):
        obs = simulation.step("look")
        print(obs)

    # Final state of the osteoblast maintenance level
    osteoblast = simulation.rootObject.containsItemWithName("Mature Osteoblast")[0]
    print(f"Final Osteoblast Maintenance Level: {osteoblast.properties['maintenance_level']}")

    # Determine if the claim is supported or refuted
    if osteoblast.properties['maintenance_level'] > 0:
        print("Claim Supported: TRAP+ osteoclasts regulate mature osteoblast maintenance.")
    else:
        print("Claim Refuted: TRAP+ osteoclasts do not regulate mature osteoblast maintenance.")

if __name__ == "__main__":
    main()
