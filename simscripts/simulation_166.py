
# Claim: Bariatric surgery leads to negative outcomes in mental health.
# The simulation will evaluate the impact of bariatric surgery on mental health outcomes, specifically depression.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, pre_op_depression=0, post_op_depression=0):
        super().__init__(name)
        self.properties = {
            "pre_op_depression": pre_op_depression,  # Scale from 0 (no depression) to 10 (severe depression)
            "post_op_depression": post_op_depression  # Scale from 0 (no depression) to 10 (severe depression)
        }

    def undergo_bariatric_surgery(self):
        # Simulate the effect of bariatric surgery on depression
        # According to the reference text, surgery leads to a decrease in depression
        self.properties["post_op_depression"] = max(0, self.properties["pre_op_depression"] - (self.properties["pre_op_depression"] * 0.5))  # 50% decrease as an example

    def makeDescriptionStr(self):
        return f"{self.name} has a pre-operative depression level of {self.properties['pre_op_depression']} and a post-operative depression level of {self.properties['post_op_depression']}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("hospital")
        patient1 = Patient("Patient A", pre_op_depression=8)  # High pre-op depression
        patient2 = Patient("Patient B", pre_op_depression=3)  # Low pre-op depression
        world.addObject(patient1)
        world.addObject(patient2)
        return world

    def generatePossibleActions(self):
        self.possibleActions = {
            "perform surgery on Patient A": ["surgery", self.rootObject.contains[0]],  # Patient A
            "perform surgery on Patient B": ["surgery", self.rootObject.contains[1]]   # Patient B
        }

    def step(self, actionStr):
        self.observationStr = ""

        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "surgery":
            patient = action[1]
            patient.undergo_bariatric_surgery()
            self.observationStr = f"{patient.name} underwent bariatric surgery."
        
        # Update the observation string to show the current state of patients
        self.observationStr += "\nCurrent states:\n"
        for obj in self.rootObject.contains:
            self.observationStr += obj.makeDescriptionStr() + "\n"

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    actions = ["perform surgery on Patient A", "perform surgery on Patient B"]
    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()
