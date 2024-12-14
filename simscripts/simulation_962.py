
# Claim: Post-transcriptional handling of mitochondrial transcripts occurs in mitochondrial RNA granules.
# The simulation will check if the presence of DDX28 as an RNA granule component supports the claim.

from simulation_utils import GameObject, Container

class MitochondrialRNAGranule(GameObject):
    def __init__(self, name, contains_transcripts=False):
        super().__init__(name)
        self.properties = {
            "contains_transcripts": contains_transcripts
        }

    def tick(self):
        # Simulate the handling of transcripts
        if self.properties["contains_transcripts"]:
            return "Transcripts are being handled in the RNA granule."
        else:
            return "No transcripts to handle in the RNA granule."

class DDX28(GameObject):
    def __init__(self, name, is_component=False):
        super().__init__(name)
        self.properties = {
            "is_component": is_component
        }

    def tick(self):
        if self.properties["is_component"]:
            return "DDX28 is functioning as an RNA granule component."
        else:
            return "DDX28 is not functioning as an RNA granule component."

class MitochondrialSimulation:
    def __init__(self):
        self.rna_granule = MitochondrialRNAGranule("Mitochondrial RNA Granule", contains_transcripts=True)
        self.ddx28 = DDX28("DDX28", is_component=True)

    def run_simulation(self):
        rna_granule_status = self.rna_granule.tick()
        ddx28_status = self.ddx28.tick()
        
        if "Transcripts are being handled" in rna_granule_status and "DDX28 is functioning" in ddx28_status:
            return "Claim Supported: Post-transcriptional handling of mitochondrial transcripts occurs in mitochondrial RNA granules."
        else:
            return "Claim Refuted: Post-transcriptional handling of mitochondrial transcripts does not occur in mitochondrial RNA granules."

def main():
    simulation = MitochondrialSimulation()
    result = simulation.run_simulation()
    print(result)

if __name__ == "__main__":
    main()
