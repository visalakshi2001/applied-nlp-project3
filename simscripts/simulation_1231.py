
# Claim: The minor G allele of FOXO3 is related to less severe symptoms of Crohn's Disease.
# The simulation will model the relationship between the G allele and the severity of Crohn's Disease symptoms.

from simulation_utils import GameObject, Container

class Allele(GameObject):
    def __init__(self, name, severity_effect=0):
        super().__init__(name)
        self.severity_effect = severity_effect  # Effect on disease severity

    def tick(self):
        # The G allele is associated with milder symptoms
        if self.name == "G allele":
            self.severity_effect = -1  # Represents milder symptoms
        elif self.name == "T allele":
            self.severity_effect = 1  # Represents more severe symptoms

    def makeDescriptionStr(self):
        return f"{self.name} with severity effect: {self.severity_effect}"

class Patient(GameObject):
    def __init__(self, name, allele):
        super().__init__(name)
        self.allele = allele  # The allele the patient carries

    def tick(self):
        # The patient's symptoms are influenced by the allele they carry
        self.symptom_severity = self.allele.severity_effect

    def makeDescriptionStr(self):
        return f"{self.name} carrying {self.allele.name} has symptom severity: {self.symptom_severity}"

class World(Container):
    def __init__(self):
        super().__init__("environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.doWorldTick()

    def _initialize_simulation(self):
        world = World()
        g_allele = Allele("G allele")
        t_allele = Allele("T allele")
        patient1 = Patient("Patient 1", g_allele)
        patient2 = Patient("Patient 2", t_allele)
        world.addObject(g_allele)
        world.addObject(t_allele)
        world.addObject(patient1)
        world.addObject(patient2)
        return world

    def doWorldTick(self):
        allObjects = self.rootObject.getAllContainedObjectsRecursive()
        for obj in allObjects:
            obj.tick()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
