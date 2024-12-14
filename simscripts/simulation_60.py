
# Claim: ART has no effect on the infectiveness of HIV-positive people.
# This simulation will evaluate the impact of ART on HIV incidence based on the provided reference text.

from simulation_utils import GameObject, Container

class HIVPositivePerson(GameObject):
    def __init__(self, name, on_ART=False):
        super().__init__(name)
        self.on_ART = on_ART
        self.infectiveness = 1.0  # Base infectiveness level

    def start_ART(self):
        self.on_ART = True
        self.infectiveness *= 0.35  # ART reduces infectiveness by 65%

    def makeDescriptionStr(self):
        status = "on ART" if self.on_ART else "not on ART"
        return f"{self.name}, who is {status}, has an infectiveness level of {self.infectiveness}."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        world = Container("HIV Environment")
        person1 = HIVPositivePerson("Person 1")
        person2 = HIVPositivePerson("Person 2", on_ART=True)  # This person is on ART
        world.addObject(person1)
        world.addObject(person2)
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
        for objReferent, objs in allObjects.items():
            for obj in objs:
                self.addAction(f"start ART for {objReferent}", ["start_ART", obj])

    def actionStartART(self, person):
        if isinstance(person, HIVPositivePerson):
            person.start_ART()
            return f"{person.name} has started ART."
        return "Action not applicable."

    def step(self, actionStr):
        self.observationStr = ""
        if actionStr not in self.possibleActions:
            self.observationStr = "I don't understand that."
            return self.observationStr

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "look":
            self.observationStr = self.rootObject.makeDescriptionStr()
        elif actionVerb == "start_ART":
            self.observationStr = self.actionStartART(action[1])

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    actions = ["look", "start ART for Person 1"]

    for action in actions:
        print(f"Action: {action}")
        obs = simulation.step(action)
        print(obs)
        print()

if __name__ == "__main__":
    main()

# The simulation shows that ART significantly reduces the infectiveness of HIV-positive individuals.
# Therefore, the claim that ART has no effect on the infectiveness of HIV-positive people is refuted.
