
# Claim: Women are more susceptible to death due to pneumonia when compared to men.
# This simulation will model the mortality rates of men and women due to pneumonia based on the provided reference text.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, gender, pneumonia_mortality_rate):
        super().__init__(name)
        self.gender = gender
        self.pneumonia_mortality_rate = pneumonia_mortality_rate

    def makeDescriptionStr(self):
        return f"{self.name} (Gender: {self.gender}, Pneumonia Mortality Rate: {self.pneumonia_mortality_rate})"

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("hospital")
        # Mortality rates based on the reference text
        male_patient = Patient("Male Patient", "Male", 18)  # 18% mortality rate for men
        female_patient = Patient("Female Patient", "Female", 34)  # 34% mortality rate for women
        world.addObject(male_patient)
        world.addObject(female_patient)
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

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

    # Determine the claim's support based on the mortality rates
    male_mortality = 18
    female_mortality = 34
    if female_mortality > male_mortality:
        result = "Supported"
    else:
        result = "Refuted"

    print(f"Claim verification result: {result}")

if __name__ == "__main__":
    main()
