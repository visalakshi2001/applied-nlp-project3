
# Claim: Ambulatory blood pressure monitoring is inaccurate at diagnosing hypertension.
# The simulation will evaluate the accuracy of ambulatory blood pressure monitoring against clinic and home monitoring.

from simulation_utils import GameObject, Container

class BloodPressureMonitor(GameObject):
    def __init__(self, name, accuracy):
        super().__init__(name)
        self.properties = {
            "accuracy": accuracy  # Accuracy of the monitoring method
        }

    def makeDescriptionStr(self):
        return f"{self.name} with accuracy of {self.properties['accuracy']}%."

class Simulation:
    def __init__(self):
        self.rootObject = self._initialize_simulation()
        self.observationStr = self.rootObject.makeDescriptionStr()
        self.evaluate_accuracy()

    def _initialize_simulation(self):
        world = Container("Hypertension Diagnosis Environment")
        clinic_monitor = BloodPressureMonitor("Clinic Monitor", 70)  # 70% accuracy
        home_monitor = BloodPressureMonitor("Home Monitor", 75)      # 75% accuracy
        ambulatory_monitor = BloodPressureMonitor("Ambulatory Monitor", 90)  # 90% accuracy

        world.addObject(clinic_monitor)
        world.addObject(home_monitor)
        world.addObject(ambulatory_monitor)
        
        return world

    def evaluate_accuracy(self):
        clinic_accuracy = self.rootObject.containsItemWithName("Clinic Monitor")[0].properties["accuracy"]
        home_accuracy = self.rootObject.containsItemWithName("Home Monitor")[0].properties["accuracy"]
        ambulatory_accuracy = self.rootObject.containsItemWithName("Ambulatory Monitor")[0].properties["accuracy"]

        # Check if ambulatory monitoring is more accurate than both clinic and home monitoring
        if ambulatory_accuracy > clinic_accuracy and ambulatory_accuracy > home_accuracy:
            self.result = "Supported: Ambulatory monitoring is more accurate than clinic and home monitoring."
        else:
            self.result = "Refuted: Ambulatory monitoring is not more accurate than clinic and home monitoring."

    def makeDescriptionStr(self):
        outStr = f"In the {self.rootObject.name}, you see: \n"
        for obj in self.rootObject.contains:
            outStr += "\t" + obj.makeDescriptionStr() + "\n"
        return outStr

def main():
    simulation = Simulation()
    print(simulation.observationStr)
    print(simulation.result)

if __name__ == "__main__":
    main()
