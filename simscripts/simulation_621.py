
# Claim: Individuals with Alzheimers who participate in six months of physical activity improve cognitive function for up to 18 months.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, cognitive_score=0):
        super().__init__(name)
        self.cognitive_score = cognitive_score
        self.properties = {
            "cognitive_score": cognitive_score,
            "improvement": 0
        }

    def participate_in_activity(self, duration):
        if duration == 6:  # 6 months of physical activity
            self.properties["improvement"] = 0.73  # Improvement observed at 18 months
            self.cognitive_score += self.properties["improvement"]

    def makeDescriptionStr(self):
        return f"{self.name} has a cognitive score of {self.cognitive_score}."

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
        participant = Participant("Alzheimer's Patient")
        world.addObject(participant)
        return world

    def addAction(self, actionStr, actionArgs):
        if actionStr not in self.possibleActions:
            self.possibleActions[actionStr] = actionArgs

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("participate in physical activity", ["participate", self.rootObject.contains[0]])
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
        elif actionVerb == "participate":
            participant = action[1]
            participant.participate_in_activity(6)  # Simulate 6 months of activity
            self.observationStr = f"{participant.name} participated in physical activity for 6 months."

        return self.observationStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Simulate the action of participating in physical activity
    print("Action: participate in physical activity")
    obs = simulation.step("participate in physical activity")
    print(obs)
    print(simulation.rootObject.makeDescriptionStr())

    # Check cognitive score to determine if the claim is supported
    cognitive_score = simulation.rootObject.contains[0].properties["cognitive_score"]
    if cognitive_score > 0:
        print("Claim Supported: Improvement in cognitive function observed.")
    else:
        print("Claim Refuted: No improvement in cognitive function.")

if __name__ == "__main__":
    main()
