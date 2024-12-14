
# Claim: Stiff substrates inhibit mesodermal differentiation by degrading beta-catenin in an integrin-dependent manner.
# The simulation will model the effects of substrate stiffness on beta-catenin degradation and mesodermal differentiation.

from simulation_utils import GameObject, Container

class StemCell(GameObject):
    def __init__(self, name, substrate_stiffness=0):
        super().__init__(name)
        self.substrate_stiffness = substrate_stiffness
        self.beta_catenin_level = 100  # Initial level of beta-catenin
        self.differentiation_status = "undifferentiated"  # Initial differentiation status

    def tick(self):
        # Simulate the effect of substrate stiffness on beta-catenin degradation
        if self.substrate_stiffness > 5:  # Assuming stiffness > 5 leads to degradation
            self.beta_catenin_level -= 20  # Degrade beta-catenin
            if self.beta_catenin_level < 50:
                self.differentiation_status = "inhibited"  # Inhibition of differentiation
        else:
            self.beta_catenin_level += 10  # Accumulate beta-catenin
            if self.beta_catenin_level >= 100:
                self.differentiation_status = "differentiated"  # Successful differentiation

    def makeDescriptionStr(self):
        return f"A {self.name} on a substrate with stiffness {self.substrate_stiffness}, beta-catenin level is {self.beta_catenin_level}, and differentiation status is {self.differentiation_status}."

class Substrate(Container):
    def __init__(self, name, stiffness):
        super().__init__(name)
        self.stiffness = stiffness

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("environment")
        stiff_substrate = Substrate("stiff substrate", 10)
        soft_substrate = Substrate("soft substrate", 2)
        stem_cell_stiff = StemCell("stem cell on stiff substrate", substrate_stiffness=stiff_substrate.stiffness)
        stem_cell_soft = StemCell("stem cell on soft substrate", substrate_stiffness=soft_substrate.stiffness)
        
        world.addObject(stiff_substrate)
        world.addObject(soft_substrate)
        world.addObject(stem_cell_stiff)
        world.addObject(stem_cell_soft)
        
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
            if isinstance(obj, StemCell):
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

if __name__ == "__main__":
    main()
