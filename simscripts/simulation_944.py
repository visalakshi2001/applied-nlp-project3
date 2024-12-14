
# Claim: Physical activity does not improve cognitive function in individuals with Alzheimers.
# The simulation will test the claim against the provided reference text.

from simulation_utils import GameObject, Container

class Participant(GameObject):
    def __init__(self, name, cognitive_score=0):
        super().__init__(name)
        self.cognitive_score = cognitive_score

    def improve_cognition(self, improvement):
        self.cognitive_score += improvement

    def deteriorate_cognition(self, deterioration):
        self.cognitive_score -= deterioration

    def makeDescriptionStr(self):
        return f"{self.name} has a cognitive score of {self.cognitive_score}."

class Intervention(Container):
    def __init__(self, name):
        super().__init__(name)
        self.participants = []

    def add_participant(self, participant):
        self.addObject(participant)
        self.participants.append(participant)

    def conduct_intervention(self):
        # Simulating the intervention effects
        for participant in self.participants:
            participant.improve_cognition(0.26)  # Improvement from physical activity
            # Simulating the control group deterioration
            participant.deteriorate_cognition(1.04)  # Deterioration in usual care group

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_intervention()

    def _initialize_simulation(self):
        world = Container("Research Study")
        intervention = Intervention("Physical Activity Intervention")
        
        # Adding participants
        participant1 = Participant("Participant 1", cognitive_score=10)  # Initial cognitive score
        participant2 = Participant("Participant 2", cognitive_score=10)  # Initial cognitive score
        
        intervention.add_participant(participant1)
        intervention.add_participant(participant2)
        
        world.addObject(intervention)
        return world

    def run_intervention(self):
        intervention = self.rootObject.contains[0]  # Get the intervention
        intervention.conduct_intervention()  # Conduct the intervention
        self.observationStr += "\nAfter the intervention:\n"
        for participant in intervention.participants:
            self.observationStr += participant.makeDescriptionStr() + "\n"

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
