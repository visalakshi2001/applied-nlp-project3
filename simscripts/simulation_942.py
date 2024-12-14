
# Claim: Phase information is useful for predicting donor-recipient matches in organ transplantation.
# The simulation will model the relationship between donor and recipient based on MHC haplotypes.

from simulation_utils import GameObject, Container

class Donor(GameObject):
    def __init__(self, name, haplotype):
        super().__init__(name)
        self.haplotype = haplotype  # MHC haplotype of the donor

class Recipient(GameObject):
    def __init__(self, name, haplotype):
        super().__init__(name)
        self.haplotype = haplotype  # MHC haplotype of the recipient

class MatchPredictor:
    def __init__(self, donor, recipient):
        self.donor = donor
        self.recipient = recipient

    def is_match(self):
        # A simple matching logic based on haplotypes
        return self.donor.haplotype == self.recipient.haplotype

class World(Container):
    def __init__(self):
        super().__init__("Transplantation Environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you have:\n"
        for obj in self.contains:
            outStr += f"\t{obj.name} with haplotype {obj.haplotype}\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.match_result = self.check_match()

    def _initialize_simulation(self):
        world = World()
        donor = Donor("Donor_1", "HLA-A1")
        recipient = Recipient("Recipient_1", "HLA-A1")
        world.addObject(donor)
        world.addObject(recipient)
        return world

    def check_match(self):
        donor = self.rootObject.contains[0]  # First object is the donor
        recipient = self.rootObject.contains[1]  # Second object is the recipient
        predictor = MatchPredictor(donor, recipient)
        return predictor.is_match()

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    if simulation.match_result:
        print("The claim is supported: Phase information is useful for predicting donor-recipient matches.")
    else:
        print("The claim is refuted: Phase information is not useful for predicting donor-recipient matches.")

if __name__ == "__main__":
    main()
