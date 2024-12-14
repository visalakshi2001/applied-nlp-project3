
# Claim: Exercise reduces cancer mortality rates among Chinese citizens.
# This simulation will evaluate the impact of exercise and other lifestyle factors on cancer mortality rates among Chinese women.

from simulation_utils import GameObject, Container

class Woman(GameObject):
    def __init__(self, name, healthy_lifestyle_score=0):
        super().__init__(name)
        self.healthy_lifestyle_score = healthy_lifestyle_score
        self.cancer_mortality_rate = 1.0  # Base mortality rate

    def tick(self):
        # Adjust cancer mortality rate based on healthy lifestyle score
        if self.healthy_lifestyle_score >= 4:
            self.cancer_mortality_rate *= 0.76  # 24% reduction
        elif self.healthy_lifestyle_score == 3:
            self.cancer_mortality_rate *= 0.85  # 15% reduction
        elif self.healthy_lifestyle_score == 2:
            self.cancer_mortality_rate *= 0.95  # 5% reduction
        # If score is 1 or 0, mortality rate remains the same

    def makeDescriptionStr(self):
        return f"{self.name} has a healthy lifestyle score of {self.healthy_lifestyle_score} and a cancer mortality rate of {self.cancer_mortality_rate:.2f}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

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
        woman1 = Woman("Woman 1", healthy_lifestyle_score=5)  # Very healthy
        woman2 = Woman("Woman 2", healthy_lifestyle_score=0)  # Not healthy
        world.addObject(woman1)
        world.addObject(woman2)        
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

if __name__ == "__main__":
    main()

# The output of the simulation will show the cancer mortality rates for women with different healthy lifestyle scores.
# If the cancer mortality rate for women with a higher score is significantly lower, the claim is supported.
# If not, the claim is refuted.
