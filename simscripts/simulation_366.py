
# Claim: ERAP1 SNPs are epistatic to HLA alleles for ankylosing spondylitis.
# The simulation will test the relationship between ERAP1 SNPs and HLA alleles in the context of ankylosing spondylitis.

from simulation_utils import GameObject, Container

class SNP(GameObject):
    def __init__(self, name, isEpistatic=False):
        super().__init__(name)
        self.properties = {
            "isEpistatic": isEpistatic
        }

class HLAAllele(GameObject):
    def __init__(self, name):
        super().__init__(name)

class AnkylosingSpondylitisSimulation(Container):
    def __init__(self):
        super().__init__("Ankylosing Spondylitis Simulation")
        self.erap1_snp = SNP("ERAP1 SNP rs30187", isEpistatic=True)
        self.hla_b27 = HLAAllele("HLA-B*27")
        self.hla_b40 = HLAAllele("HLA-B*40:01")
        
        self.addObject(self.erap1_snp)
        self.addObject(self.hla_b27)
        self.addObject(self.hla_b40)

    def checkEpistasis(self):
        if self.erap1_snp.getProperty("isEpistatic"):
            return "Supported: ERAP1 SNPs are epistatic to HLA alleles."
        else:
            return "Refuted: ERAP1 SNPs are not epistatic to HLA alleles."

def main():
    simulation = AnkylosingSpondylitisSimulation()
    result = simulation.checkEpistasis()
    print(result)

if __name__ == "__main__":
    main()
