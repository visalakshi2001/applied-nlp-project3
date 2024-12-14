
# Claim: Scapular stabilizer exercises are more effective than general exercise therapy in reducing pain and improving function of the shoulder.

from simulation_utils import GameObject, Container

class Exercise(GameObject):
    def __init__(self, name, effectiveness=0):
        super().__init__(name)
        self.effectiveness = effectiveness

    def tick(self):
        # Simulate the effectiveness of the exercise over time
        self.effectiveness += 1  # Increment effectiveness for simulation purposes

    def makeDescriptionStr(self):
        return f"{self.name} with effectiveness score: {self.effectiveness}"

class Patient(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.pain_level = 10  # Initial pain level
        self.function_score = 0  # Initial function score

    def apply_exercise(self, exercise):
        # Simulate the effect of the exercise on the patient's pain and function
        self.pain_level -= exercise.effectiveness  # Pain decreases with effectiveness
        self.function_score += exercise.effectiveness  # Function improves with effectiveness

    def makeDescriptionStr(self):
        return f"{self.name} with pain level: {self.pain_level} and function score: {self.function_score}"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("rehabilitation environment")
        specific_exercise = Exercise("Scapular Stabilizer Exercises", effectiveness=5)
        general_exercise = Exercise("General Exercise Therapy", effectiveness=2)
        
        patient_specific = Patient("Patient with Specific Exercises")
        patient_general = Patient("Patient with General Exercises")
        
        world.addObject(specific_exercise)
        world.addObject(general_exercise)
        world.addObject(patient_specific)
        world.addObject(patient_general)
        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "apply specific exercise": ["apply", "specific"],
            "apply general exercise": ["apply", "general"],
            "look": ["look"]
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "apply":
            if action[1] == "specific":
                specific_exercise = self.rootObject.contains[0]  # Assuming first object is specific exercise
                patient_specific = self.rootObject.contains[2]  # Assuming third object is patient with specific exercises
                patient_specific.apply_exercise(specific_exercise)
            elif action[1] == "general":
                general_exercise = self.rootObject.contains[1]  # Assuming second object is general exercise
                patient_general = self.rootObject.contains[3]  # Assuming fourth object is patient with general exercises
                patient_general.apply_exercise(general_exercise)

        # Update the effectiveness of exercises
        for obj in self.rootObject.contains:
            if isinstance(obj, Exercise):
                obj.tick()

        self.observationStr = self.rootObject.makeDescriptionStr()
        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["apply specific exercise", "apply general exercise", "look"]
    
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Determine if the claim is supported or refuted based on the final scores
    patient_specific = simulation.rootObject.contains[2]  # Patient with specific exercises
    patient_general = simulation.rootObject.contains[3]  # Patient with general exercises

    if patient_specific.function_score > patient_general.function_score and patient_specific.pain_level < patient_general.pain_level:
        print("Claim Supported: Scapular stabilizer exercises are more effective.")
    else:
        print("Claim Refuted: Scapular stabilizer exercises are not more effective.")

if __name__ == "__main__":
    main()
