
# Claim: Headaches are correlated with cognitive impairment.
# The simulation will evaluate the relationship between headaches and cognitive impairment based on the provided reference text.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, has_severe_headache=False, cognitive_impairment=False):
        super().__init__(name)
        self.properties = {
            "has_severe_headache": has_severe_headache,
            "cognitive_impairment": cognitive_impairment
        }

    def tick(self):
        # Simulate the cognitive impairment based on headache status
        if self.properties["has_severe_headache"]:
            self.properties["cognitive_impairment"] = False  # Evidence suggests no cognitive impairment
        else:
            self.properties["cognitive_impairment"] = False  # No evidence of cognitive impairment

    def makeDescriptionStr(self):
        description = f"{self.name}: Severe Headache: {self.properties['has_severe_headache']}, Cognitive Impairment: {self.properties['cognitive_impairment']}."
        return description

class World(Container):
    def __init__(self):
        Container.__init__(self, "study environment")

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
        participant1 = Participant("Participant 1", has_severe_headache=True)
        participant2 = Participant("Participant 2", has_severe_headache=False)
        world.addObject(participant1)
        world.addObject(participant2)        
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

    # Check the cognitive impairment status of participants
    participants = simulation.rootObject.getAllContainedObjectsRecursive()
    cognitive_impairment_found = any(participant.properties["cognitive_impairment"] for participant in participants)

    if cognitive_impairment_found:
        print("Claim Supported: There is a correlation between headaches and cognitive impairment.")
    else:
        print("Claim Refuted: Evidence was lacking for cognitive impairment for any headache type.")

if __name__ == "__main__":
    main()
