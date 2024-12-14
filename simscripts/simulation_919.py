
# Claim: Participants who quit smoking reduce lung cancer risk by approximately 50%.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, smoking_status, lung_cancer_risk):
        super().__init__(name)
        self.smoking_status = smoking_status  # e.g., "quit", "heavy smoker", "light smoker"
        self.lung_cancer_risk = lung_cancer_risk  # Hazard Ratio (HR)

    def tick(self):
        # Simulate the effect of quitting smoking on lung cancer risk
        if self.smoking_status == "quit":
            self.lung_cancer_risk *= 0.50  # Reduces risk by approximately 50%

    def makeDescriptionStr(self):
        return f"{self.name} is a {self.smoking_status} with a lung cancer risk represented by HR: {self.lung_cancer_risk}."

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
        participant1 = Participant("Participant 1", "quit", 1.0)  # Initial HR of 1.0
        participant2 = Participant("Participant 2", "heavy smoker", 2.0)  # Initial HR of 2.0
        world.addObject(participant1)
        world.addObject(participant2)        
        return world

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("simulate quitting", ["simulate quitting"])

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

        if actionVerb == "simulate quitting":
            # Simulate the effect of quitting smoking
            allParticipants = self.rootObject.getAllContainedObjectsRecursive()
            for participant in allParticipants:
                if isinstance(participant, Participant) and participant.smoking_status == "quit":
                    participant.tick()
            self.observationStr = self.rootObject.makeDescriptionStr()

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print("Simulating quitting smoking...")
    obs = simulation.step("simulate quitting")
    print(obs)

if __name__ == "__main__":
    main()
