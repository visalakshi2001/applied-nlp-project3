
# Claim: Medications to treat obesity are highly effective.
# The simulation will evaluate the effectiveness of three anti-obesity medications based on the provided reference text.

from simulation_utils import GameObject, Container

class Medication(GameObject):
    def __init__(self, name, weight_loss_effect):
        super().__init__(name)
        self.weight_loss_effect = weight_loss_effect  # in kg

    def makeDescriptionStr(self):
        return f"{self.name} can reduce weight by {self.weight_loss_effect} kg."

class ObesityTreatmentSimulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.evaluate_effectiveness()

    def _initialize_simulation(self):
        world = Container("Obesity Treatment Environment")
        orlistat = Medication("Orlistat", 2.9)
        sibutramine = Medication("Sibutramine", 4.2)
        rimonabant = Medication("Rimonabant", 4.7)
        
        world.addObject(orlistat)
        world.addObject(sibutramine)
        world.addObject(rimonabant)
        
        return world

    def evaluate_effectiveness(self):
        total_weight_loss = 0
        medications = self.rootObject.getAllContainedObjectsRecursive()
        
        for med in medications:
            total_weight_loss += med.weight_loss_effect
        
        # Determine if the claim is supported or refuted
        if total_weight_loss > 0:
            self.observationStr += f"\nTotal weight loss from medications: {total_weight_loss} kg. Claim is supported."
        else:
            self.observationStr += f"\nTotal weight loss from medications: {total_weight_loss} kg. Claim is refuted."

def main():
    simulation = ObesityTreatmentSimulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
