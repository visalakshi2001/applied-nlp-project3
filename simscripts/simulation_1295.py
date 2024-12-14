
# Claim: There is no relation between Erythromycin use and hypertrophic pyloric stenosis.
# The simulation will assess the relationship between Erythromycin use and the occurrence of hypertrophic pyloric stenosis (IHPS).

from simulation_utils import GameObject, Container

class Infant(GameObject):
    def __init__(self, name, erythromycin_use=0):
        super().__init__(name)
        self.properties = {
            "erythromycin_use": erythromycin_use,  # 0 for no use, 1 for use
            "IHPS": 0  # 0 for no IHPS, 1 for IHPS
        }

    def tick(self):
        # Simulate the effect of erythromycin use on IHPS
        if self.properties["erythromycin_use"] == 1:
            self.properties["IHPS"] = 1  # Assume erythromycin use leads to IHPS

class Mother(GameObject):
    def __init__(self, name, erythromycin_use=0):
        super().__init__(name)
        self.properties = {
            "erythromycin_use": erythromycin_use  # 0 for no use, 1 for use
        }

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("hospital")
        mother = Mother("mother_1", erythromycin_use=1)  # Mother using erythromycin
        infant = Infant("infant_1", erythromycin_use=1)  # Infant using erythromycin
        world.addObject(mother)
        world.addObject(infant)
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
    print("Running simulation...")
    obs = simulation.step("look")
    print(obs)

    # Check the infant's IHPS status
    infant = simulation.rootObject.containsItemWithName("infant_1")[0]
    if infant.properties["IHPS"] == 1:
        result = "Refuted: There is a relation between Erythromycin use and hypertrophic pyloric stenosis."
    else:
        result = "Supported: There is no relation between Erythromycin use and hypertrophic pyloric stenosis."

    print(result)

if __name__ == "__main__":
    main()
