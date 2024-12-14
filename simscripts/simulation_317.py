
# Claim: Decreased diastolic blood pressure (DBP) is associated with abdominal aortic aneurysm.
# The simulation will analyze the relationship between diastolic blood pressure and abdominal aortic aneurysm.

from simulation_utils import GameObject, Container

class BloodPressure(GameObject):
    def __init__(self, name, diastolic_pressure=0):
        super().__init__(name)
        self.properties = {
            "diastolic_pressure": diastolic_pressure,
            "associated_with_AAA": False
        }

    def assess_association(self):
        # The threshold for association with abdominal aortic aneurysm
        if self.properties["diastolic_pressure"] < 70:  # Arbitrary threshold for simulation
            self.properties["associated_with_AAA"] = True
        else:
            self.properties["associated_with_AAA"] = False

    def makeDescriptionStr(self):
        description = f"{self.name} has a diastolic pressure of {self.properties['diastolic_pressure']} mm Hg."
        if self.properties["associated_with_AAA"]:
            description += " This is associated with abdominal aortic aneurysm."
        else:
            description += " This is not associated with abdominal aortic aneurysm."
        return description

class AorticAneurysm(GameObject):
    def __init__(self, name):
        super().__init__(name)

class World(Container):
    def __init__(self):
        Container.__init__(self, "environment")

    def makeDescriptionStr(self):
        outStr = f"In the {self.name}, you see: \n"
        for obj in self.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.run_assessment()

    def _initialize_simulation(self):
        world = World()
        blood_pressure_low = BloodPressure("Low DBP Patient", diastolic_pressure=65)
        blood_pressure_normal = BloodPressure("Normal DBP Patient", diastolic_pressure=75)
        aortic_aneurysm = AorticAneurysm("Abdominal Aortic Aneurysm")
        
        world.addObject(blood_pressure_low)
        world.addObject(blood_pressure_normal)
        world.addObject(aortic_aneurysm)
        
        return world

    def run_assessment(self):
        for obj in self.rootObject.getAllContainedObjectsRecursive():
            if isinstance(obj, BloodPressure):
                obj.assess_association()

def main():
    simulation = Simulation()
    print(simulation.observationStr)

if __name__ == "__main__":
    main()
