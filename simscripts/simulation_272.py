
# Claim: Combination nicotine replacement therapies with varenicline or bupropion are more effective after 12 weeks of treatment compared to varenicline monotherapy.

from simulation_utils import GameObject, Container

class Treatment(GameObject):
    def __init__(self, name, abstinence_rate):
        super().__init__(name)
        self.abstinence_rate = abstinence_rate

    def makeDescriptionStr(self):
        return f"{self.name} has an abstinence rate of {self.abstinence_rate}%."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("treatment_environment")
        combination_therapy = Treatment("Combination Therapy (Varenicline + Bupropion)", 53.0)  # 12-week abstinence rate
        varenicline_monotherapy = Treatment("Varenicline Monotherapy", 43.2)  # 12-week abstinence rate
        world.addObject(combination_therapy)
        world.addObject(varenicline_monotherapy)
        return world

    def makeNameToObjectDict(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        nameToObjectDict = {}
        for obj in allObjects:
            nameToObjectDict[obj.name] = [obj]
        return nameToObjectDict

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

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

        return self.observationStr

    def checkClaim(self):
        combination_rate = 53.0
        varenicline_rate = 43.2
        if combination_rate > varenicline_rate:
            return "Claim Supported: Combination therapy is more effective."
        else:
            return "Claim Refuted: Combination therapy is not more effective."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.checkClaim())

if __name__ == "__main__":
    main()
