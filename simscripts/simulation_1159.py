
# Claim: The DESMOND program demonstrates no significant impact on weight loss.
# The simulation will evaluate the outcomes of the DESMOND program based on the provided reference text.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, weight_loss=0):
        super().__init__(name)
        self.weight_loss = weight_loss

    def tick(self):
        # Simulate weight loss over time
        # In this case, we assume no significant weight loss occurs
        self.weight_loss = 0  # No significant impact on weight loss

    def makeDescriptionStr(self):
        return f"{self.name} has experienced a weight loss of {self.weight_loss} kg."

class DESMONDProgram(Container):
    def __init__(self):
        super().__init__("DESMOND Program")
        self.participants = []

    def addParticipant(self, participant):
        self.addObject(participant)

    def evaluateWeightLoss(self):
        total_weight_loss = sum(participant.weight_loss for participant in self.contains)
        return total_weight_loss

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.generatePossibleActions()

    def _initialize_simulation(self):
        program = DESMONDProgram()
        # Adding participants to the program
        for i in range(5):  # Simulating 5 participants
            participant = Participant(f"Participant {i + 1}")
            program.addParticipant(participant)
        return program

    def generatePossibleActions(self):
        self.possibleActions = {}
        self.addAction("evaluate weight loss", [])

    def addAction(self, actionStr, actionArgs):
        self.possibleActions[actionStr] = actionArgs

    def step(self, actionStr):
        if actionStr not in self.possibleActions:
            return "I don't understand that."

        action = self.possibleActions[actionStr]
        actionVerb = action[0]

        if actionVerb == "evaluate weight loss":
            total_weight_loss = self.rootObject.evaluateWeightLoss()
            if total_weight_loss == 0:
                return "The DESMOND program shows no significant impact on weight loss."
            else:
                return f"The DESMOND program shows a total weight loss of {total_weight_loss} kg."

        return "ERROR: Unknown action."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    action = "evaluate weight loss"
    print(f"Action: {action}")
    result = simulation.step(action)
    print(result)

if __name__ == "__main__":
    main()
