
# Claim: Reduction of Rpl38 alters the composition of the Hox gene mRNAs translation in mice without lowering overall protein synthesis.

from simulation_utils import GameObject, Container

class Rpl38(GameObject):
    def __init__(self, name, protein_synthesis=100, hox_mRNA_translation=100):
        super().__init__(name)
        self.properties = {
            "protein_synthesis": protein_synthesis,  # Overall protein synthesis level
            "hox_mRNA_translation": hox_mRNA_translation  # Translation level of Hox mRNAs
        }

    def reduce_expression(self):
        # Simulate reduction of Rpl38 expression
        self.properties["hox_mRNA_translation"] -= 30  # Arbitrary reduction to represent altered translation
        # Overall protein synthesis remains unchanged
        return self.properties["protein_synthesis"], self.properties["hox_mRNA_translation"]

class MouseEmbryo(Container):
    def __init__(self, name):
        super().__init__(name)
        self.rpl38 = Rpl38("Rpl38")

    def simulate(self):
        # Simulate the reduction of Rpl38
        protein_synthesis, hox_mRNA_translation = self.rpl38.reduce_expression()
        return protein_synthesis, hox_mRNA_translation

class Simulation:
    def __init__(self):
        self.mouse_embryo = MouseEmbryo("Mouse Embryo")

    def run(self):
        protein_synthesis, hox_mRNA_translation = self.mouse_embryo.simulate()
        return protein_synthesis, hox_mRNA_translation

def main():
    simulation = Simulation()
    protein_synthesis, hox_mRNA_translation = simulation.run()
    
    # Check the results against the claim
    if protein_synthesis == 100 and hox_mRNA_translation < 100:
        result = "Supported"
    else:
        result = "Refuted"
    
    print(f"Overall Protein Synthesis: {protein_synthesis}, Hox mRNA Translation: {hox_mRNA_translation}")
    print(f"Claim Verification Result: {result}")

if __name__ == "__main__":
    main()
