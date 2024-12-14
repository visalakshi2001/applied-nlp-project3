
# Claim: The DESMOND program caused substantial weight loss in most participants.
# The simulation will check if the DESMOND program led to significant weight loss based on the provided reference text.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, weight_loss=0):
        super().__init__(name)
        self.weight_loss = weight_loss

    def tick(self):
        # Simulate weight loss over time
        self.weight_loss += 0  # No substantial weight loss as per the conclusion

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
        for i in range(10):  # Simulating 10 participants
            participant = Participant(f"Participant {i+1}")
            program.addParticipant(participant)
        return program

    def generatePossibleActions(self):
        self.possibleActions = {"evaluate": []}

    def step(self, actionStr):
        if actionStr == "evaluate":
            total_weight_loss = self.rootObject.evaluateWeightLoss()
            if total_weight_loss == 0:
                return "The DESMOND program showed no substantial weight loss in participants."
            else:
                return f"The DESMOND program showed a total weight loss of {total_weight_loss} kg."
        else:
            return "Unknown action."

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    
    # Evaluate the program's effectiveness
    result = simulation.step("evaluate")
    print(result)

if __name__ == "__main__":
    main()
