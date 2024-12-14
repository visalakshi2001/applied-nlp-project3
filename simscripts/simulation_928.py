
# Claim: Patients with microcytosis and higher erythrocyte count are more vulnerable to severe malarial anaemia when infected with Plasmodium falciparum.

from simulation_utils import GameObject, Container

class Patient(GameObject):
    def __init__(self, name, microcytosis, erythrocyte_count, has_alpha_thalassemia):
        super().__init__(name)
        self.properties = {
            "microcytosis": microcytosis,
            "erythrocyte_count": erythrocyte_count,
            "has_alpha_thalassemia": has_alpha_thalassemia,
            "vulnerability_to_SMA": self.calculate_vulnerability()
        }

    def calculate_vulnerability(self):
        # If the patient has alpha thalassemia, they are less vulnerable
        if self.properties["has_alpha_thalassemia"]:
            return "low"
        # Higher erythrocyte count and microcytosis increases vulnerability
        if self.properties["microcytosis"] and self.properties["erythrocyte_count"] > 5.0:  # arbitrary threshold
            return "high"
        return "normal"

    def makeDescriptionStr(self):
        return f"{self.name} has microcytosis: {self.properties['microcytosis']}, erythrocyte count: {self.properties['erythrocyte_count']}, vulnerability to SMA: {self.properties['vulnerability_to_SMA']}."

class World(Container):
    def __init__(self):
        Container.__init__(self, "hospital")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()

    def _initialize_simulation(self):
        world = World()
        patient1 = Patient("Patient A", True, 6.0, True)  # has alpha thalassemia
        patient2 = Patient("Patient B", True, 7.0, False)  # does not have alpha thalassemia
        patient3 = Patient("Patient C", False, 4.5, False)  # normal patient
        world.addObject(patient1)
        world.addObject(patient2)
        world.addObject(patient3)
        return world

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
