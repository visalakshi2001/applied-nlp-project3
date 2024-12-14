
# Claim: General exercise therapy is more effective than scapular stabilizer exercises in reducing pain and improving function of the shoulder.

from simulation_utils import GameObject, Container

class Exercise(GameObject):
    def __init__(self, name, effectiveness=0):
        super().__init__(name)
        self.effectiveness = effectiveness

    def tick(self):
        # Simulate the effectiveness of the exercise over time
        self.effectiveness += 1  # Increment effectiveness for simulation purposes

    def makeDescriptionStr(self):
        return f"{self.name} has an effectiveness score of {self.effectiveness}."

class Patient(GameObject):
    def __init__(self, name, exercise_type):
        super().__init__(name)
        self.exercise_type = exercise_type
        self.pain_level = 10  # Initial pain level
        self.function_score = 0  # Initial function score

    def undergo_exercise(self):
        # Simulate the effect of the exercise on pain and function
        if self.exercise_type.effectiveness > 5:  # Arbitrary threshold for effectiveness
            self.pain_level -= 3  # Pain reduces
            self.function_score += 5  # Function improves
        else:
            self.pain_level -= 1  # Minimal pain reduction
            self.function_score += 2  # Minimal function improvement

    def makeDescriptionStr(self):
        return f"{self.name} has a pain level of {self.pain_level} and a function score of {self.function_score}."

class World(Container):
    def __init__(self):
        super().__init__("exercise environment")

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
        general_exercise = Exercise("General Exercise Therapy", effectiveness=6)  # More effective
        scapular_exercise = Exercise("Scapular Stabilizer Exercises", effectiveness=3)  # Less effective

        patient1 = Patient("Patient A", general_exercise)
        patient2 = Patient("Patient B", scapular_exercise)

        world.addObject(general_exercise)
        world.addObject(scapular_exercise)
        world.addObject(patient1)
        world.addObject(patient2)

        return world

    def generatePossibleActions(self):
        self.possibleActions = {"look": ["look"], "exercise": ["exercise"]}

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]

        if action[0] == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif action[0] == "exercise":
            for obj in self.rootObject.contains:
                if isinstance(obj, Patient):
                    obj.undergo_exercise()
                    obj.tick()  # Update effectiveness
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the exercise process
    for _ in range(3):  # Simulate 3 rounds of exercise
        print("Action: exercise")
        obs = simulation.step("exercise")
        print(obs)
        print()

if __name__ == "__main__":
    main()
