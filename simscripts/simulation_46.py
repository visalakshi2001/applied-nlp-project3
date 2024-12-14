
# Claim: A single nucleotide variant the gene DGKK is strongly associated with increased risk of hypospadias.
# The simulation will check the association of SNPs in DGKK with hypospadias risk.

from simulation_utils import GameObject, Container

class SNP(GameObject):
    def __init__(self, name, odds_ratio, p_value):
        super().__init__(name)
        self.odds_ratio = odds_ratio
        self.p_value = p_value

    def is_significant(self):
        return self.p_value < 0.05  # A common threshold for significance

    def makeDescriptionStr(self):
        return f"{self.name} with odds ratio {self.odds_ratio} and p-value {self.p_value}."

class Gene(GameObject):
    def __init__(self, name):
        super().__init__(name)
        self.snps = []

    def add_snp(self, snp):
        self.snps.append(snp)

    def evaluate_association(self):
        significant_snps = [snp for snp in self.snps if snp.is_significant()]
        return len(significant_snps) > 0  # If any SNP is significant, we support the claim

    def makeDescriptionStr(self):
        description = f"Gene: {self.name}, SNPs: \n"
        for snp in self.snps:
            description += "\t" + snp.makeDescriptionStr() + "\n"
        return description

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.result = self.evaluate_claim()

    def _initialize_simulation(self):
        gene_dgkk = Gene("DGKK")
        # Adding SNPs with their odds ratios and p-values
        snp1 = SNP("rs1934179", 2.5, 2.5e-11)
        snp2 = SNP("rs7063116", 2.3, 2.9e-9)
        gene_dgkk.add_snp(snp1)
        gene_dgkk.add_snp(snp2)
        return gene_dgkk

    def evaluate_claim(self):
        if self.rootObject.evaluate_association():
            return "Supported"
        else:
            return "Refuted"

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(f"Claim verification result: {simulation.result}")

if __name__ == "__main__":
    main()
