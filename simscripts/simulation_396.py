
# Claim: Exercise increases cancer mortality rates among Chinese citizens.
# The simulation will evaluate the relationship between exercise and cancer mortality rates based on the provided reference text.

from simulation_utils import GameObject, Container

class LifestyleFactor(GameObject):
    def __init__(self, name, exercise_level=0, cancer_mortality_rate=0):
        super().__init__(name)
        self.properties = {
            "exercise_level": exercise_level,  # 0: no exercise, 1: low exercise, 2: moderate exercise, 3: high exercise
            "cancer_mortality_rate": cancer_mortality_rate  # hypothetical cancer mortality rate
        }

    def tick(self):
        # Simulate the effect of exercise on cancer mortality rate
        if self.properties["exercise_level"] == 0:
            self.properties["cancer_mortality_rate"] += 0.1  # No exercise increases mortality
        elif self.properties["exercise_level"] == 1:
            self.properties["cancer_mortality_rate"] += 0.05  # Low exercise slightly increases mortality
        elif self.properties["exercise_level"] == 2:
            self.properties["cancer_mortality_rate"] -= 0.05  # Moderate exercise decreases mortality
        elif self.properties["exercise_level"] == 3:
            self.properties["cancer_mortality_rate"] -= 0.1  # High exercise significantly decreases mortality

    def makeDescriptionStr(self):
        return f"{self.name} with exercise level {self.properties['exercise_level']} has a cancer mortality rate of {self.properties['cancer_mortality_rate']}."

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
        no_exercise = LifestyleFactor("No Exercise", exercise_level=0, cancer_mortality_rate=0.8)
        low_exercise = LifestyleFactor("Low Exercise", exercise_level=1, cancer_mortality_rate=0.75)
        moderate_exercise = LifestyleFactor("Moderate Exercise", exercise_level=2, cancer_mortality_rate=0.7)
        high_exercise = LifestyleFactor("High Exercise", exercise_level=3, cancer_mortality_rate=0.6)
        
        world.addObject(no_exercise)
        world.addObject(low_exercise)
        world.addObject(moderate_exercise)
        world.addObject(high_exercise)
        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"]}

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

    # Evaluate the claim based on the simulation results
    cancer_mortality_rates = [obj.properties["cancer_mortality_rate"] for obj in simulation.rootObject.contains]
    if all(rate > 0.6 for rate in cancer_mortality_rates):
        print("Claim Refuted: Exercise does not increase cancer mortality rates.")
    else:
        print("Claim Supported: Exercise increases cancer mortality rates.")

if __name__ == "__main__":
    main()
