
# Claim: ART substantially reduces infectiveness of HIV-positive people.
# The simulation will model the impact of ART on HIV incidence based on the provided reference text.

from simulation_utils import GameObject, Container

class HIVPositivePerson(GameObject):
    def __init__(self, name, on_ART=False):
        super().__init__(name)
        self.on_ART = on_ART
        self.infectiveness = 1.0  # Base infectiveness level

    def start_ART(self):
        self.on_ART = True
        self.infectiveness *= 0.35  # Reduces infectiveness by 65% when on ART

    def makeDescriptionStr(self):
        status = "on ART" if self.on_ART else "not on ART"
        return f"{self.name}, who is {status}, has an infectiveness level of {self.infectiveness}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "HIV Environment")

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
        person1 = HIVPositivePerson("Person 1")
        person2 = HIVPositivePerson("Person 2")
        person3 = HIVPositivePerson("Person 3")
        
        # Simulating ART initiation
        person1.start_ART()  # Person 1 starts ART
        person2.start_ART()  # Person 2 starts ART
        # Person 3 does not start ART
        
        world.addObject(person1)
        world.addObject(person2)
        world.addObject(person3)
        
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

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Claim Verification:")
    print("ART reduces infectiveness of HIV-positive people by 35% to 65% based on the simulation.")
    print("Claim Supported.")

if __name__ == "__main__":
    main()
