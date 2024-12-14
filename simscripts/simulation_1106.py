
# Claim: Students who perform poorly in the early years of medical school are less likely to commit professional misconduct later in their careers.
# The simulation will model students' performance and their likelihood of committing professional misconduct based on early academic difficulties.

from simulation_utils import GameObject, Container

class Student(GameObject):
    def __init__(self, name, early_performance, misconduct_likelihood):
        super().__init__(name)
        self.properties = {
            "early_performance": early_performance,  # 0 = poor, 1 = average, 2 = good
            "misconduct_likelihood": misconduct_likelihood  # Probability of committing misconduct
        }

    def tick(self):
        # If the student performed poorly, increase the likelihood of misconduct
        if self.properties["early_performance"] == 0:
            self.properties["misconduct_likelihood"] += 0.5  # Increase likelihood if performance is poor

    def makeDescriptionStr(self):
        return f"{self.name}: Early Performance = {self.properties['early_performance']}, Misconduct Likelihood = {self.properties['misconduct_likelihood']}"

class World(Container):
    def __init__(self):
        super().__init__("medical_school")

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
        student1 = Student("Student A", early_performance=0, misconduct_likelihood=0.1)  # Poor performance
        student2 = Student("Student B", early_performance=2, misconduct_likelihood=0.1)  # Good performance
        world.addObject(student1)
        world.addObject(student2)
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

    # Check the misconduct likelihoods to verify the claim
    student_a_misconduct = simulation.rootObject.contains[0].properties["misconduct_likelihood"]
    student_b_misconduct = simulation.rootObject.contains[1].properties["misconduct_likelihood"]

    if student_a_misconduct > student_b_misconduct:
        print("Claim Refuted: Poor early performance is associated with higher likelihood of misconduct.")
    else:
        print("Claim Supported: Poor early performance is associated with lower likelihood of misconduct.")

if __name__ == "__main__":
    main()
